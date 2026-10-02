#!/usr/bin/env python3
"""Offline, additive Explorer context-v3 producer for every OKF+ metadata record.

Uses exact vendored Explorer contracts without a sibling checkout or network.
The bounded v1 index is an evaluation aid; the v3 corpus contains the full input.
Publication URLs are proposed bindings, not evidence of deployment or admission.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata
from urllib.parse import urlsplit

try:
    from .model import load_json
except ImportError:
    from model import load_json

EXPLORER_REVISION = '84fb37f11411c04db8c58046827061f741249002'
SCHEMA_DIR = 'profiles/context-assembly/v1/'
ENGINE_DIR = 'apps/okf-explorer/src/lib/context/'
ENGINE_FILES = ('index.ts', 'types.ts', 'unit.ts', 'corpus.ts', 'corpusV3.ts')
SCHEMA_FILES = ('common.schema.json', 'context-adjacency.schema.json', 'corpus-v3.schema.json',
                'discovery-card.schema.json', 'discovery-cards.schema.json',
                'discovery-postings.schema.json', 'evidence-unit.schema.json', 'index.schema.json')
VENDOR_ROOT = Path(__file__).resolve().parents[2] / 'okf-plus/vendor/explorer-context'
VENDOR_MANIFEST_SHA256 = '5f43735afcc49fad7dd20e7f893a9c9011d5a441d131dc77d80e94eaf37a8ea9'
MARKER = 'gis-ai-go.okf-plus-context-projection.v1\n'
MAX_RECORD_TEXT = 100_000
SHARD_BYTES = 1024 * 1024
LIMITATIONS = [
    'Complete coverage of the bound generated OKF+ input, not every possible OS/ONS source or observation.',
    'Evidence units are complete normalised metadata records, not statistical observations or verbatim official documents.',
    'Source-native provenance, rights, temporal and release/update facts are retained whole; unknown fields remain unknown.',
    'Discovery cards are navigation aids; complete evidence is separately hash-bound and never truncated.',
    'The v1 index is representative; the corpus-v3 inventory and lexical postings cover every input record.',
    'Authored concepts provide navigation to their complete metadata. This does not establish answer sufficiency for arbitrary questions.',
    'Source content is inert. No model, provider API or network call occurs during production or local engine verification.',
    'Candidate publication bindings are not verified live URLs. Installed Ask OKF admission and remote-client acceptance remain unproved.',
]


def canonical(value):
    """Explorer semantic hash convention: canonical JSON, no trailing newline."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def token_bucket(value):
    # All generated IDs and search tokens are ASCII, matching JS charCodeAt.
    h = 0x811c9dc5
    for char in value:
        h = ((h ^ ord(char)) * 0x01000193) & 0xffffffff
    return f'{h >> 24:02x}'


def occurrences(text):
    text = ''.join(x for x in unicodedata.normalize('NFKD', text) if not unicodedata.category(x).startswith('M')).lower()
    return re.findall(r'[a-z0-9]{2,}', text)


def _https(url):
    parsed = urlsplit(url)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password and not parsed.fragment


def _reference(path, raw, decoded=None):
    value = {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}
    if decoded is not None:
        value.update(encoding='gzip', decoded_bytes=len(decoded), decoded_sha256=sha(decoded))
    return value


def vendor_files(vendor_root=None):
    """Verify the exact dependency closure and upstream notices before use."""
    root = Path(vendor_root) if vendor_root is not None else VENDOR_ROOT
    raw_manifest = (root / 'manifest.json').read_bytes()
    if sha(raw_manifest) != VENDOR_MANIFEST_SHA256:
        raise ValueError('Vendored context manifest checksum mismatch')
    manifest = load_json(raw_manifest.decode())
    if (manifest.get('schema') != 'gis-ai-go.okf-plus-vendored-context.v1'
            or manifest.get('sourceRevision') != EXPLORER_REVISION
            or manifest.get('sourceRepository') != 'https://github.com/chris-page-gov/okf-explorer'):
        raise ValueError('Unsupported vendored context source')
    expected = {SCHEMA_DIR + x for x in SCHEMA_FILES} | {ENGINE_DIR + x for x in ENGINE_FILES} | {'LICENSE.md', 'LICENSE-CODE.md'}
    entries = manifest.get('files', [])
    if len(entries) != len(expected) or {x['path'] for x in entries} != expected:
        raise ValueError('Vendored dependency closure mismatch')
    files = {}
    for entry in entries:
        path = root / entry['path']
        if path.is_symlink() or not path.is_file():
            raise ValueError('Vendored source must be a regular retained file')
        raw = path.read_bytes()
        if sha(raw) != entry['sha256'] or len(raw) != entry['bytes']:
            raise ValueError('Vendored source checksum mismatch: ' + entry['path'])
        files[entry['path']] = raw
    return files


