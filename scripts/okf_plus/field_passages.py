#!/usr/bin/env python3
"""Private candidate links from exact native field headings to captured passages."""
from __future__ import annotations
import argparse
import hashlib
import re
import ctypes
import os
import shutil
import tempfile
from collections import Counter
from pathlib import Path
try:
    from .model import PREFIXES, canonical, load_json
    from .passages import no_symlinks
except ImportError:
    from model import PREFIXES, canonical, load_json
    from passages import no_symlinks

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://docs.os.uk/osngd/data-structure/'
BINDINGS = {'bld-fts-building-4': BASE + 'buildings/building-features/building.md',
            'trn-ntwk-roadlink-5': BASE + 'transport/transport-network/road-link.md',
            'trn-ntwk-pavementlink-1': BASE + 'transport/transport-network/pavement-link.md'}


def checked(base, relative):
    path = no_symlinks(Path(base) / relative)
    if not path.is_relative_to(Path(base).absolute()):
        raise ValueError('Path escapes evidence root')
    return path


def read(path, expected=None):
    raw = no_symlinks(path).read_bytes()
    if expected and hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('Evidence checksum mismatch')
    return load_json(raw.decode())


def heading_text(text):
    return text.replace('\\_', '_').replace('`', '')


def document_sections(private, entry, url):
    directory = checked(private, entry['passageDirectory'])
    manifest_path = checked(directory, 'manifest.jsonld')
    manifest = read(manifest_path)
    source = manifest['source']
    if source['url'] != url or source['sha256'] != entry['receipt']['sha256']:
        raise ValueError('Document source binding mismatch')
    sections = {}
    reconstructed = hashlib.sha256()
    reconstructed_bytes = 0
    for segment in manifest['segments']:
        path = checked(directory, segment['file'])
        payload = read(path, segment['sha256'])
        if path.stat().st_size != segment['bytes']:
            raise ValueError('Passage byte length mismatch')
        chunk = payload['text'].encode('utf-8')
        reconstructed.update(chunk)
        reconstructed_bytes += len(chunk)
        if payload['source'] != source or payload['position'] != segment['position']:
            raise ValueError('Passage source or position mismatch')
        for heading in payload['headingBreadcrumb']:
            name = heading_text(heading['text'])
            key = (heading['line'], heading['level'])
            sections.setdefault(name, {}).setdefault(key, []).append({
                '@id': payload['@id'], 'path': path.relative_to(Path(private).absolute()).as_posix(),
                'sha256': segment['sha256'], 'bytes': segment['bytes'],
                'position': segment['position'], 'headingBreadcrumb': payload['headingBreadcrumb']})
    if (reconstructed.hexdigest() != source['sha256'] or
            reconstructed_bytes != source['bytes'] or
            manifest['reconstruction']['sha256'] != reconstructed.hexdigest() or
            manifest['reconstruction']['bytes'] != reconstructed_bytes or
            ('bytes' in entry['receipt'] and entry['receipt']['bytes'] != reconstructed_bytes)):
        raise ValueError('Document reconstruction checksum or byte length mismatch')
    return source, sections, hashlib.sha256(manifest_path.read_bytes()).hexdigest()


def discover_bindings(root):
    """Exact frozen titles provide candidate routes, never version equivalence."""
    root = no_symlinks(root)
    paths = {'collections': 'okf-plus/source/os-ngd-collections.json',
             'documentation': 'okf-plus/source/osngd-documentation.json'}
    snapshots = {key: read(checked(root, path)) for key, path in paths.items()}
    hashes = {key: hashlib.sha256(checked(root, path).read_bytes()).hexdigest()
              for key, path in paths.items()}
    candidates = {}
    for number, document in enumerate(snapshots['documentation']['records']):
        if document['url'].startswith(BASE):
            candidates.setdefault(document['title'], []).append((number, document))
    result = {}
    for number, collection in enumerate(snapshots['collections']['records']):
        title = collection['title']
        unversioned = re.sub(r' v[0-9]+$', '', title)
        matches = candidates.get(unversioned, [])
        evidence = {'collectionTitle': title, 'matchTitle': unversioned,
            'collectionSnapshot': paths['collections'], 'collectionSnapshotSha256': hashes['collections'],
            'collectionPointer': '/records/' + str(number),
            'documentationSnapshot': paths['documentation'], 'documentationSnapshotSha256': hashes['documentation'],
            'candidates': [{'url': document['url'], 'title': document['title'],
                'pointer': '/records/' + str(index)} for index, document in matches]}
        result[collection['id']] = {'status': 'unique-route' if len(matches) == 1 else
            ('ambiguous-route' if matches else 'route-not-found'),
            'url': matches[0][1]['url'] if len(matches) == 1 else None, 'evidence': evidence}
    return result


