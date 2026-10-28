#!/usr/bin/env python3
"""Project complete OKF+ metadata into the existing Explorer's lazy Reader.

This offline producer preserves native context routes and semantic identities.
Learning is an ordered presentation of authored links, never a domain assertion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
import json
import math
from pathlib import Path
import re
import unicodedata

try:
    from .context_projection import _validate_pair, canonical, sha, token_bucket
    from .model import load_json, safe_reference
    from .explorer_facets import FACET_DEFINITIONS, facet_values, presentation_facets
    from .explorer_relationships import project_relationships
    from .explorer_resources import project_resources
except ImportError:
    from context_projection import _validate_pair, canonical, sha, token_bucket
    from model import load_json, safe_reference
    from explorer_facets import FACET_DEFINITIONS, facet_values, presentation_facets
    from explorer_relationships import project_relationships
    from explorer_resources import project_resources

MARKER = 'gis-ai-go.okf-plus-explorer-projection.v1\n'
RECORD_CHUNK_SIZE = 32
RESULT_CHUNK_SIZE = 256
MAX_SHARD_BYTES = 4 * 1024 * 1024
MAX_GRAPH_OVERVIEW_NODES = 128
STOP_WORDS = set('a an and are as at be by for from in into is it of on or the to with'.split())
LIMITATIONS = [
    'Complete retained metadata input; catalogue inclusion is not whole-product or semantic completeness.',
    'This is a dated metadata review preview, not a geographic data store or a live retrieval service.',
    'Original source, version, rights and explicit gaps remain in each complete record.',
    'Learning links are authored navigation, not supplier assertions or assessed qualifications.',
    'Lexical search is a discovery aid; a matching name does not establish identity or equivalence.',
]


def reference(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def tokens(text):
    value = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.category(c).startswith('M')).lower()
    return {token for match in re.finditer(r'[a-z0-9][a-z0-9._-]*', value)
            if len(token := match[0].strip('._-')) >= 2 and token not in STOP_WORDS}


def _validate_context(search, bundle, context):
    """Check every copied byte against the existing full projection's bindings."""
    try:
        entry = load_json(context['descriptor-entrypoints.json'].decode())
        review = load_json(context['projection-manifest.json'].decode())
        manifest = load_json(context['manifest.json'].decode())
    except (KeyError, AttributeError) as error:
        raise ValueError('Complete generated context projection is required') from error
    if (entry.get('schema') != 'gis-ai-go.okf-plus-context-entrypoints.v1'
            or review.get('inputBundleSha256') != sha(canonical(bundle))
            or review.get('inputSearchSha256') != sha(canonical(search))
            or manifest.get('schema') != 'okf-context-corpus.v3'
            or manifest.get('records', {}).get('count') != bundle['recordCount']
            or manifest.get('semantic_source_snapshot') != review.get('snapshot')):
        raise ValueError('Context projection does not bind this complete input snapshot')
    required = {row['path']: row for row in review['outputs']}
    required['projection-manifest.json'] = entry['projectionManifest']
    for path, binding in required.items():
        if (not isinstance(path, str) or not re.fullmatch(r'[A-Za-z0-9._/-]+', path)
                or any(p in ('', '.', '..') for p in path.split('/'))):
            raise ValueError('Unsafe generated context path')
        raw = context.get(path)
        if raw is None or len(raw) != binding['bytes'] or sha(raw) != binding['sha256']:
            raise ValueError('Context byte binding mismatch: ' + path)
    for name, binding in entry['entrypoints'].items():
        if name not in ('context_assembly', 'context_corpus') or binding != reference(binding['path'], context[binding['path']]):
            raise ValueError('Context entrypoint binding mismatch')
    # Copy only the exact verified closure, not arbitrary sibling files.
    return {path: context[path] for path in required}, manifest['semantic_source_snapshot'], entry