def pinned_contract(vendor_root=None):
    """Load verified pinned schemas; remote reference resolution is unavailable."""
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    raw = {p: value for p, value in vendor_files(vendor_root).items() if p.startswith(SCHEMA_DIR)}
    schemas = {Path(p).name: load_json(b.decode()) for p, b in raw.items()}
    registry = Registry().with_resources((s['$id'], Resource.from_contents(s)) for s in schemas.values())
    checks = {name: Draft202012Validator(s, registry=registry) for name, s in schemas.items()}
    checks['record'] = Draft202012Validator({'$ref': schemas['common.schema.json']['$id'] + '#/$defs/record'}, registry=registry)
    return checks, {path: sha(value) for path, value in raw.items()}


def _validate_pair(search, bundle):
    if search.get('schema') != 'gis-ai-go.okf-plus-search-index.v1' or bundle.get('schema') != 'gis-ai-go.okf-plus-bundle.v1':
        raise ValueError('Unsupported input contract')
    if not re.fullmatch('[0-9a-f]{40}', search.get('revision', '')):
        raise ValueError('Full source revision is required')
    if any(search.get(k) != bundle.get(k) for k in ('revision', 'inputDigest')):
        raise ValueError('Search/bundle snapshot identities differ')
    records = search.get('records'); semantic = bundle.get('records')
    if not isinstance(records, list) or not isinstance(semantic, list) or not records:
        raise ValueError('Non-empty record arrays required')
    by_id = {r['@id']: r for r in semantic}
    if len(by_id) != len(semantic) or len({r['id'] for r in records}) != len(records) or set(by_id) != {r['id'] for r in records}:
        raise ValueError('Duplicate or mismatched input identities')
    if bundle.get('recordCount') != len(records):
        raise ValueError('Bundle record denominator differs')
    for row in records:
        parent = by_id[row['id']]
        for key in ('title', 'description', 'type', 'sourceFamily', 'nativeIdentifier', 'sources', 'temporal', 'update', 'details', 'tags', 'resource', 'rights', 'limitations'):
            if key not in row or row[key] != parent.get(key):
                raise ValueError('Search/bundle field mismatch: ' + row['id'] + '/' + key)
        if row.get('schemaEvidence', {}) != parent.get('schemaEvidence', {}):
            raise ValueError('Schema evidence differs between inputs')
        if not isinstance(row.get('text'), str) or not isinstance(row.get('route'), str) or not re.fullmatch(r'[a-z][a-z0-9-]*(?:/[A-Za-z0-9._~-]+)+', row['route']) or '..' in row['route'].split('/'):
            raise ValueError('Invalid whole text or source route')
    return sorted(records, key=lambda r: r['id']), by_id


