#!/usr/bin/env python3
"""Offline, lossless source-native field evidence cards; no remote resolution."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

try:
    from .model import canonical, digest, read_markdown
except ImportError:
    from model import canonical, digest, read_markdown

ROOT = Path(__file__).resolve().parents[2]
MAX_CARD_BYTES = 64 * 1024


def tokens(value):
    text = json.dumps(value, ensure_ascii=False)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    return sorted(set(re.findall(r'[a-z0-9]+', text.casefold())))


def cards_from_records(root, max_card_bytes=MAX_CARD_BYTES):
    """Bind exact fields to parent bytes and all retained provenance claims.

    Hashes identify local inputs; source response claims remain source claims and
    are not upgraded to independent verification by this derivative export.
    """
    root = Path(root).resolve()
    if type(max_card_bytes) is not int or not 1024 <= max_card_bytes <= 1024 * 1024:
        raise ValueError('max_card_bytes must be 1024 to 1048576')
    cards = []
    seen = set()
    snapshot_hashes = {}
    for path in sorted((root / 'okf-plus/records/os-ngd-collections').glob('*.md')):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError('Unsafe parent path')
        parent, _ = read_markdown(path)
        for field in parent.get('okfp:field', []):
            identity = field.get('@id')
            if not isinstance(identity, str) or not identity or identity in seen:
                raise ValueError('Missing or duplicate field identity')
            seen.add(identity)
            sources = parent['sources']
            snapshots = []
            for source in sources:
                relative = source.get('normalisedSource')
                if relative is None:
                    continue
                snapshot = root / relative
                if not snapshot.resolve().is_relative_to(root) or snapshot.is_symlink():
                    raise ValueError('Unsafe snapshot path')
                if relative not in snapshot_hashes:
                    snapshot_hashes[relative] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
                snapshots.append({'path': relative, 'sha256': snapshot_hashes[relative]})
            card = {'@context': [parent['@context'], {
                        'field': 'okfp:field', 'parent': 'okfp:parentCollection',
                        'provenance': {'@id': 'okfp:provenance', '@type': '@json'},
                        'rights': {'@id': 'okfp:rights', '@type': '@json'},
                        'limitations': {'@id': 'okfp:limitations', '@type': '@json'}}], '@id': identity + '/evidence-card',
                    '@type': 'okfp:FieldEvidenceCard', 'field': field,
                    'parent': {'@id': parent['@id'], 'nativeIdentifier': parent['nativeIdentifier'],
                               'resource': parent['resource']},
                    'provenance': {'parentPath': path.relative_to(root).as_posix(),
                                   'parentSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                   'fieldSha256': digest(field), 'sources': sources,
                                   'snapshotFiles': snapshots,
                                   'schemaEvidence': parent.get('schemaEvidence', {})},
                    'rights': parent['rights'], 'limitations': parent.get('limitations', []) + [
                        'Metadata evidence only; no feature values or live retrieval admission.',
                        'Units, datum and methods are only those stated in the retained native field; no aliases or missing semantics inferred.',
                        'Source provenance claims are retained; export hashes bind local inputs and do not independently validate upstream responses.']}
            if len(canonical(card)) > max_card_bytes:
                raise ValueError('Complete field card exceeds byte limit: ' + identity)
            cards.append(card)
    return cards


def search_cards(cards, question, max_records=10, max_bytes=65536):
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise ValueError('question must contain 1 to 2000 characters')
    if type(max_records) is not int or not 1 <= max_records <= 100:
        raise ValueError('max_records must be 1 to 100')
    if type(max_bytes) is not int or not 1024 <= max_bytes <= 1024 * 1024:
        raise ValueError('max_bytes must be 1024 to 1048576')
    terms = set(tokens(question))
    ranked = []
    for card in cards:
        native = card['field'].get('dcterms:identifier', '')
        parent_native = card.get('parent', {}).get('nativeIdentifier', '')
        native_tokens = tokens([native, parent_native])
        evidence_tokens = set(tokens(card['field'])) | set(tokens(parent_native))
        # OS native identifiers can join words without separators. Match literal
        # substrings of at least four characters only within native identifiers;
        # this adds no synonyms and does not infer a measurement's meaning.
        matched = {term for term in terms if term in evidence_tokens or
                   (len(term) >= 4 and any(term in token for token in native_tokens))}
        ranked.append((len(matched), card))
    ranked = sorted((x for x in ranked if x[0]), key=lambda x: (-x[0], x[1]['@id']))
    result = {'schema': 'gis-ai-go.okf-plus-field-search.v1', 'status': 'discovery-only',
              'question': question, 'matchingCandidates': len(ranked),
              'omittedCandidates': 0, 'omissions': [], 'cards': [x[1] for x in ranked[:max_records]]}
    if len(ranked) > max_records:
        result['omissions'].append('record-limit')
    while True:
        result['omittedCandidates'] = len(ranked) - len(result['cards'])
        if len(canonical(result)) <= max_bytes:
            return result
        if not result['cards']:
            raise ValueError('Byte budget cannot fit search envelope')
        result['cards'].pop()
        if 'byte-limit' not in result['omissions']:
            result['omissions'].append('byte-limit')


def export(root, output, max_card_bytes=MAX_CARD_BYTES):
    cards = cards_from_records(root, max_card_bytes)
    output = Path(output).absolute()
    # Inspect lexical paths before resolving: resolving first conceals symlinks.
    for component in (output, *output.parents):
        if component.is_symlink():
            raise ValueError('Symlink output path forbidden')
    output = output.resolve()
    root = Path(root).resolve()
    if not output.is_relative_to(root / 'artifacts'):
        raise ValueError('Output must be under checkout artifacts')
    index = {'schema': 'gis-ai-go.okf-plus-field-index.v1', 'cards': []}
    # Validate the complete cohort before writing any card.
    with tempfile.TemporaryDirectory(prefix='okf-field-cards-') as staging:
        staged = Path(staging)
        for card in cards:
            name = hashlib.sha256(card['field']['@id'].encode()).hexdigest() + '.jsonld'
            raw = canonical(card)
            (staged / name).write_bytes(raw)
            index['cards'].append({'id': card['field']['@id'], 'parent': card['parent']['@id'],
                                   'path': name, 'sha256': hashlib.sha256(raw).hexdigest(),
                                   'bytes': len(raw),
                                   'parentNativeIdentifier': card['parent']['nativeIdentifier'],
                                   'tokens': tokens([card['field'], card['parent']['nativeIdentifier']])})
        (staged / 'index.json').write_bytes(canonical(index))
        # Check every destination before the first write, including index.json.
        for path in staged.iterdir():
            destination = output / path.name
            if destination.is_symlink():
                raise ValueError('Symlink output leaf forbidden')
            if destination.exists() and not destination.is_file():
                raise ValueError('Output leaf is not a regular file')
        output.mkdir(parents=True, exist_ok=True)
        for path in sorted(staged.iterdir()):
            (output / path.name).write_bytes(path.read_bytes())
    return cards, index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--question')
    parser.add_argument('--max-records', type=int, default=10)
    parser.add_argument('--max-bytes', type=int, default=65536)
    parser.add_argument('--max-card-bytes', type=int, default=MAX_CARD_BYTES)
    args = parser.parse_args()
    cards, index = export(args.root, args.output or args.root / 'artifacts/okf-plus/field-cards', args.max_card_bytes)
    result = search_cards(cards, args.question, args.max_records, args.max_bytes) if args.question else {'cards': len(cards), 'schema': index['schema']}
    print(canonical(result).decode(), end='')


if __name__ == '__main__':
    main()