def learning_presentation(rows, semantic):
    from jsonschema import Draft202012Validator
    schema = load_json((Path(__file__).resolve().parents[2] / 'okf-plus/schemas/learning-path.schema.json').read_text())
    validator = Draft202012Validator(schema)
    routes = {row['id']: row['route'] for row in rows}
    paths = []
    for row in rows:
        authored = semantic[row['id']].get('details', {}).get('learningPath')
        if authored is None:
            continue
        validator.validate(authored)
        if authored.get('schema') != 'gis-ai-go.okf-plus-learning-path.v1':
            raise ValueError('Unsupported authored learning path')
        path_id = authored.get('id')
        if not isinstance(path_id, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,79}', path_id):
            raise ValueError('Invalid learning path ID')
        steps = []
        seen = set()
        for step in authored.get('steps', []):
            identifier = step.get('recordId')
            if identifier not in routes:
                raise ValueError('Learning step references an absent record: ' + str(identifier))
            if identifier in seen:
                raise ValueError('Duplicate route within learning path')
            seen.add(identifier)
            target = semantic[identifier]
            source_urls = {target['resource'], *(source['resource'] for source in target['sources'])}
            for source in step['sourceRefs']:
                safe_reference(source)
                if source not in source_urls:
                    raise ValueError('Learning source does not belong to its referenced record')
            for key in ('title', 'outcome'):
                if not isinstance(step.get(key), str) or not step[key].strip():
                    raise ValueError('Learning step requires ' + key)
            result = {key: deepcopy(step[key]) for key in ('title', 'outcome', 'practice', 'minutes') if key in step}
            if 'minutes' in result and (type(result['minutes']) is not int or not 1 <= result['minutes'] <= 480):
                raise ValueError('Learning duration outside supported bounds')
            result['route'] = routes[identifier]
            evidence_ids = step.get('conceptRefs', [])
            if any(identifier not in routes for identifier in evidence_ids):
                raise ValueError('Learning concept references an absent record')
            result['evidence_routes'] = list(dict.fromkeys(routes[identifier] for identifier in evidence_ids))
            steps.append(result)
        if not 1 <= len(steps) <= 24:
            raise ValueError('Learning path must contain 1..24 steps')
        for prerequisite in authored.get('prerequisiteConcepts', []):
            if prerequisite.get('recordId') not in routes:
                raise ValueError('Learning prerequisite concept is absent')
        path = {'id': path_id, 'title': authored.get('title', row['title']),
                'description': authored.get('description', row['description']),
                'prerequisites': authored.get('prerequisites', []), 'steps': steps}
        paths.append(path)
    ids = {path['id'] for path in paths}
    if len(ids) != len(paths) or len(paths) > 12:
        raise ValueError('Learning path IDs must be unique; maximum 12 paths')
    for path in paths:
        if any(prerequisite not in ids or prerequisite == path['id'] for prerequisite in path['prerequisites']):
            raise ValueError('Unknown or self-referencing learning prerequisite')
    by_id = {path['id']: path for path in paths}
    def visit(identifier, ancestors):
        if identifier in ancestors:
            raise ValueError('Cyclic learning prerequisites')
        for parent in by_id[identifier]['prerequisites']:
            visit(parent, ancestors | {identifier})
    for identifier in by_id:
        visit(identifier, set())
    return {'schema': 'okf-large-learning-presentation.v1',
            'title': 'Learn to use OS and ONS evidence',
            'introduction': 'Choose a question, read the linked source context and record what remains unknown. Practice progress is not assessment.',
            'paths': paths} if paths else None