def _evidence(row, semantic, base_url, captured_at, outputs):
    # The body and every semantic front-matter field are retained, not only a
    # title/summary shortlist. This is a declared normalised record boundary.
    text = row['text'] + '\n\nOKF+ complete retained semantic metadata (JSON):\n' + canonical(semantic).decode() + '\n'
    if len(text) > MAX_RECORD_TEXT or len(row['title']) > 500:
        raise ValueError('Whole record exceeds the pinned engine bound; do not truncate: ' + row['id'])
    raw = text.encode(); literal_hash = sha(raw)
    path = 'passages/' + sha(row['id'].encode()) + '.txt'
    outputs[path] = raw
    passage_url = base_url + path
    provenance = []
    omissions = []
    for ordinal, source in enumerate(row['sources']):
        if (not isinstance(source, dict) or not isinstance(source.get('resource'), str)
                or not _https(source['resource']) or not re.fullmatch('[0-9a-f]{64}', str(source.get('responseSha256', '')))
                or not isinstance(source.get('retrievedAt'), str)):
            omissions.append({'sourceOrdinal': ordinal, 'reason': 'No complete captured HTTP-response binding; original source object retained in whole text.'})
            continue
        provenance.append({'url': source['resource'], 'source_sha256': source['responseSha256'],
                           'locator': source.get('sourcePointer') or source.get('normalisedPointer') or 'complete captured response',
                           'captured_at': source['retrievedAt']})
    provenance.append({'url': passage_url, 'source_sha256': literal_hash,
                       'locator': 'complete normalised metadata passage', 'captured_at': captured_at,
                       'literal_sha256': literal_hash})
    if len(provenance) > 32:
        raise ValueError('Whole provenance exceeds the pinned engine bound: ' + row['id'])
    record = {'id': row['id'], 'route': row['route'], 'label': row['title'], 'kind': 'evidence',
              'text': text, 'assertion_status': 'normalized',
              'authority': {'class': 'derived', 'label': 'GIS AI GO normalised metadata projection',
                            'source': base_url + 'projection-manifest.json'},
              'scope': 'Complete retained metadata for this source representation only; no observation, execution or reuse entitlement is established.',
              'provenance': provenance, 'rights': canonical(row['rights']).decode(), 'access': 'public',
              'review_status': semantic.get('reviewStatus', 'not-human-reviewed')}
    record['evidence_unit'] = {'schema': 'okf-evidence-unit.v1', 'kind': 'section', 'boundary_status': 'author-declared',
        'completeness': 'complete-within-declared-boundary', 'offset_unit': 'utf-8-bytes', 'joiner': '',
        'spans': [{'source_url': passage_url, 'source_sha256': literal_hash, 'extraction_url': passage_url,
                   'extraction_sha256': literal_hash, 'locator': 'complete normalised metadata passage',
                   'source_text_sha256': literal_hash, 'source_text_bytes': len(raw), 'source_start': 0,
                   'source_end': len(raw), 'unit_start': 0, 'unit_end': len(raw), 'literal_sha256': literal_hash}]}
    return record, omissions


def _card(record, row, base_url):
    # A card is navigation. Facts themselves are always in the complete passage.
    summary = 'Metadata record; open the bound complete passage for provenance, rights, temporal extent, release/update routes and limitations.'
    aliases = [row['nativeIdentifier'], row['sourceFamily']]
    aliases += [x for x in row.get('tags', []) if isinstance(x, str)]
    # Overflow is explicit in the producer manifest, never evidence truncation.
    aliases = list(dict.fromkeys(x for x in aliases if len(x) <= 500))[:100]
    return {'id': base_url + 'discovery/' + sha(record['id'].encode()), 'evidence_id': record['id'],
            'evidence_sha256': sha(canonical(record)), 'label': record['label'], 'heading_path': [row['sourceFamily']],
            'summary': summary, 'search_aliases': aliases, 'assertion_status': 'normalized',
            'authority': record['authority'], 'scope': 'Discovery only; no evidence or rights are omitted from the linked complete record.',
            'provenance': [deepcopy(record['provenance'][-1])], 'rights': record['rights'], 'access': record['access']}