def bounded_overlay(row, max_bytes):
    """Externalise whole ordered passage references; every file stays bounded."""
    if len(canonical(row)) <= max_bytes:
        return row, {}
    row = dict(row)
    passages = row['passages']
    if not passages:
        raise ValueError('Overlay metadata exceeds byte ceiling')
    files, entries, current = {}, [], []
    key = hashlib.sha256(row['@id'].encode()).hexdigest()
    def publish(group):
        payload = canonical({'references': group})
        name = key + '-references-' + str(len(entries) + 1) + '.json'
        files[name] = payload
        entries.append({'path': name, 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)})
    for passage in passages:
        candidate = current + [passage]
        if len(canonical({'references': candidate})) > max_bytes:
            if not current: raise ValueError('Single passage reference exceeds byte ceiling')
            publish(current)
            current = [passage]
            if len(canonical({'references': current})) > max_bytes:
                raise ValueError('Single passage reference exceeds byte ceiling')
        else: current = candidate
    if current: publish(current)
    manifest = {'profile': 'okf-plus-passage-reference-manifest.v1',
        'sha256': hashlib.sha256(canonical(passages)).hexdigest(), 'referenceCount': len(passages),
        'reconstruction': 'Concatenate references arrays from ordered parts.', 'parts': entries}
    manifest_name = key + '-references-manifest.json'
    raw = canonical(manifest)
    if len(raw) > max_bytes: raise ValueError('Reference manifest exceeds byte ceiling')
    files[manifest_name] = raw
    row['passages'] = []
    row['passageManifest'] = {'path': manifest_name, 'sha256': hashlib.sha256(raw).hexdigest(),
                              'bytes': len(raw), 'referenceCount': len(passages)}
    if len(canonical(row)) > max_bytes: raise ValueError('Overlay metadata exceeds byte ceiling')
    return row, files


def overlays(cards_root, private, *, all_collections=False, root=ROOT):
    cards_root, private = no_symlinks(cards_root), no_symlinks(private)
    index = read(checked(cards_root, 'index.json'))
    checkpoint = read(checked(private, 'checkpoint.json'))
    registry = discover_bindings(root) if all_collections else {}
    documents = {}
    results = []
    for item in index['cards']:
        native_parent = item.get('parentNativeIdentifier', item['parent'].rsplit('/', 1)[-1])
        if not all_collections and native_parent not in BINDINGS:
            continue
        card = read(checked(cards_root, item['path']), item['sha256'])
        if card['parent']['nativeIdentifier'] != native_parent or card['field']['@id'] != item['id']:
            raise ValueError('Card identity mismatch')
        route = registry.get(native_parent, {'status': 'route-not-found', 'url': None}) if all_collections else {}
        url = route.get('url') if all_collections else BINDINGS[native_parent]
        entry = checkpoint['records'].get(url, {})
        row = {'@context': {**PREFIXES, **{k: {'@id': 'okfp:' + k, '@type': '@json'} for k in
                 ['card', 'parent', 'source', 'binding', 'passages', 'passageManifest', 'status', 'rights', 'limitations']}},
               '@id': card['@id'] + '/private-passages', '@type': 'okfp:CandidateFieldPassageOverlay',
               'card': {'@id': card['@id'], 'path': item['path'], 'sha256': item['sha256']},
               'parent': card['parent'], 'source': {'url': url},
               'binding': {'method': 'curated-route-exact-heading-match',
                           'versionStatus': 'current-document-not-independently-version-matched',
                           'nativeField': card['field']['dcterms:identifier']},
               'rights': {'audience': 'private', 'publicationAdmitted': False, 'executionAdmitted': False},
               'limitations': ['Candidate evidence links only; no inferred units, datum, methods or semantic equivalence.'],
               'passages': []}
        if all_collections:
            row['binding']['method'] = 'frozen-exact-title-exact-heading-candidate'
            row['binding']['routeEvidence'] = route.get('evidence', {})
        if all_collections and route['status'] != 'unique-route':
            row['status'] = route['status']
        elif entry.get('status') != 'captured':
            row['status'] = 'document-not-captured'
        else:
            if url not in documents:
                documents[url] = document_sections(private, entry, url)
            source, sections, manifest_hash = documents[url]
            row['source'] = {**source, 'manifestSha256': manifest_hash, 'receipt': entry['receipt']}
            matches = sections.get(card['field']['dcterms:identifier'], {})
            if len(matches) > 1:
                row['status'] = 'ambiguous-heading'
            elif not matches:
                row['status'] = 'heading-not-found'
            else:
                row['status'] = 'matched'
                row['passages'] = next(iter(matches.values()))
        results.append(row)
    return results