def _search(rows, datasets, outputs, snapshot, record_facets):
    """Existing bounded static-search v1: lexical metadata, no semantic inference."""
    postings = defaultdict(list)
    docs = []
    facets = {definition['key']: defaultdict(list) for definition in FACET_DEFINITIONS}
    sort_values = []
    for ordinal, (row, dataset) in enumerate(zip(rows, datasets)):
        name = dataset['name']
        docs.append({'ordinal': ordinal, 'name': name, 'route': row['route'], 'title': row['title'],
                     'publisher': dataset['publisher'], 'publisher_title': dataset['publisher_title'],
                     'source_publishers': dataset['source_publishers'],
                     'resource_count': dataset['resource_count'], 'formats': [], 'tags': row['tags'],
                     'notes': row['description'], 'record_type': row['type'], 'record_id': row['id'],
                     'native_id': row['nativeIdentifier'], 'open': row['route'],
                     **{key: values for key, values in record_facets[row['id']].items()
                        if key not in ('record_type', 'tag', 'source_publisher')}})
        fields = [(row['title'], 8, 1), (row['description'], 4, 2),
                  (' '.join([row['nativeIdentifier'], *row['tags']]), 4, 4),
                  (row['text'] + '\n' + canonical(row['details']).decode(), 1, 8)]
        scores = {}
        for text, weight, mask in fields:
            for token in tokens(text):
                old_weight, old_mask = scores.get(token, (0, 0))
                scores[token] = (old_weight + weight, old_mask | mask)
        for token, (weight, mask) in scores.items():
            postings[token].append([ordinal, weight, mask])
        for key, values in record_facets[row['id']].items():
            for value in values:
                facets[key][value].append(ordinal)
        sort_values.append(['', row['title'], None])
    search_paths = []

    def put(path, value):
        raw = canonical(value)
        if len(raw) > MAX_SHARD_BYTES:
            raise ValueError('Search shard exceeds bounded loading limit: ' + path)
        outputs[path] = raw
        search_paths.append(path)
        return path

    result_paths = [put(f'search/results/{offset // RESULT_CHUNK_SIZE:05d}.json', docs[offset:offset + RESULT_CHUNK_SIZE])
                    for offset in range(0, len(docs), RESULT_CHUNK_SIZE)]
    by_prefix = defaultdict(dict)
    for token, values in sorted(postings.items()):
        prefix = re.sub('[^a-z0-9]', '', token)[:2] or '_'
        by_prefix[prefix][token] = values
    lexicon_paths = {}; posting_paths = []; prefix_paths = {}
    for prefix, values in sorted(by_prefix.items()):
        # Partition by complete token to keep every request finite without
        # silently dropping very common terms or trailing records.
        partitions = []; current = {}; size = 16
        for token, values_for_token in values.items():
            amount = len(canonical({token: values_for_token})) + 1
            if amount > MAX_SHARD_BYTES - 16:
                raise ValueError('One complete token exceeds the search shard budget')
            if current and size + amount > MAX_SHARD_BYTES:
                partitions.append(current); current = {}; size = 16
            current[token] = values_for_token; size += amount
        if current:
            partitions.append(current)
        lexicon = []; suggestions = defaultdict(list)
        for number, partition in enumerate(partitions):
            path = put(f'search/postings/{prefix}-{number:05d}.json', {'tokens': partition})
            posting_paths.append(path)
            for token, values_for_token in partition.items():
                df = len(values_for_token)
                lexicon.append({'token': token, 'df': df, 'postings': path})
                for length in range(3, min(8, len(token)) + 1):
                    suggestions[token[:length]].append({'token': token, 'df': df})
        lexicon_paths[prefix] = put(f'search/lexicon/{prefix}.json', lexicon)
        prefix_paths[prefix] = put(f'search/prefixes/{prefix}.json', {
            key: sorted(value, key=lambda item: (-item['df'], item['token']))[:16]
            for key, value in suggestions.items()})
    facet_path = put('search/facets.json', facets)
    filter_paths = {key: put(f'search/filter-{key}.json', {'schema': 'okf-static-filter-postings.v1', 'key': key, 'values': values})
                    for key, values in facets.items()}
    sort_path = put('search/sort.json', sort_values)
    # The current worker does not hydrate doc_map. Keep its full mapping in the
    # existing partitioned contract for other consumers, within finite files.
    doc_map = [put(f'search/doc-map/{offset // 1000:05d}.json',
                   {str(i): rows[i]['route'] for i in range(offset, min(offset + 1000, len(rows)))})
               for offset in range(0, len(rows), 1000)]
    shards = {'search': [{**reference(path, outputs[path]), 'snapshot': snapshot} for path in sorted(search_paths)]}
    outputs['search/shard-metadata.json'] = canonical({'snapshot': snapshot, 'shards': shards})
    manifest = {'schema': 'okf-static-search.v1', 'snapshot': snapshot,
        'token_min_length': 2, 'prefix_min_length': 3, 'lexicon_shard_length': 2,
        'result_limit': 100, 'result_doc_chunk_size': RESULT_CHUNK_SIZE,
        'weights': {'title': 8, 'description': 4, 'native': 4, 'source_text': 1},
        'field_masks': {'title': 1, 'description': 2, 'native': 4, 'source_text': 8},
        'counts': {'documents': len(rows), 'tokens': len(postings), 'postings_shards': len(posting_paths),
                   'max_postings_per_token': max(map(len, postings.values()), default=1)},
        'shard_metadata': 'search/shard-metadata.json',
        'shard_manifest_sha256': sha(canonical(shards) + b'\n'),
        'doc_map_partitioning': {'schema': 'okf-search-doc-map-partitioning.v1',
            'algorithm': 'contiguous-ordinal-max-count-v1', 'max_records': 1000,
            'max_bytes': 5 * 1024 * 1024, 'partition_index_width': 5},
        'entrypoints': {'lexicon': lexicon_paths, 'prefixes': prefix_paths, 'postings': posting_paths,
            'result_docs': result_paths, 'facets': facet_path, 'filter_postings': filter_paths,
            'sort_values': sort_path, 'doc_map': doc_map}}
    outputs['search/manifest.json'] = canonical(manifest)
    return {key: [{'value': value, 'count': len(indices)} for value, indices in sorted(values.items())]
            for key, values in facets.items()}