def project(search, bundle, *, base_url, captured_at, representatives=2):
    """Return full corpus outputs. All inputs survive as whole evidence units."""
    if not _https(base_url) or not base_url.endswith('/') or urlsplit(base_url).query:
        raise ValueError('An explicit HTTPS candidate publication directory is required')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', captured_at):
        raise ValueError('Explicit UTC projection capture timestamp is required')
    datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
    if type(representatives) is not int or not 1 <= representatives <= 10:
        raise ValueError('Representative count must be 1..10 per family')
    rows, semantic = _validate_pair(search, bundle)
    outputs = {}; evidence = []; cards = []; source_omissions = []; concept_rows = []; edges = []; requirements = []
    snapshot = 'okf-plus-' + sha(canonical({'revision': search['revision'], 'inputDigest': search['inputDigest'],
        'searchSha256': sha(canonical(search)), 'bundleSha256': sha(canonical(bundle)), 'capturedAt': captured_at}))[:24]
    identity = {'id': 'https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/context-bundle',
                'snapshot': snapshot, 'source_url': base_url + 'manifest.json'}
    for row in rows:
        record, omissions = _evidence(row, semantic[row['id']], base_url, captured_at, outputs)
        evidence.append(record); cards.append(_card(record, row, base_url))
        if omissions:
            source_omissions.append({'id': row['id'], 'omissions': omissions})
        if row['type'] in ('Concept', 'SourceFamily'):
            concept = {k: deepcopy(v) for k, v in record.items() if k != 'evidence_unit'}
            concept.update(id=record['id'] + '#context-navigation', kind='concept')
            concept_rows.append(concept)
            edge = {'id': base_url + 'assertion/' + sha(record['id'].encode()),
                    'source': concept['id'], 'target': record['id'], 'predicate': 'http://purl.org/dc/terms/references',
                    'label': 'navigation to complete retained metadata', 'assertion_status': 'normalized',
                    'authority': record['authority'], 'scope': 'Navigation only; no statistical or legal applicability inference.',
                    'provenance': deepcopy(record['provenance'])}
            edges.append(edge)
            requirements.append({'id': base_url + 'requirement/' + sha(record['id'].encode()),
                'label': 'Complete metadata for the resolved authored concept', 'when_all': [concept['id']],
                'required': [record['id']], 'covers': [concept['id']],
                'scope': 'Only the definition/source-family metadata in this input record.',
                'limitations': ['This requirement does not establish sufficient evidence for arbitrary statistical questions.']})
    base_index = {'schema': 'okf-context-index.v1', 'bundle': identity,
                  'scope': 'Bounded authored navigation over the complete retained OS/ONS metadata corpus.',
                  'limitations': LIMITATIONS, 'records': concept_rows, 'assertions': [], 'requirements': requirements}
    if len(canonical(base_index)) > 8 * 1024 * 1024 or len(concept_rows) > 10000 or len(requirements) > 500:
        raise ValueError('Authored base exceeds pinned engine limits')
    outputs['base-index.json'] = canonical(base_index)
    record_refs = []; card_refs = []; current = []; current_cards = []; size = 0; first = 0

    def emit():
        nonlocal current, current_cards, size, first
        if not current:
            return
        ordinal = len(record_refs)
        for kind, values, schema, key, refs in (
            ('records', current, 'okf-context-records.v1', 'records', record_refs),
            ('discovery', current_cards, 'okf-discovery-cards.v1', 'cards', card_refs)):
            decoded = canonical({'schema': schema, 'first_ordinal': first, key: values})
            if len(decoded) > 4 * 1024 * 1024:
                raise ValueError('Whole record/card shard exceeds contract')
            raw = gzip.compress(decoded, compresslevel=6, mtime=0)
            path = f'{kind}/{ordinal:05d}.json.gz'; outputs[path] = raw
            reference = {**_reference(path, raw, decoded), 'first_ordinal': first, 'count': len(values)}
            if kind == 'records':
                reference.update(first_id=values[0]['id'], last_id=values[-1]['id'])
            refs.append(reference)
        first += len(current); current = []; current_cards = []; size = 0

    postings = {f'{i:02x}': defaultdict(list) for i in range(256)}; totals = Counter(source=0, discovery=0)
    for ordinal, (record, card) in enumerate(zip(evidence, cards)):
        amount = len(canonical(record)) + len(canonical(card))
        if current and (len(current) >= 64 or size + amount > SHARD_BYTES):
            emit()
        current.append(record); current_cards.append(card); size += amount
        a = occurrences(record['text']); b = occurrences('\n'.join([card['label'], *card['heading_path'], card['summary'], *card['search_aliases']]))
        ac, bc = Counter(a), Counter(b); totals.update(source=len(a), discovery=len(b))
        for token in sorted(ac.keys() | bc.keys()):
            postings[token_bucket(token)][token].append([ordinal, ac[token], len(a), bc[token], len(b)])
    emit()
    search_refs = {}
    for bucket, values in postings.items():
        decoded = canonical({'schema': 'okf-context-postings.v2', 'postings': values})
        if len(decoded) > 4 * 1024 * 1024:
            raise ValueError('Posting bucket exceeds pinned contract: ' + bucket)
        raw = gzip.compress(decoded, compresslevel=6, mtime=0); path = 'search/' + bucket + '.json.gz'
        outputs[path] = raw; search_refs[bucket] = _reference(path, raw, decoded)
    incoming = defaultdict(list); outgoing = defaultdict(list)
    for edge in edges:
        outgoing[edge['source']].append(edge); incoming[edge['target']].append(edge)
    buckets = {f'{i:02x}': [] for i in range(256)}
    for identifier in sorted([r['id'] for r in evidence + concept_rows]):
        entry = {'id': identifier}
        for direction, values in (('incoming', incoming[identifier]), ('outgoing', outgoing[identifier])):
            values = sorted(values, key=lambda x: x['id'])
            entry.update({direction: values, direction + '_count': len(values),
                          direction + '_ids_sha256': sha(canonical([x['id'] for x in values]))})
        buckets[token_bucket(identifier)].append(entry)
    adjacency = {}
    for bucket, entries in buckets.items():
        decoded = canonical({'schema': 'okf-context-adjacency-bucket.v1', 'entries': entries})
        if len(decoded) > 4 * 1024 * 1024:
            raise ValueError('Adjacency bucket exceeds pinned contract')
        raw = gzip.compress(decoded, compresslevel=6, mtime=0); path = 'relationships/' + bucket + '.json.gz'
        outputs[path] = raw; adjacency[bucket] = _reference(path, raw, decoded)
    manifest = {'schema': 'okf-context-corpus.v3', 'bundle': identity, 'scope': base_index['scope'],
                'limitations': LIMITATIONS, 'semantic_source_snapshot': snapshot,
                'base_index': _reference('base-index.json', outputs['base-index.json']),
                'counts': {'documents': len(rows), 'pages': len(rows), 'nonempty_pages': len(rows), 'empty_pages': 0, 'tokenless_pages': 0},
                'records': {'count': len(rows), 'shards': record_refs}, 'discovery': {'count': len(rows), 'shards': card_refs},
                'search': {'tokenisation': 'nfkd-lowercase-ascii-alphanumeric-min2-v1', 'bucket_algorithm': 'fnv1a32-high-byte-hex-v1',
                    'shards': search_refs, 'ranking': {'schema': 'okf-bm25.v1', 'k1': 1.2, 'b': 0.75, 'score_scale': 1000000,
                        'fields': ['source', 'discovery']}, 'total_tokens': dict(totals)},
                'relationships': {'schema': 'okf-context-adjacency.v1', 'bucket_algorithm': 'fnv1a32-high-byte-hex-v1', 'shards': adjacency},
                'extensions': {'inputRevision': search['revision'], 'inputDigest': search['inputDigest'],
                    'sourceUnit': 'one normalised metadata representation; page count is a contract unit, not a source PDF page',
                    'wholeCorpusSearchSchema': search['schema'], 'globalSourceCompleteness': 'not-established'}}
    outputs['manifest.json'] = canonical(manifest)
    representative_ids = set(); families = Counter()
    for row in rows:
        if row['type'] in ('Concept', 'SourceFamily') or families[row['sourceFamily']] < representatives:
            representative_ids.add(row['id']); families[row['sourceFamily']] += 1
    sample = {**base_index, 'records': concept_rows + [r for r in evidence if r['id'] in representative_ids], 'assertions': edges}
    if len(canonical(sample)) > 8 * 1024 * 1024 or len(sample['records']) > 10000:
        raise ValueError('Representative index exceeds pinned bounds')
    outputs['index.json'] = canonical(sample)
    review = {'schema': 'gis-ai-go.okf-plus-context-projection.v1', 'explorerRevision': EXPLORER_REVISION,
        'snapshot': snapshot, 'capturedAt': captured_at, 'sourceRevision': search['revision'], 'inputDigest': search['inputDigest'],
        'vendorManifestSha256': VENDOR_MANIFEST_SHA256,
        'inputSearchSha256': sha(canonical(search)), 'inputBundleSha256': sha(canonical(bundle)),
        'hashConvention': 'UTF-8 canonical JSON with sorted keys and no final newline',
        'wholeCorpus': {'inputRecords': len(rows), 'evidenceRecords': len(evidence), 'discoveryCards': len(cards),
                        'omittedRecordIds': [], 'omittedEvidenceFields': [], 'sourceFieldBindingOmissions': source_omissions},
        'representativeIndex': {'selectedInputIds': sorted(representative_ids),
            'omittedInputIds': [r['id'] for r in rows if r['id'] not in representative_ids],
            'selection': f'All Concept/SourceFamily records and first {representatives} canonical IDs per source family.',
            'reasonForOmission': 'Bounded evaluation index only; all these records remain in the complete v3 corpus.'},
        'semanticProjection': {'baseConcepts': len(concept_rows), 'navigationAssertions': len(edges),
            'requirements': len(requirements), 'rule': 'Only derived links from authored navigation nodes to their complete retained record.',
            'sourceAssertions': 'Retained whole in semantic JSON; not automatically promoted to traversal requirements.'},
        'discoveryCardScope': 'Navigation aliases are limited to 100 values of at most 500 characters; source fields remain whole in evidence and source postings.',
        'publication': 'candidate-not-deployed', 'installedAskOkfAdmission': 'not-established', 'limitations': LIMITATIONS,
        'outputs': [_reference(p, raw) for p, raw in sorted(outputs.items())]}
    outputs['projection-manifest.json'] = canonical(review)
    outputs['descriptor-entrypoints.json'] = canonical({'schema': 'gis-ai-go.okf-plus-context-entrypoints.v1',
        'candidatePublicationBase': base_url, 'entrypoints': {
            'context_assembly': _reference('index.json', outputs['index.json']),
            'context_corpus': _reference('manifest.json', outputs['manifest.json'])},
        'projectionManifest': _reference('projection-manifest.json', outputs['projection-manifest.json']),
        'status': 'candidate-not-deployed-or-service-admitted'})
    return outputs, review


