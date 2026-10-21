"""Offline discovery of exact retained lexical forms, codes and field names.

This projection preserves source positions and typed native values. Search
normalisation is a navigation aid, never an equivalence or execution assertion.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import re
import stat
import unicodedata

try:
    from .model import CTX, PREFIXES, canonical, digest, load_json, safe_reference
    from .vocabulary_usage import expanded_iri
    from .vocabulary_inventory import schema_constraints, schema_roots
except ImportError:
    from model import CTX, PREFIXES, canonical, digest, load_json, safe_reference
    from vocabulary_usage import expanded_iri
    from vocabulary_inventory import schema_constraints, schema_roots

SCHEMA = 'gis-ai-go.okf-plus-term-discovery.v1'
LABELS = {PREFIXES['skos'] + name: kind for name, kind in (
    ('prefLabel', 'preferred-label'), ('altLabel', 'alternative-label'),
    ('hiddenLabel', 'hidden-label'), ('notation', 'notation'))}
LABELS[PREFIXES['rdfs'] + 'label'] = 'node-label'
MAX_RECORDS = 100_000
MAX_FORMS = 1_000_000
MAX_INPUT_BYTES = 256 * 1024 * 1024


def pointer_part(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def normalise(value):
    """Case/Unicode search view only; source spelling and types stay intact."""
    return unicodedata.normalize('NFKC', value).casefold().strip()


def display(value):
    return value if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _forms(row):
    forms = []

    def add(value, kind, pointer, node_id=None, language=None, datatype=None):
        forms.append({'kind': kind, 'value': value, 'display': display(value),
                      'pointer': pointer, 'nodeId': node_id or row['@id'],
                      'language': language, 'datatype': datatype})

    def labels(value, kind, pointer, node_id):
        if isinstance(value, list):
            for i, item in enumerate(value):
                labels(item, kind, pointer + '/' + str(i), node_id)
        elif isinstance(value, dict) and '@value' in value:
            if value.get('@type') == '@json':
                raise ValueError('A lexical label cannot be opaque JSON')
            add(value['@value'], kind, pointer + '/@value', node_id,
                value.get('@language'), value.get('@type'))
        elif isinstance(value, dict) and set(value) in ({'@list'}, {'@set'}):
            key = next(iter(value))
            labels(value[key], kind, pointer + '/' + key, node_id)
        elif isinstance(value, (str, int, float, bool)) or value is None:
            add(value, kind, pointer, node_id)
        else:
            raise ValueError('Unsupported label representation at ' + pointer)

    def semantic(value, pointer='', node_id=None):
        if isinstance(value, list):
            for i, child in enumerate(value):
                semantic(child, pointer + '/' + str(i), node_id)
            return
        if not isinstance(value, dict) or '@value' in value or value.get('@type') == '@json':
            return
        node_id = value.get('@id', node_id or row['@id'])
        for key, child in value.items():
            path = pointer + '/' + pointer_part(key)
            iri = expanded_iri(key, alias=True)
            if iri in LABELS:
                labels(child, LABELS[iri], path, node_id)
                continue
            definition = CTX.get(key)
            if isinstance(definition, dict) and definition.get('@type') == '@json':
                continue
            if key != '@context':
                semantic(child, path, node_id)

    def enums(value, pointer, node_id):
        for path, keyword, native in schema_constraints(value, pointer):
            if keyword == 'enum':
                for i, item in enumerate(native):
                    add(item, 'native-enum', path + '/' + str(i), node_id)
            else:
                add(native, 'native-constant', path, node_id)

    def native_tables(value, pointer):
        if isinstance(value, dict):
            if value.get('encoding') == 'os-documentation-native-label-table.v1':
                if value.get('columns') != ['sourceRow', 'nativeText'] or not isinstance(value.get('rows'), list):
                    raise ValueError('Unsupported native label table')
                for i, cells in enumerate(value['rows']):
                    if (not isinstance(cells, list) or len(cells) != 2
                            or type(cells[0]) is not int or cells[0] < 0
                            or not isinstance(cells[1], str)):
                        raise ValueError('Invalid native label row')
                    add(cells[1], 'native-table-label', pointer + '/rows/' + str(i) + '/1')
                return
            for key, child in value.items():
                native_tables(child, pointer + '/' + pointer_part(key))
        elif isinstance(value, list):
            for i, child in enumerate(value):
                native_tables(child, pointer + '/' + str(i))

    for key, kind in (('@id', 'record-iri'), ('title', 'record-title'),
                      ('nativeIdentifier', 'native-identifier')):
        if key in row:
            add(row[key], kind, '/' + key)
    semantic(row)
    for i, form in enumerate(row.get('okfp:lexicalForm', [])):
        if (not isinstance(form, dict) or not isinstance(form.get('okfp:formKind'), str)
                or not form['okfp:formKind']
                or form.get('okfp:authority') not in ('source-stated', 'project-search-variant')):
            raise ValueError('Lexical forms require a kind, authority and source')
        sources = form.get('prov:wasDerivedFrom')
        sources = sources if isinstance(sources, list) else [sources]
        if not sources or any(not isinstance(s, dict) or not isinstance(s.get('@id'), str) for s in sources):
            raise ValueError('Lexical forms require source references')
        for source in sources:
            safe_reference(source['@id'])
        value = form.get('rdf:value')
        if not isinstance(value, dict) or not isinstance(value.get('@value'), str):
            raise ValueError('Lexical forms require a literal string value')
        labels(value, 'qualified-lexical-form', '/okfp:lexicalForm/' + str(i) + '/rdf:value', row['@id'])
        forms[-1]['formKind'] = form['okfp:formKind']
        forms[-1]['authority'] = form['okfp:authority']
        forms[-1]['sources'] = [source['@id'] for source in sources]
        forms[-1]['formId'] = form.get('@id')
    for i, field in enumerate(row.get('okfp:field', [])):
        pointer = '/okfp:field/' + str(i)
        node_id = field['@id']
        add(node_id, 'field-iri', pointer + '/@id', node_id)
        if 'dcterms:identifier' in field:
            add(field['dcterms:identifier'], 'native-field-name',
                pointer + '/dcterms:identifier', node_id)
        definition = field.get('okfp:schemaDefinition', {})
        if definition.get('@type') == '@json' and '@value' in definition:
            enums(definition['@value'], pointer + '/okfp:schemaDefinition/@value', node_id)
    # Retained schema/queryable and API contract contexts are separately positioned.
    # They may repeat field-node constraints; occurrences are never deduplicated.
    for pointer, schema in schema_roots(row):
        enums(schema, pointer, row['@id'])
    native_tables(row.get('details', {}), '/details')
    # Deliberately keep duplicate labels, table positions, nulls and whitespace.
    return forms


def build_discovery(records, usage, revision, input_digest):
    if len(records) > MAX_RECORDS:
        raise ValueError('Too many records for term discovery')
    entries, seen, counts = [], set(), Counter()
    matches = defaultdict(set)
    for row in sorted(records, key=lambda item: item['@id']):
        if row['@id'] in seen:
            raise ValueError('Duplicate term-discovery record')
        seen.add(row['@id'])
        forms = _forms(row)
        counts.update(form['kind'] for form in forms)
        if sum(counts.values()) > MAX_FORMS:
            raise ValueError('Too many lexical forms')
        for form in forms:
            matches[normalise(form['display'])].add(form['nodeId'])
        entries.append({'recordId': row['@id'], 'recordSha256': digest(row),
                        'title': row.get('title', ''), 'sourceFamily': row.get('sourceFamily'),
                        'definition': row.get('description', ''), 'resource': row.get('resource'),
                        'assertionStatus': row.get('assertionStatus'), 'reviewStatus': row.get('reviewStatus'),
                        'lifecycleStatus': row.get('status'), 'sources': row.get('sources', []),
                        'temporal': row.get('temporal'), 'update': row.get('update'), 'forms': forms})
    terms = []
    for namespace in usage.get('namespaces', []):
        for term in namespace['terms']:
            terms.append({**term, 'compactIri': namespace['prefix'] + ':' + term['iri'][len(namespace['namespace']):],
                          'definitionSource': namespace.get('source'),
                          'mappingReview': namespace.get('mappingReview')})
    return {'schema': SCHEMA, 'revision': revision, 'inputDigest': input_digest,
            'recordCount': len(entries), 'formCount': sum(counts.values()),
            'byFormKind': dict(sorted(counts.items())), 'records': entries,
            'semanticTerms': terms,
            'ambiguousForms': [{'normalisedForm': key, 'nodeIds': sorted(ids)}
                               for key, ids in sorted(matches.items()) if key and len(ids) > 1],
            'coverage': {'retainedRecordTraversal': 'complete', 'globalVocabularyCompleteness': 'not-established',
                         'allPossibleTermForms': 'not-established',
                         'normalisation': 'NFKC, casefold and surrounding whitespace for search only',
                         'unindexedCategories': ['Unretained vocabularies and labels', 'Unreviewed translations or spelling variants',
                                                 'Arbitrary prose, tags and opaque JSON outside the recognised native structures'],
                         'limits': ['Native table labels do not establish API enum identity or a unique concept.',
                                    'A search hit is not exactMatch, sameAs, a join or a provider query alias.',
                                    'Record definitions do not supply missing definitions for individual enum values.',
                                    'No remote context, source link or schema reference is fetched.']}}


def search_discovery(index, query, limit=20):
    if index.get('schema') != SCHEMA:
        raise ValueError('Unsupported term-discovery index')
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError('Use a non-empty query of at most 500 characters')
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError('Result limit must be between 1 and 100')
    needle = normalise(query)
    tokens = set(re.findall(r'\w+', needle))
    hits = []
    for row in index['records']:
        for form in row['forms']:
            haystack = normalise(form['display'])
            exact = needle == haystack
            if exact or (tokens and tokens <= set(re.findall(r'\w+', haystack))):
                hits.append({'recordId': row['recordId'], 'title': row['title'],
                             'recordDefinition': row['definition'], 'resource': row['resource'],
                             'sourceFamily': row['sourceFamily'], 'recordSha256': row['recordSha256'],
                             'sources': row['sources'], 'temporal': row['temporal'], 'update': row['update'],
                             'form': form, 'exactSearchForm': exact,
                             'meaning': 'lexical-navigation-only'})
    hits.sort(key=lambda h: (not h['exactSearchForm'], h['recordId'], h['form']['pointer'], h['form']['kind']))
    semantic = [term for term in index.get('semanticTerms', [])
                if needle in {normalise(term['iri']), normalise(term['compactIri'])}]
    return {'schema': 'gis-ai-go.okf-plus-term-search.v1', 'revision': index['revision'],
            'inputDigest': index['inputDigest'], 'query': query, 'matchedForms': len(hits),
            'returnedForms': min(len(hits), limit), 'truncated': len(hits) > limit,
            'hits': hits[:limit], 'semanticTerms': semantic[:limit],
            'matchedSemanticTerms': len(semantic),
            'inferencePerformed': False, 'providerCalls': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', required=True, type=Path)
    parser.add_argument('--query', required=True)
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    index = load_index(args.index)
    print(canonical(search_discovery(index, args.query, args.limit)).decode(), end='')


def load_index(path):
    """Bound the actual read, and refuse concurrent replacement or growth."""
    path = Path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_INPUT_BYTES:
            raise ValueError('Term-discovery index is not a bounded regular file')
        raw = stream.read(MAX_INPUT_BYTES + 1)
        after = os.fstat(stream.fileno())
    identity = lambda st: (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
    if (len(raw) > MAX_INPUT_BYTES or len(raw) != before.st_size
            or identity(before) != identity(after) or identity(after) != identity(path.stat())):
        raise ValueError('Term-discovery index changed during its bounded read')
    return load_json(raw.decode('utf-8'))


if __name__ == '__main__':
    main()