def _discovery_indexes(rows, datasets, facets, record_facets, resources, publishers,
                       relationships, outputs, snapshot, captured_at):
    """Expose bounded navigation without loading every complete Reader record."""
    def put(path, value):
        raw = canonical(value)
        if len(raw) > MAX_SHARD_BYTES:
            raise ValueError('Discovery shard exceeds bounded loading limit: ' + path)
        outputs[path] = raw
        return reference(path, raw)

    chunks = {'resources': []}
    by_dataset = defaultdict(list)
    for resource in resources:
        by_dataset[resource['dataset']].append(resource)
    resource_buckets = {f'{number:02x}': {} for number in range(256)}
    for offset in range(0, len(datasets), RECORD_CHUNK_SIZE):
        group = datasets[offset:offset + RECORD_CHUNK_SIZE]
        selected = []; locators = {}
        for dataset in group:
            values = by_dataset[dataset['name']]
            if len(values) > 256:
                raise ValueError('One record exceeds the bounded source-reference count')
            locators[dataset['route']] = list(range(len(selected), len(selected) + len(values)))
            selected.extend(values)
        if len(selected) > 1024:
            raise ValueError('Shared source-reference chunk exceeds the bounded row count')
        ref = put(f'resources/{offset // RECORD_CHUNK_SIZE:05d}.json', selected) if selected else None
        if ref and ref['bytes'] > 2 * 1024 * 1024:
            raise ValueError('Shared source-reference chunk exceeds the targeted byte budget')
        if ref:
            chunks['resources'].append(ref)
        for dataset in group:
            indices = locators[dataset['route']]
            resource_buckets[token_bucket(dataset['route'])][dataset['route']] = {
                'dataset': dataset['name'], 'count': len(indices),
                'chunks': [{**ref, 'rows': indices}] if indices else []}
    resource_bucket_refs = {bucket: put('resources/locator/' + bucket + '.json', values)
                            for bucket, values in resource_buckets.items() if values}
    if any(ref['bytes'] > 1024 * 1024 for ref in resource_bucket_refs.values()):
        raise ValueError('Source-reference locator bucket exceeds the targeted byte budget')
    resource_ref = put('record-resources.json', {'schema': 'okf-record-resource-index.v1',
        'snapshot': snapshot, 'algorithm': 'fnv1a32-prefix-2', 'buckets': resource_bucket_refs})
    if resource_ref['bytes'] > 256 * 1024:
        raise ValueError('Source-reference locator manifest exceeds its byte budget')
    for name, values in (('publishers', publishers), ('relationships', relationships)):
        chunks[name] = [put(f'{name}/{offset // 128:05d}.json', values[offset:offset + 128])
                        for offset in range(0, len(values), 128)]
    adjacency = {f'{number:02x}': defaultdict(list) for number in range(256)}
    connected = Counter()
    for relationship in relationships:
        for route in sorted({relationship['source'], relationship['target']}):
            adjacency[token_bucket(route)][route].append(relationship)
            connected[route] += 1
    bucket_refs = {bucket: put('relationships/adjacency/' + bucket + '.json', values)
                   for bucket, values in adjacency.items() if values}
    put('relationship-adjacency.json', {'schema': 'okf-relationship-adjacency.v1',
        'algorithm': 'fnv1a32-prefix-2', 'snapshot': snapshot, 'routes': len(connected),
        'relationships': len(relationships), 'buckets': bucket_refs})

    by_route = {row['route']: row for row in rows}
    facet_coverage = {}
    analyses = []
    total = len(rows)
    for definition in FACET_DEFINITIONS:
        key = definition['key']; values = facets[key]
        covered = sum(bool(record_facets[row['id']][key]) for row in rows)
        memberships = sum(item['count'] for item in values)
        facet_coverage[key] = {'sourcePaths': definition['source_paths'],
            'nonemptyRecords': covered, 'distinctValues': len(values), 'memberships': memberships,
            'missingRecords': total - covered}
        analyses.append({'key': key, 'label': definition['label'],
            'description': 'Exact retained metadata values from ' + ', '.join(definition['source_paths']) + '.',
            'coverage': covered / total if total else 0, 'cardinality': len(values),
            'top_share': max((item['count'] / total for item in values), default=0),
            'entropy': -sum((item['count'] / memberships) * math.log2(item['count'] / memberships) for item in values) if memberships else 0,
            'expected_reduction': 1 - sum(item['count'] ** 2 for item in values) / (memberships * total) if memberships and total else 0,
            'recommended_control': 'search' if len(values) > 40 else 'distribution',
            'recommendation': 'primary' if definition['shown'] else 'advanced',
            'default_hidden': not definition['shown'], 'values': values})
    # These labels cover this bounded graph overview only. Do not advertise the
    # optional global endpoint-label registry with partial route coverage: that
    # contract would mark all other record, citation and facet labels missing.
    selected_routes = {route for route, _ in connected.most_common(MAX_GRAPH_OVERVIEW_NODES)}
    nodes = [{'id': route, 'route': route, 'label': by_route[route]['title'],
              'type': by_route[route]['type'], 'count': connected[route]} for route in sorted(selected_routes)]
    edge_counts = Counter(row['kind'] for row in relationships)
    top_resources = sorted(datasets, key=lambda dataset: (-dataset['resource_count'], dataset['route']))[:8]
    analysis = {'schema': 'okf-explorer-analysis.v1', 'snapshot': snapshot, 'generated_at': captured_at,
        'summary': {'title': 'OS and ONS geospatial knowledge', 'record_count': total,
            'resource_count': len(resources), 'relationship_count': len(relationships),
            'description': 'Browse retained metadata, its source references and explicit typed links between records.',
            'notices': ['Relationships count explicit links between retained records, not every external or nested RDF reference.',
                        'Source references are record-to-URL citations, not a claim of downloadable data or access permission.',
                        f'The graph overview shows up to {MAX_GRAPH_OVERVIEW_NODES} connected records; select a record for its exact incident links.']},
        'display': {'facets': {'order': [definition['key'] for definition in FACET_DEFINITIONS],
                             'default_mode': 'suggested'}},
        'facet_analysis': analyses,
        'graph_overview': {'nodes': nodes, 'edges': [relationship for relationship in relationships
            if relationship['source'] in selected_routes and relationship['target'] in selected_routes]},
        'relationship_overview': {
            'types': [{'kind': kind, 'count': count, 'samples': [
                {key: edge[key] for key in ('source', 'target', 'label')}
                for edge in relationships if edge['kind'] == kind][:3]} for kind, count in sorted(edge_counts.items())],
            'top_connected': [{'id': route, 'label': by_route[route]['title'], 'type': by_route[route]['type'],
                               'count': count} for route, count in connected.most_common(12)]},
        'resource_overview': {'total_resources': len(resources),
            'distributions': {'resource_type': [{'value': 'source-reference', 'count': len(resources)}] if resources else []},
            'high_resource_datasets': [{'route': dataset['route'], 'label': dataset['title'],
                'publisher': dataset['publisher'], 'count': dataset['resource_count'],
                'samples': [{'id': resource['id'], 'label': resource['name'], 'host': resource['host']}
                            for resource in by_dataset[dataset['name']][:3]]} for dataset in top_resources if dataset['resource_count']]}}
    analysis_ref = put('analysis-overview.json', analysis)
    return chunks, analysis_ref, facet_coverage, resource_ref