def validate_outputs(outputs, checks):
    """Validate every record, card, posting and adjacency shard, not a sample."""
    count = 0
    for path, raw in outputs.items():
        if path.endswith('.txt') or path in ('projection-manifest.json', 'descriptor-entrypoints.json'):
            continue
        data = load_json((gzip.decompress(raw) if path.endswith('.gz') else raw).decode())
        schema = data['schema']
        if schema == 'okf-context-records.v1':
            for record in data['records']:
                checks['record'].validate(record); count += 1
        else:
            name = {'okf-context-index.v1': 'index', 'okf-context-corpus.v3': 'corpus-v3',
                    'okf-discovery-cards.v1': 'discovery-cards', 'okf-context-postings.v2': 'discovery-postings',
                    'okf-context-adjacency-bucket.v1': 'context-adjacency'}[schema]
            checks[name + '.schema.json'].validate(data)
    return {'status': 'passed-pinned-schema-validation', 'allEvidenceRecordsValidated': count}


def install(outputs, output):
    output = Path(output).resolve()
    if output.exists():
        if not (output / '.okf-plus-context').is_file() or (output / '.okf-plus-context').read_text() != MARKER:
            raise ValueError('Refusing to replace unmarked output')
        shutil.rmtree(output)
    output.mkdir(parents=True); (output / '.okf-plus-context').write_text(MARKER)
    for path, raw in outputs.items():
        target = output / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)


