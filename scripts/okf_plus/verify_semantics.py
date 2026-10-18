#!/usr/bin/env python3
"""Build and independently verify the small OS record view, without networking."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

try:
    from .model import canonical, digest, load_json, read_markdown
    from .semantic import CONTEXT, MAX_CARD_BYTES, generate_semantic, resolve_pointer
    from .semantic_search import render, search
except ImportError:
    from model import canonical, digest, load_json, read_markdown
    from semantic import CONTEXT, MAX_CARD_BYTES, generate_semantic, resolve_pointer
    from semantic_search import render, search

ROOT = Path(__file__).resolve().parents[2]
MARKER = 'gis-ai-go-okf-plus-atomic-build.v1\n'


def verify_cards(root, directory):
    """Inspect emitted records independently of the generator's counters."""
    from jsonschema import Draft202012Validator
    schema_path = root / 'okf-plus/schemas/semantic-card.schema.json'
    if (not schema_path.is_file() or schema_path.is_symlink()
            or not schema_path.resolve().is_relative_to(root.resolve())):
        raise ValueError('Required semantic card schema is missing or unsafe')
    schema = load_json(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    if load_json((directory / 'context.jsonld').read_text()) != {'@context': CONTEXT}:
        raise ValueError('Emitted Linked Data context differs from the reviewed mapping')
    sources, identities, kinds = {}, set(), {}
    total, maximum = 0, 0
    for path in sorted((directory / 'cards').rglob('*.md')):
        if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
            raise ValueError('Card escapes generated directory')
        raw = path.read_bytes()
        if len(raw) > MAX_CARD_BYTES:
            raise ValueError('Oversized atomic record')
        card, _ = read_markdown(path)
        validator.validate(card)
        if card['@id'] in identities:
            raise ValueError('Duplicate atomic identity')
        identities.add(card['@id'])
        if set(card) - set(CONTEXT) - {'@id', '@type', '@context'}:
            raise ValueError('Unmapped Linked Data term')
        evidence = card['source']
        relative = Path(evidence['snapshot'])
        if relative.is_absolute() or '..' in relative.parts or relative.parts[:2] != ('okf-plus', 'source'):
            raise ValueError('Source snapshot is outside the admitted source module')
        source_path = root / relative
        if source_path.is_symlink() or not source_path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Source snapshot escapes the checkout')
        if relative not in sources:
            sources[relative] = load_json(source_path.read_text())
        snapshot = sources[relative]
        if digest(resolve_pointer(snapshot, evidence['pointer'])) != evidence['sha256']:
            raise ValueError('Atomic source value digest mismatch')
        if digest(resolve_pointer(snapshot, evidence['recordPointer'])) != evidence['recordSha256']:
            raise ValueError('Atomic source record digest mismatch')
        supplement = card.get('semanticEvidence')
        if supplement:
            supplement_path = Path(supplement['snapshot'])
            if supplement_path.is_absolute() or '..' in supplement_path.parts or supplement_path.parts[:2] != ('okf-plus', 'source'):
                raise ValueError('Semantic evidence escapes source module')
            if (root / supplement_path).is_symlink() or not (root / supplement_path).resolve().is_relative_to(root.resolve()):
                raise ValueError('Semantic evidence escapes the checkout')
            if supplement_path not in sources:
                sources[supplement_path] = load_json((root / supplement_path).read_text())
            if digest(resolve_pointer(sources[supplement_path], supplement['pointer'])) != supplement['sha256']:
                raise ValueError('Semantic evidence digest mismatch')
        total += 1
        maximum = max(maximum, len(raw))
        kinds[card['kind']] = kinds.get(card['kind'], 0) + 1
    if not total:
        raise ValueError('No atomic records generated')
    return {'recordsChecked': total, 'maximumCardBytes': maximum, 'byKind': dict(sorted(kinds.items())),
            'sourceSnapshotsChecked': len(sources)}


def verify(root, output, revision):
    root, output = Path(root).resolve(), Path(output).absolute()
    if output == root or output.resolve().is_relative_to(root / 'okf-plus'):
        raise ValueError('Output cannot replace source records')
    if any(part.is_symlink() for part in (output, *output.parents)):
        raise ValueError('Output cannot traverse symlinks')
    if output.exists() and (not (output / '.okf-plus-atomic-generated').is_file()
                            or (output / '.okf-plus-atomic-generated').read_text() != MARKER):
        raise ValueError('Refusing to replace an unmarked output directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    inputs = []
    input_paths = sorted(set((root / 'okf-plus/source').glob('os*.json')) |
                         {root / 'okf-plus/source/locator-index.json'} |
                         set((root / 'scripts/okf_plus').glob('*.py')) |
                         set((root / 'okf-plus/schemas').glob('*.json')))
    for path in input_paths:
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError('Build input escapes checkout')
        if path.is_file():
            inputs.append({'path': path.relative_to(root).as_posix(),
                           'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    with tempfile.TemporaryDirectory(prefix='.okf-atomic-', dir=output.parent) as temporary:
        staged = Path(temporary) / 'staged'
        coverage = generate_semantic(root, staged, revision)
        audit = verify_cards(root, staged)
        if audit['recordsChecked'] != coverage['cardCount'] or audit['maximumCardBytes'] != coverage['maximumCardBytes']:
            raise ValueError('Coverage differs from independent record audit')
        # Real ordinary-language prompts: no expected identifiers are injected.
        probes = []
        for question in ('pavement width', 'building heights', 'road height above sea level'):
            result = search(staged, question, max_records=5, max_bytes=16384)
            if len(render(result)) > 16384 or not result.get('results'):
                raise ValueError('Bounded discovery probe failed')
            probes.append({'question': question, 'status': 'retrieved-evidence-not-answer-acceptance',
                           'bytes': len(render(result)), 'result': result})
        report = {'schema': 'gis-ai-go.okf-plus-atomic-verification.v1', 'revision': revision,
                  'inputDigest': digest(inputs), 'inputs': inputs,
                  'status': 'passed', 'audit': audit, 'discoveryProbes': probes,
                  'networkRequests': 0, 'globalCompleteness': 'not-established',
                  'limitations': ['Evidence retrieval is not an independent semantic answer assessment.',
                                  'Fresh OS acquisition and authenticated live retrieval are separate checks.']}
        (staged / 'verification.json').write_bytes(canonical(report) + b'\n')
        (staged / '.okf-plus-atomic-generated').write_text(MARKER)
        previous = Path(temporary) / 'previous'
        if output.exists():
            output.rename(previous)
        try:
            staged.rename(output)
        except BaseException:
            if previous.exists():
                previous.rename(output)
            raise
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/okf-plus/atomic')
    parser.add_argument('--revision')
    args = parser.parse_args()
    revision = args.revision or subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.root, text=True).strip()
    def deny(event, _args):
        if event in ('socket.connect', 'socket.getaddrinfo', 'urllib.Request'):
            raise RuntimeError('Network is forbidden during atomic verification')
    sys.addaudithook(deny)
    result = verify(args.root, args.output, revision)
    print(json.dumps({'status': result['status'], **result['audit']}, sort_keys=True))


if __name__ == '__main__':
    main()