def project(search, bundle, context, *, captured_at):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', captured_at):
        raise ValueError('Explicit UTC capture timestamp is required')
    datetime.fromisoformat(captured_at.replace('Z', '+00:00'))
    rows, semantic = _validate_pair(search, bundle)
    if len({row['route'] for row in rows}) != len(rows):
        raise ValueError('Every semantic record requires a unique Reader route')
    context, snapshot, entry = _validate_context(search, bundle, context)
    outputs = {'context/' + path: raw for path, raw in context.items()}
    record_facets = {row['id']: facet_values(semantic[row['id']]) for row in rows}
    resources, publishers, record_resources, resource_coverage = project_resources(rows, semantic)
    relationships, relationship_coverage = project_relationships(
        rows, semantic, captured_at=captured_at, source_revision=bundle['revision'])
    datasets = []
    for row in rows:
        parent = semantic[row['id']]
        datasets.append({'id': row['id'], 'name': row['route'].removeprefix('records/'),
            'route': row['route'], 'title': row['title'], 'notes': row['description'],
            **{key: values for key, values in record_facets[row['id']].items()
               if key not in ('record_type', 'tag', 'source_publisher')},
            **record_resources[row['id']],
            'record_type': row['type'], 'tags': row['tags'],
            'narrative': {'title': row['title'], 'body': row['text'],
                          'source_url': 'https://github.com/chris-page-gov/gis-ai-go/blob/' + bundle['revision'] + '/okf-plus/' + row['route']},
            'url': row['resource'], 'source_api_url': row['resource'],
            'provenance': {'sources': deepcopy(row['sources']), 'source_revision': bundle['revision'],
                           'source_file': 'okf-plus/' + row['route']},
            'okf_plus': {'schema': 'gis-ai-go.okf-plus-record-context.v1', 'record_id': row['id'],
                         'source_revision': bundle['revision'], 'metadata': deepcopy(parent)}})
    chunks = []; buckets = {f'{number:02x}': {} for number in range(256)}
    for offset in range(0, len(datasets), RECORD_CHUNK_SIZE):
        chunk_index = offset // RECORD_CHUNK_SIZE
        path = f'records/{chunk_index:05d}.json'
        raw = canonical(datasets[offset:offset + RECORD_CHUNK_SIZE])
        if len(raw) > MAX_SHARD_BYTES:
            raise ValueError('Complete Reader shard exceeds bounded loading limit; do not truncate')
        outputs[path] = raw; chunks.append(reference(path, raw))
        for row_index, dataset in enumerate(datasets[offset:offset + RECORD_CHUNK_SIZE]):
            buckets[token_bucket(dataset['route'])][dataset['route']] = [chunk_index, row_index]
    bucket_refs = {}
    for bucket, values in buckets.items():
        path = 'locator/' + bucket + '.json'; raw = canonical(values)
        outputs[path] = raw; bucket_refs[bucket] = reference(path, raw)
    outputs['record-locator.json'] = canonical({'schema': 'okf-record-locator-sharded.v1',
        'algorithm': 'fnv1a32-prefix-2', 'snapshot': snapshot, 'records': len(rows),
        'chunk_size': RECORD_CHUNK_SIZE, 'record_chunks': chunks, 'buckets': bucket_refs, 'bucket_count': 256})
    facets = _search(rows, datasets, outputs, snapshot, record_facets)
    outputs['facets.json'] = canonical(facets)
    discovery_chunks, analysis_ref, facet_coverage, resource_ref = _discovery_indexes(
        rows, datasets, facets, record_facets, resources, publishers, relationships,
        outputs, snapshot, captured_at)
    counts = {'datasets': len(rows), 'records': len(rows), 'resources': len(resources),
              'publishers': len(publishers), 'relationships': len(relationships)}
    coverage = {'schema': 'gis-ai-go.okf-plus-explorer-discovery-coverage.v1',
        'snapshot': snapshot, 'sourceRevision': bundle['revision'], 'inputDigest': bundle['inputDigest'],
        'records': len(rows), 'facets': facet_coverage, 'resources': resource_coverage,
        'relationships': relationship_coverage,
        'limitations': ['Facets are named, source-backed metadata dimensions; absent values are not invented.',
                        'Typed graph rows cover explicit retained-record associations, not all RDF or geographic feature relationships.']}
    outputs['discovery-coverage.json'] = canonical(coverage)
    recent = [row for row in rows if row['type'] in ('Concept', 'SourceFamily')][:12]
    outputs['overview.json'] = canonical({'schema': 'okf-explorer-overview.v1',
        'title': 'OS and ONS geospatial knowledge', 'generated_at': captured_at, 'counts': counts,
        'notices': LIMITATIONS, 'facet_previews': facets,
        'recent_datasets': [{'ordinal': rows.index(row), 'name': row['route'].removeprefix('records/'),
            'route': row['route'], 'title': row['title'],
            **{key: record_resources[row['id']][key] for key in ('publisher', 'publisher_title', 'source_publishers', 'resource_count')},
            'formats': [],
            'tags': row['tags'], 'notes': row['description'], 'open': row['route']} for row in recent]})
    locator_ref = reference('record-locator.json', outputs['record-locator.json'])
    outputs['data-manifest.json'] = canonical({'title': 'OS and ONS geospatial knowledge',
        'generated_at': captured_at, 'snapshot': snapshot, 'counts': counts,
        'indexes': {'overview': 'overview.json', 'search': 'search/manifest.json',
                    'facets': 'facets.json', 'record_locator': locator_ref,
                    'analysis': analysis_ref['path'],
                    'record_resources': resource_ref,
                    'relationship_adjacency': 'relationship-adjacency.json'},
        'chunks': {'datasets': chunks, **discovery_chunks},
        'shards': {'datasets': chunks, **discovery_chunks}})
    entrypoints = {'data_manifest': 'data-manifest.json', 'overview_index': 'overview.json',
                   'search_manifest': 'search/manifest.json', 'record_locator': locator_ref,
                   'analysis_overview': analysis_ref['path'],
                   'record_resources': resource_ref,
                   'relationship_adjacency': 'relationship-adjacency.json'}
    integrity = {key: reference(path, outputs[path]) for key, path in entrypoints.items() if isinstance(path, str)}
    for name, binding in entry['entrypoints'].items():
        entrypoints[name] = {**binding, 'path': 'context/' + binding['path']}
    descriptor = {'schema': 'okf-explorer-large-corpus.v1', 'kind': 'okf-large-corpus',
        'title': 'OS and ONS geospatial knowledge',
        'description': 'Source-linked OKF+ metadata and unassessed learning paths. Open a record for its complete context and qualifications.',
        'generated_at': captured_at, 'snapshot': snapshot, 'version': bundle['revision'], 'status': 'draft',
        'counts': counts, 'entrypoints': entrypoints, 'entrypoint_integrity': integrity,
        'vocabulary': {'record_singular': 'metadata record', 'record_plural': 'metadata records',
                       'resource_singular': 'source reference', 'resource_plural': 'source references',
                       'resource_stack_label': 'Source references',
                       'search_placeholder': 'Search retained metadata, fields and explanations'},
        'source': {'repository': 'https://github.com/chris-page-gov/gis-ai-go',
                   'revision': bundle['revision'], 'inputDigest': bundle['inputDigest']},
        'extensions': {'gis_ai_go': {'limitations': LIMITATIONS, 'globalSourceCompleteness': 'not-established',
                         'discoveryCoverage': reference('discovery-coverage.json', outputs['discovery-coverage.json'])},
                       'okf-explorer-presentation.v1': {'schema': 'okf-explorer-presentation.v1',
                         'status': 'stable', 'snapshot': snapshot, 'defaults': {'facet_mode': 'suggested'},
                         'facets': presentation_facets()}}}
    learning = learning_presentation(rows, semantic)
    if learning:
        descriptor['learning_presentation'] = learning
    outputs['okf-explorer.json'] = canonical(descriptor)
    outputs['route-map.json'] = canonical({'schema': 'gis-ai-go.okf-plus-reader-routes.v1',
        'snapshot': snapshot, 'records': [{'id': row['id'], 'route': row['route']} for row in rows]})
    report = {'schema': 'gis-ai-go.okf-plus-explorer-projection.v1', 'sourceRevision': bundle['revision'],
        'inputDigest': bundle['inputDigest'], 'snapshot': snapshot, 'capturedAt': captured_at,
        'inputRecords': len(rows), 'readerRecords': len(datasets), 'omittedRecordIds': [],
        'recordChunkSize': RECORD_CHUNK_SIZE, 'maximumRecordShardBytes': max(len(outputs[row['path']]) for row in chunks),
        'learningPaths': len(learning['paths']) if learning else 0, 'status': 'candidate-not-deployed',
        'discovery': {'facets': len(facets), 'resources': len(resources), 'publishers': len(publishers),
                      'relationships': len(relationships), 'coverage': reference('discovery-coverage.json', outputs['discovery-coverage.json'])},
        'outputs': [reference(path, raw) for path, raw in sorted(outputs.items())]}
    outputs['projection-manifest.json'] = canonical(report)
    return outputs, report


def install(outputs, directory):
    directory = Path(directory)
    if directory.exists():
        raise ValueError('Refusing to replace an existing output directory; choose a new candidate')
    directory.mkdir(parents=True)
    (directory / '.okf-plus-explorer').write_text(MARKER)
    for path, raw in outputs.items():
        target = directory / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search-index', type=Path, required=True)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--context-directory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--captured-at', required=True)
    args = parser.parse_args()
    if args.context_directory.is_symlink():
        raise ValueError('Context directory must be a retained regular directory')
    root = args.context_directory.resolve()
    context = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('Symlink context input forbidden')
        if path.is_file() and not path.name.startswith('.'):
            context[path.relative_to(root).as_posix()] = path.read_bytes()
    outputs, report = project(load_json(args.search_index.read_text()), load_json(args.bundle.read_text()),
                              context, captured_at=args.captured_at)
    install(outputs, args.output)
    print(json.dumps({key: report[key] for key in ('snapshot', 'readerRecords', 'learningPaths', 'maximumRecordShardBytes')}))


if __name__ == '__main__':
    main()
