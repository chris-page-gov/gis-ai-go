#!/usr/bin/env python3
"""Private candidate links from exact native field headings to captured passages."""
from __future__ import annotations
import argparse
import hashlib
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


def overlays(cards_root, private):
    cards_root, private = no_symlinks(cards_root), no_symlinks(private)
    index = read(checked(cards_root, 'index.json'))
    checkpoint = read(checked(private, 'checkpoint.json'))
    documents = {}
    results = []
    for item in index['cards']:
        native_parent = item.get('parentNativeIdentifier', item['parent'].rsplit('/', 1)[-1])
        if native_parent not in BINDINGS:
            continue
        card = read(checked(cards_root, item['path']), item['sha256'])
        if card['parent']['nativeIdentifier'] != native_parent or card['field']['@id'] != item['id']:
            raise ValueError('Card identity mismatch')
        url = BINDINGS[native_parent]
        entry = checkpoint['records'].get(url, {})
        row = {'@context': {**PREFIXES, **{k: {'@id': 'okfp:' + k, '@type': '@json'} for k in
                 ['card', 'parent', 'source', 'binding', 'passages', 'status', 'rights', 'limitations']}},
               '@id': card['@id'] + '/private-passages', '@type': 'okfp:CandidateFieldPassageOverlay',
               'card': {'@id': card['@id'], 'path': item['path'], 'sha256': item['sha256']},
               'parent': card['parent'], 'source': {'url': url},
               'binding': {'method': 'curated-route-exact-heading-match',
                           'versionStatus': 'current-document-not-independently-version-matched',
                           'nativeField': card['field']['dcterms:identifier']},
               'rights': {'audience': 'private', 'publicationAdmitted': False, 'executionAdmitted': False},
               'limitations': ['Candidate evidence links only; no inferred units, datum, methods or semantic equivalence.'],
               'passages': []}
        if entry.get('status') != 'captured':
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


def export(root, cards_root=None, private=None, output=None):
    root = no_symlinks(root)
    cards_root = cards_root or root / 'artifacts/okf-plus/field-cards'
    private = private or root / 'artifacts/okf-plus/private-os-documents'
    output = no_symlinks(output or root / 'artifacts/okf-plus/field-passages')
    if not output.is_relative_to(root / 'artifacts'):
        raise ValueError('Output must be under artifacts')
    rows = overlays(cards_root, private)
    files = {hashlib.sha256(row['@id'].encode()).hexdigest() + '.jsonld': canonical(row) for row in rows}
    summary = {'schema': 'gis-ai-go.okf-plus-field-passages.v1', 'candidateOnly': True,
               'counts': dict(Counter(row['status'] for row in rows)), 'bindings': BINDINGS,
               'files': [{'path': name, 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sorted(files.items())]}
    files['index.json'] = canonical(summary)
    for name in files:
        target = no_symlinks(output / name)
        if target.exists() and not target.is_file():
            raise ValueError('Output leaf must be a regular file')
    output.mkdir(parents=True, exist_ok=True)
    for name, raw in files.items():
        (output / name).write_bytes(raw)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    summary = export(args.root)
    print(canonical({'counts': summary['counts'], 'candidateOnly': True}).decode(), end='')

if __name__ == '__main__':
    main()