def verify_engine(output, cases, *, vendor_root=None, node='node'):
    """Execute pinned engine bytes against local hash-bound files; network denied."""
    runner = r'''
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [engine, root, casesFile] = process.argv.slice(2);
const {validateContextIndex} = await import(pathToFileURL(path.join(engine,'index.ts')));
const {assembleDiscoveryCorpusContext,validateDiscoveryCorpusManifest} = await import(pathToFileURL(path.join(engine,'corpusV3.ts')));
const corpus=JSON.parse(await fs.readFile(path.join(root,'manifest.json'),'utf8'));
validateDiscoveryCorpusManifest(corpus);
validateContextIndex(JSON.parse(await fs.readFile(path.join(root,'index.json'),'utf8')));
const base=corpus.bundle.source_url;
const bytes=await fs.readFile(path.join(root,'manifest.json'));
const digest=Buffer.from(await crypto.subtle.digest('SHA-256',bytes)).toString('hex');
const cases=JSON.parse(await fs.readFile(casesFile,'utf8'));const results=[];
globalThis.fetch=()=>{throw new Error('Network is forbidden in local compatibility validation');};
for(const c of cases){
 const fetcher=async(url,options)=>{
  const u=new URL(url);const prefix=new URL('.',base);if(u.origin!==prefix.origin||!u.pathname.startsWith(prefix.pathname))throw new Error('Escaped corpus binding');
  if(options.redirect!=='error'||options.credentials!=='omit')throw new Error('Unexpected transport contract');
  const relative=u.pathname.slice(prefix.pathname.length);if(relative.split('/').some(p=>p==='.'||p==='..'))throw new Error('Unsafe local path');
  const raw=await fs.readFile(path.join(root,relative));return new Response(raw,{status:200});
 };
 const result=await assembleDiscoveryCorpusContext(corpus,{index_url:base,index_sha256:digest},c.question,c.budget||{},fetcher);
 const selected=result.selected.map(x=>x.record);
 if(c.expectedId){const record=selected.find(r=>r.id===c.expectedId);if(!record)throw new Error('Expected complete record absent: '+c.expectedId);
  for(const text of c.requiredText||[])if(!record.text.includes(text))throw new Error('Required retained metadata absent');
 }
 if(c.expectOmission&&!result.budget.omissions.length&&!result.retrieval.omissions.length)throw new Error('Expected explicit budget omission');
 if(c.expectInsufficient&&result.evidence_status!=='insufficient')throw new Error('Unsupported sufficient claim');
 if(c.expectEmpty&&selected.length)throw new Error('Unknown question retained unrelated evidence');
 results.push({...(c.id?{id:c.id}:{}),question:c.question,contextId:result.context_id,evidenceStatus:result.evidence_status,selectedIds:selected.map(r=>r.id),
  candidateCount:result.retrieval.candidate_count,corpusRecords:result.retrieval.corpus_records,
  budgetOmissions:result.budget.omissions,retrievalOmissions:result.retrieval.omissions,missing:result.missing,
  fetchedFiles:result.retrieval.fetched_files,fetchedBytes:result.retrieval.fetched_bytes});
}
process.stdout.write(JSON.stringify({schema:'gis-ai-go.okf-plus-context-engine-check.v1',status:'passed',networkCalls:0,results}));
'''
    with tempfile.TemporaryDirectory(prefix='okf-context-engine-') as directory:
        temp = Path(directory); pins = {}
        files = vendor_files(vendor_root)
        for name in ENGINE_FILES:
            raw = files[ENGINE_DIR + name]; (temp / name).write_bytes(raw); pins[ENGINE_DIR + name] = sha(raw)
        (temp / 'runner.mjs').write_text(runner)
        (temp / 'cases.json').write_bytes(canonical(cases))
        result = subprocess.run([node, str(temp / 'runner.mjs'), str(temp), str(Path(output).resolve()), str(temp / 'cases.json')],
                                check=True, capture_output=True, text=True, timeout=120)
        report = load_json(result.stdout); report.update(explorerRevision=EXPLORER_REVISION,
            vendorManifestSha256=VENDOR_MANIFEST_SHA256, engineFileSha256=pins)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search-index', type=Path, required=True)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--vendor-root', type=Path, default=VENDOR_ROOT,
                        help='Exact vendored dependency directory; default is in this checkout')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--publication-base', required=True)
    parser.add_argument('--captured-at', required=True)
    parser.add_argument('--representatives-per-family', type=int, default=2)
    parser.add_argument('--all-records', action='store_true', help='Explicit whole-corpus intent; all records are always retained')
    parser.add_argument('--engine-cases', type=Path)
    args = parser.parse_args()
    search_raw, bundle_raw = args.search_index.read_bytes(), args.bundle.read_bytes()
    outputs, report = project(load_json(search_raw.decode()), load_json(bundle_raw.decode()),
        base_url=args.publication_base, captured_at=args.captured_at, representatives=args.representatives_per_family)
    checks, schemas = pinned_contract(args.vendor_root)
    validation = validate_outputs(outputs, checks)
    validation.update(explorerRevision=EXPLORER_REVISION, schemaFileSha256=schemas,
                      vendorManifestSha256=VENDOR_MANIFEST_SHA256,
                      transferredInputSha256={'search': sha(search_raw), 'bundle': sha(bundle_raw)})
    outputs['schema-validation.json'] = canonical(validation)
    install(outputs, args.output)
    if args.engine_cases:
        result = verify_engine(args.output, load_json(args.engine_cases.read_text()), vendor_root=args.vendor_root)
        (args.output / 'engine-validation.json').write_bytes(canonical(result))
    print(json.dumps({'status': 'built-and-schema-validated', 'records': report['wholeCorpus']['evidenceRecords'],
        'snapshot': report['snapshot'], 'corpusManifestSha256': sha(outputs['manifest.json']),
        'installedAskOkfAdmission': 'not-established'}))


if __name__ == '__main__':
    main()
