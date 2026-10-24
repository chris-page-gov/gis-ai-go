"""Offline inventory of recognised controlled-list structures in OKF+ records.

This inventories retained evidence. It does not fetch referenced routes, infer
concept identity or claim a complete external vocabulary denominator.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .model import canonical, read_markdown
except ImportError:  # Direct script execution.
    from model import canonical, read_markdown

SCHEMA_MAPS = {'properties', 'patternProperties', '$defs', 'definitions',
               'dependentSchemas', 'dependencies'}
SCHEMA_ARRAYS = {'allOf', 'anyOf', 'oneOf', 'prefixItems'}
SCHEMA_SINGLE = {'additionalProperties', 'unevaluatedProperties', 'propertyNames',
                 'contains', 'not', 'if', 'then', 'else', 'additionalItems',
                 'unevaluatedItems', 'contentSchema'}
ROUTE_PARTS = ('/code-lists/', '/codelist/', '/code-lists-and-enumerations',
               '/code-list-and-enumerations', '/classification-scheme')


def token(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def walk(value, pointer=''):
    yield pointer, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, pointer + '/' + token(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, pointer + '/' + str(index))


def schema_constraints(value, pointer=''):
    """Visit only known JSON Schema subschema positions; annotations stay opaque."""
    if not isinstance(value, dict):
        return  # Boolean schemas and property-dependency arrays contain no constraints.
    for key, child in value.items():
        path = pointer + '/' + token(key)
        if key == 'enum':
            if not isinstance(child, list):
                raise ValueError('Schema enum must be an array')
            yield path, key, child
        elif key == 'const':
            yield path, key, child
        elif key in SCHEMA_MAPS and isinstance(child, dict):
            for name, subschema in child.items():
                yield from schema_constraints(subschema, path + '/' + token(name))
        elif (key in SCHEMA_ARRAYS or key == 'items') and isinstance(child, list):
            for index, subschema in enumerate(child):
                yield from schema_constraints(subschema, path + '/' + str(index))
        elif key in SCHEMA_SINGLE or key == 'items':
            yield from schema_constraints(child, path)
        # Do not follow $ref, examples/default, arbitrary extensions or values in enum/const.


def media_schemas(value, pointer):
    if not isinstance(value, dict):
        return
    if 'schema' in value:
        yield pointer + '/schema', value['schema']
    for media, entry in value.get('content', {}).items():
        if isinstance(entry, dict) and 'schema' in entry:
            yield pointer + '/content/' + token(media) + '/schema', entry['schema']


def schema_roots(row):
    """Known roots in the retained NGD and normalised OpenAPI projections."""
    details = row.get('details', {})
    family = row['sourceFamily']
    if family == 'os-ngd-collections':
        for lane, schema in details.get('schemas', {}).items():
            yield '/details/schemas/' + token(lane), schema
    elif family == 'os-api-contracts':
        for index, contract in enumerate(details.get('contracts', [])):
            root = '/details/contracts/' + str(index)
            for name, schema in contract.get('schemas', {}).items():
                yield root + '/schemas/' + token(name), schema
            parameters = contract.get('componentParameters', {})
            if isinstance(parameters, dict):
                for name, entry in parameters.items():
                    yield from media_schemas(entry, root + '/componentParameters/' + token(name))
            for number, operation in enumerate(contract.get('operations', [])):
                path = root + '/operations/' + str(number)
                for n, parameter in enumerate(operation.get('parameters', [])):
                    yield from media_schemas(parameter, path + '/parameters/' + str(n))
                yield from media_schemas(operation.get('requestBody'), path + '/requestBody')
                for status, response in operation.get('responses', {}).items():
                    response_path = path + '/responses/' + token(status)
                    yield from media_schemas(response, response_path)
                    for name, header in response.get('headers', {}).items():
                        yield from media_schemas(header, response_path + '/headers/' + token(name))


def record_nodes(row):
    """Keep field constraints, source labels and catalogue references separate."""
    details = row.get('details', {})
    family = row['sourceFamily']
    for root, schema in schema_roots(row):
        for pointer, keyword, native in schema_constraints(schema, root):
            yield {'kind': ('native-schema-' if family == 'os-ngd-collections'
                            else 'native-api-contract-') + keyword,
                   'pointer': pointer, 'valueCount': len(native) if keyword == 'enum' else 1,
                   'nativeValueSha256': hashlib.sha256(canonical(native)).hexdigest()}
    for pointer, value in walk(details, '/details'):
        if isinstance(value, dict) and 'nativeLabelTable' in value:
            table = value['nativeLabelTable']
            yield {'kind': 'native-documentation-label-table',
                   'pointer': pointer + '/nativeLabelTable',
                   'rowCount': len(table.get('rows', [])),
                   'omittedRows': value.get('nativeLabelScope', {}).get('omittedLabelRows')}
    if family == 'ons-code-lists':
        yield {'kind': 'ons-code-list-catalogue-entry', 'pointer': '/details',
               'nativeId': details['id'], 'advertisedLinks': details.get('advertisedLinks', {})}
    if family == 'ons-nomis-datasets':
        for pointer, value in walk(details.get('components', {}), '/details/components'):
            if isinstance(value, dict) and 'codelist' in value:
                yield {'kind': 'nomis-native-sdmx-codelist-reference',
                       'pointer': pointer + '/codelist', 'nativeId': value['codelist'],
                       'conceptRef': value.get('conceptref')}
        for pointer, value in walk(row.get('qb:structure', {}), '/qb:structure'):
            if isinstance(value, dict) and 'qb:codeList' in value:
                yield {'kind': 'nomis-projected-codelist-route',
                       'pointer': pointer + '/qb:codeList', 'route': value['qb:codeList']['@id']}
    if family == 'ons-nomis-time-options':
        yield {'kind': 'nomis-retained-time-code-list', 'pointer': '/details/timeOptionsTable',
               'nativeId': details.get('codeListId'),
               'rowCount': len(details.get('timeOptionsTable', {}).get('rows', []))}
    if family == 'ons-latest-versions':
        for number, dimension in enumerate(details.get('dimensions', [])):
            yield {'kind': 'ons-version-dimension-reference',
                   'pointer': '/details/dimensions/' + str(number),
                   'nativeId': dimension.get('id'), 'name': dimension.get('name'),
                   'label': dimension.get('label'), 'edition': details.get('edition'),
                   'version': details.get('version')}
    if family == 'ons-population-types':
        yield {'kind': 'ons-population-type', 'pointer': '/details',
               'nativeId': details.get('name'), 'label': details.get('label')}


def inventory(repo):
    sources, nodes, routes = [], [], {}
    families = Counter()
    for path in sorted((repo / 'okf-plus/records').rglob('*.md')):
        raw = path.read_bytes()
        row, _ = read_markdown(path)
        source = {'file': str(path.relative_to(repo)), 'recordId': row['@id'],
                  'sha256': hashlib.sha256(raw).hexdigest()}
        sources.append(source)
        families[row['sourceFamily']] += 1
        for node in record_nodes(row):
            nodes.append({**source, 'sourceFamily': row['sourceFamily'],
                          'sourceUrl': row['resource'], **node})
        for pointer, value in walk(row):
            if (isinstance(value, str) and value.startswith(('https://', 'http://'))
                    and any(part in value for part in ROUTE_PARTS)):
                key = (value, row['sourceFamily'])
                route = routes.setdefault(key, {'sourceUrl': value, 'sourceLane': key[1],
                                                'status': 'retained-reference-not-followed',
                                                'references': []})
                route['references'].append({'recordId': row['@id'], 'pointer': pointer})
    nodes.sort(key=lambda item: (item['recordId'], item['pointer'], item['kind']))
    route_rows = sorted(routes.values(), key=lambda item: (item['sourceUrl'], item['sourceLane']))
    counts = Counter(item['kind'] for item in nodes)
    summary = {
        'schema': 'gis-ai-go.retained-vocabulary-inventory.v2',
        'scope': 'Recognised controlled-list structures in every retained Markdown record; no network.',
        'corpusRecords': len(sources), 'sourceFamilyCounts': dict(sorted(families.items())),
        'sourceInventorySha256': hashlib.sha256(canonical(sources)).hexdigest(),
        'recognisedNodeCounts': dict(sorted(counts.items())), 'recognisedNodeTotal': len(nodes),
        'uniqueAdvertisedOrProjectedUrls': len({item['sourceUrl'] for item in route_rows}),
        'ngdNavigationCodeListRoutes': len({item['sourceUrl'] for item in route_rows
                                         if item['sourceLane'] == 'osngd-documentation'
                                         and '/osngd/code-lists/code-lists-overview/' in item['sourceUrl']}),
        'nomisUniqueNativeCodeListIds': len({item['nativeId'] for item in nodes
                                          if item['kind'] == 'nomis-native-sdmx-codelist-reference'}),
        'nativeSchemaValueOccurrences': sum(item['valueCount'] for item in nodes
                                            if item['kind'].startswith('native-schema-')),
        'documentationLabelRows': sum(item['rowCount'] for item in nodes
                                       if item['kind'] == 'native-documentation-label-table'),
        'retainedTimeCodeRows': sum(item['rowCount'] for item in nodes
                                    if item['kind'] == 'nomis-retained-time-code-list'),
        'rulesCompleteForBoundCorpus': True, 'completeDomainVocabularyCoverage': False,
        'externalDenominator': None,
        'limits': [
            'Counts use different units and include repeated schema/queryable contexts; they are not distinct concepts.',
            'Annotations and remote schema references remain opaque. Unknown prose routes are outside the stated rules.',
            'Advertised and project-projected URLs retain their exact spelling; current availability and syntax are unverified.',
            'Catalogue entries and dimension references do not establish subordinate category or edition closure.',
            'Native label tables are bounded source-position evidence, not API enum identity or vocabulary conformance.',
        ],
    }
    return summary, sources, nodes, route_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True,
                        help='New local directory for generated inventory; no existing output is overwritten.')
    args = parser.parse_args()
    result = inventory(args.repo)
    args.output.mkdir(parents=False, exist_ok=False)
    for name, value in zip(('summary.json', 'sources.json', 'nodes.json', 'routes.json'), result):
        (args.output / name).write_bytes(canonical(value))
    print(json.dumps({'records': result[0]['corpusRecords'],
                      'recognisedNodes': result[0]['recognisedNodeTotal']}))


if __name__ == '__main__':
    main()