def export(root, cards_root=None, private=None, output=None, *, all_collections=False, max_overlay_bytes=16384):
    root = no_symlinks(root)
    cards_root = cards_root or root / 'artifacts/okf-plus/field-cards'
    private = private or root / 'artifacts/okf-plus/private-os-documents'
    output = no_symlinks(output or root / 'artifacts/okf-plus/field-passages')
    if not output.is_relative_to(root / 'artifacts'):
        raise ValueError('Output must be under artifacts')
    if type(max_overlay_bytes) is not int or not 1024 <= max_overlay_bytes <= 16384:
        raise ValueError('Overlay byte ceiling must be 1024..16384')
    if all_collections and output.exists():
        raise ValueError('All-collection output must be a new directory')
    rows = overlays(cards_root, private, all_collections=all_collections, root=root)
    files = {}
    for row in rows:
        bounded, references = bounded_overlay(row, max_overlay_bytes)
        files.update(references)
        files[hashlib.sha256(row['@id'].encode()).hexdigest() + '.jsonld'] = canonical(bounded)
    summary = {'schema': 'gis-ai-go.okf-plus-field-passages.v1', 'candidateOnly': True,
               'counts': dict(Counter(row['status'] for row in rows)),
               'bindings': {key: value['url'] for key,value in discover_bindings(root).items()
                            if value['status'] == 'unique-route'} if all_collections else BINDINGS,
               'allCollections': all_collections, 'maxOverlayBytes': max_overlay_bytes,
               'files': [{'path': name, 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sorted(files.items())]}
    files['index.json'] = canonical(summary)
    for name in files:
        target = no_symlinks(output / name)
        if target.exists() and not target.is_file():
            raise ValueError('Output leaf must be a regular file')
    if all_collections:
        output.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix='.' + output.name + '-', dir=output.parent))
        try:
            for name, raw in files.items():
                with (stage / name).open('wb') as stream:
                    stream.write(raw); stream.flush(); os.fsync(stream.fileno())
            descriptor = os.open(stage, os.O_RDONLY | os.O_DIRECTORY)
            try: os.fsync(descriptor)
            finally: os.close(descriptor)
            rename = getattr(ctypes.CDLL(None, use_errno=True), 'renameat2', None)
            if rename is None: raise OSError('Atomic all-collection publication requires renameat2')
            rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
            rename.restype = ctypes.c_int
            no_symlinks(output)
            if rename(-100, os.fsencode(stage), -100, os.fsencode(output), 1):
                error = ctypes.get_errno()
                raise OSError(error, os.strerror(error), str(output))
        finally:
            if stage.exists(): shutil.rmtree(stage)
    else:
        output.mkdir(parents=True, exist_ok=True)
        for name, raw in files.items():
            (output / name).write_bytes(raw)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--all-collections', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    summary = export(args.root, output=args.output, all_collections=args.all_collections)
    print(canonical({'counts': summary['counts'], 'candidateOnly': True}).decode(), end='')

if __name__ == '__main__':
    main()
