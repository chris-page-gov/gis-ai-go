#!/usr/bin/env python3
"""Capture OS documentation contracts and catalogues without feature requests.

Source pages remain in Capture's ignored evidence store. Public projections omit
guide prose, examples, abstracts, contacts and account fields. No JavaScript from
the product page is executed; only its serialised catalogue state is parsed.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

try:
    from .harvest import Capture, ROOT, clean_text
except ImportError:
    from harvest import Capture, ROOT, clean_text

API_INDEX = 'https://docs.os.uk/os-apis/llms.txt'
OPENSEARCH = 'https://osmetadata.astuntechnology.com/geonetwork/api/collections/main?f=opensearch'
GEMINI_PATH = '/geonetwork/api/collections/044fac9d-3bba-4214-b010-eeb9978422b2/items'
PRODUCT_SEARCH = 'https://www.ordnancesurvey.co.uk/products/search-for-os-products'
GEMINI_PAGINATION_REFERENCE = 'https://github.com/geonetwork/geonetwork-microservices/tree/main/modules/services/ogc-api-records'
HTTP_METHODS = {'get', 'head', 'options', 'post', 'put', 'patch', 'delete', 'trace'}
SCHEMA_KEYS = {
    '$ref', '$id', '$schema', 'type', 'format', 'enum', 'const', 'required',
    'additionalProperties', 'items', 'prefixItems', 'oneOf', 'anyOf', 'allOf',
    'not', 'if', 'then', 'else', 'minimum', 'maximum', 'exclusiveMinimum',
    'exclusiveMaximum', 'multipleOf', 'minItems', 'maxItems', 'uniqueItems',
    'minLength', 'maxLength', 'pattern', 'minProperties', 'maxProperties',
    'nullable', 'readOnly', 'writeOnly', 'deprecated',
}
GUIDES = {
    'https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates.md': 'product-refresh-guidance',
    'https://docs.os.uk/os-downloads/resources/product-resources/end-of-life-product-notices.md': 'withdrawal-index',
    'https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/os-ngd-data-ordering-and-currency.md': 'delivery-currency-guidance',
    'https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning.md': 'schema-versioning-guidance',
    'https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering.md': 'temporal-filter-guidance',
    'https://docs.os.uk/osngd/os-ngd-news/change-log.md': 'documentation-change-log',
    'https://docs.os.uk/osngd/code-lists/code-lists-overview.md': 'code-list-index',
}


def safe_url(value):
    if not isinstance(value, str):
        return None
    p = urlparse(value)
    if (p.scheme != 'https' or not p.hostname or p.username or p.password
            or any(k.lower() in {'key', 'token', 'apikey', 'api_key', 'signature', 'sig'}
                   for k in parse_qs(p.query))):
        return None
    return value


def structure(value):
    """Keep machine constraints, never descriptions/examples or vendor extensions."""
    if isinstance(value, bool):
        return value
    if not isinstance(value, dict):
        return {}
    result = {}
    for key, item in value.items():
        if key in {'properties', 'patternProperties', '$defs', 'definitions'} and isinstance(item, dict):
            result[key] = {name: structure(schema) for name, schema in item.items()}
        elif key in SCHEMA_KEYS:
            if isinstance(item, dict):
                result[key] = structure(item)
            elif isinstance(item, list) and key in {'allOf', 'anyOf', 'oneOf', 'prefixItems'}:
                result[key] = [structure(schema) for schema in item]
            else:
                result[key] = item
    return result


def parameters(items):
    return [{**{k: p[k] for k in ('$ref', 'name', 'in', 'required', 'deprecated', 'style', 'explode') if k in p},
             **({'schema': structure(p['schema'])} if 'schema' in p else {})}
            for p in items if isinstance(p, dict)]


def content(items):
    return {media: {'schema': structure(spec.get('schema', {}))}
            for media, spec in items.items() if isinstance(spec, dict)}


def contract_projection(spec):
    operations = []
    for path, path_item in spec.get('paths', {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            responses = {}
            for code, response in operation.get('responses', {}).items():
                if isinstance(response, dict):
                    responses[code] = ({'$ref': response['$ref']} if '$ref' in response
                                       else {'content': content(response.get('content', {}))})
            row = {
                'method': method.upper(), 'path': path,
                'operationId': operation.get('operationId'),
                'parameters': parameters(path_item.get('parameters', [])) + parameters(operation.get('parameters', [])),
                'responses': responses,
                'documentedSecurity': operation.get('security', spec.get('security')),
                'securityDeclaration': 'operation' if 'security' in operation else 'root' if 'security' in spec else 'not-declared',
                'httpMethodSemantics': 'safe-method' if method in {'get', 'head', 'options', 'trace'} else 'potential-state-change',
                'callable': False, 'admission': 'not-reviewed',
                'deprecated': operation.get('deprecated', False),
            }
            body = operation.get('requestBody')
            if isinstance(body, dict):
                row['requestBody'] = ({'$ref': body['$ref']} if '$ref' in body
                                      else {'required': body.get('required', False), 'content': content(body.get('content', {}))})
            operations.append(row)
    schemes = {}
    for name, scheme in spec.get('components', {}).get('securitySchemes', {}).items():
        if isinstance(scheme, dict):
            schemes[name] = {k: v for k, v in scheme.items() if k in {'$ref', 'type', 'scheme', 'name', 'in', 'bearerFormat', 'openIdConnectUrl'}}
            if isinstance(scheme.get('flows'), dict):
                schemes[name]['flows'] = {flow: {**{k: v for k, v in data.items() if k in {'authorizationUrl', 'tokenUrl', 'refreshUrl'}},
                                               'scopeNames': list(data.get('scopes', {}))}
                                        for flow, data in scheme['flows'].items() if isinstance(data, dict)}
    components = spec.get('components', {})
    return {'openapi': spec['openapi'], 'title': spec.get('info', {}).get('title'),
            'version': spec.get('info', {}).get('version'),
            'servers': [s['url'] for s in spec.get('servers', []) if isinstance(s, dict) and isinstance(s.get('url'), str)],
            'securitySchemes': schemes, 'operations': operations,
            'schemas': {name: structure(schema) for name, schema in components.get('schemas', {}).items()},
            'componentParameters': {name: parameters([p])[0] for name, p in components.get('parameters', {}).items() if isinstance(p, dict)},
            'unresolvedComponentClasses': sorted(set(components) - {'schemas', 'parameters', 'securitySchemes'}),
            'validationStatus': 'extracted-not-conformance-validated'}


def extract_contracts(text):
    contracts, errors = [], []
    for number, block in enumerate(re.findall(r'^```json\s*\n(.*?)^```\s*$', text, re.M | re.S), 1):
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            errors.append({'jsonFence': number, 'error': 'invalid-json'})
            continue
        if isinstance(obj, dict) and isinstance(obj.get('openapi'), str) and isinstance(obj.get('paths'), dict):
            contracts.append({'jsonFence': number, 'fragmentSha256': hashlib.sha256(block.encode()).hexdigest(), **contract_projection(obj)})
    return contracts, errors


def documents(cap):
    index, receipt = cap.get(API_INDEX, 'text')
    if index is None:
        return
    urls = dict((url, html.unescape(title)) for title, url in re.findall(r'^- \[(.*?)\]\((https://[^)]+)\)', index, re.M))
    receipts, records = [receipt], []
    for url, title in urls.items():
        p = urlparse(url)
        if p.netloc != 'docs.os.uk' or not p.path.startswith('/os-apis/') or not p.path.endswith('.md') or p.query or p.fragment:
            raise ValueError('Unexpected API documentation index route')
        text, r = cap.get(url, 'text'); receipts.append(r)
        contracts, errors = extract_contracts(text) if text is not None else ([], [])
        records.append({'id': url, 'url': url, 'title': title, 'kind': 'documentation-contract',
                        'contentCaptured': text is not None, 'contracts': contracts, 'extractionErrors': errors,
                        'sourceSha256': r.get('sha256'), 'callable': False})
    cap.save('os-api-contracts', records, receipts, {
        'unit': 'indexed OS API documentation page', 'reportedTotal': len(urls),
        'retrievedUnique': sum(r['contentCaptured'] for r in records),
        'catalogueComplete': all(r['contentCaptured'] for r in records),
        'openapiFragments': sum(len(r['contracts']) for r in records),
        'limitations': ['Contract extraction does not authorise calls or prove current service availability.',
                       'Raw guide prose and examples stay in ignored capture evidence.',
                       'Fragments remain separate; external references are not retrieved and component conflicts are not merged.']})


def guides(cap):
    receipts, records = [], []
    for url, kind in GUIDES.items():
        text, r = cap.get(url, 'text'); receipts.append(r)
        heading = re.search(r'^# (.+)$', text or '', re.M)
        records.append({'id': url, 'url': url, 'title': clean_text(heading[1]) if heading else kind,
                        'kind': kind, 'contentCaptured': text is not None, 'sourceSha256': r.get('sha256'),
                        'semanticReview': 'See docs/implementation/OKF-220_OS_SOURCE_REVIEW.md',
                        'callable': False})
    cap.save('os-lifecycle-guides', records, receipts, {'unit': 'selected official lifecycle guide',
             'reportedTotal': len(GUIDES), 'retrievedUnique': sum(r['contentCaptured'] for r in records),
             'catalogueComplete': all(r['contentCaptured'] for r in records),
             'limitations': ['Selected guide coverage only, not all release histories or code-list values.',
                            'Guide text is retained privately; semantic claims require source review.']})


def gemini_record(hit):
    source = hit.get('_source', {})
    identifier = source.get('uuid') or source.get('metadataIdentifier') or hit.get('_id')
    if not isinstance(identifier, str) or not identifier:
        raise ValueError('GEMINI metadata record has no identifier')
    title = source.get('resourceTitleObject', {})
    if isinstance(title, dict):
        title = title.get('default') or title.get('eng') or next(iter(title.values()), '')
    return {'id': identifier, 'title': clean_text(title), 'kind': 'catalogue-metadata',
            'url': 'https://osmetadata.astuntechnology.com/geonetwork/api/collections/main/items/' + identifier,
            **{k: source[k] for k in ('resourceType', 'resourceDate', 'createDate', 'changeDate', 'mainLanguage') if k in source},
            'callable': False}


def gemini(cap, documented_pagination=False):
    xml, r = cap.get(OPENSEARCH, 'text'); receipts = [r]
    if xml is None:
        return
    if '<!DOCTYPE' in xml.upper() or '<!ENTITY' in xml.upper():
        raise ValueError('XML entity declarations are not admitted')
    templates = [e.attrib.get('template', '') for e in ET.fromstring(xml).iter()
                 if e.tag.split('}')[-1] == 'Url' and e.attrib.get('type') == 'application/json' and e.attrib.get('indexOffset') == '0']
    if len(templates) != 1:
        raise ValueError('Expected one zero-based JSON catalogue template')
    template = templates[0]
    expected = 'https://osmetadata.astuntechnology.com' + GEMINI_PATH + '?f=json&q={searchTerms}&startIndex={startIndex?}'
    if template != expected:
        raise ValueError('Catalogue template changed; review before traversal')
    # The service's advertised startIndex was observed to repeat page zero.
    # GeoNetwork's own README documents lowercase startindex and limit; the
    # separately authorised probe verified distinct pages before enabling this.
    traversal_template = (template.replace('startIndex={startIndex?}', 'startindex={startIndex?}') + '&limit=10'
                          if documented_pagination else template)
    records, unique, total, stable, duplicates, offset, reason = [], set(), None, True, 0, 0, None
    while True:
        data, r = cap.get(traversal_template.replace('{searchTerms}', '').replace('{startIndex?}', str(offset))); receipts.append(r)
        if data is None:
            reason = 'request-failed'; break
        hits = data.get('hits', {}); count = hits.get('total', {}); batch = hits.get('hits', [])
        if data.get('timed_out') or data.get('_shards', {}).get('failed', 0) or count.get('relation') != 'eq' or not isinstance(count.get('value'), int):
            reason = 'inexact-or-incomplete-source-response'; break
        if total is not None and total != count['value']:
            stable = False
        total = count['value']
        before = len(unique)
        for hit in batch:
            record = gemini_record(hit)
            if record['id'] in unique:
                duplicates += 1
            else:
                records.append(record); unique.add(record['id'])
        if duplicates:
            reason = 'duplicate-records'; break
        offset += len(batch)
        if offset >= total:
            break
        if not batch or len(unique) == before:
            reason = 'non-progressing-page'; break
    cap.save('os-gemini-metadata', records, receipts, {'unit': 'GEMINI catalogue metadata UUID',
             'reportedTotal': total, 'retrievedUnique': len(unique), 'stableReportedTotal': stable,
             'duplicateCount': duplicates, 'stopReason': reason,
             'pagination': {'advertisedTemplate': template, 'traversalTemplate': traversal_template,
                            'method': 'reviewed-documented-lowercase-parameter' if documented_pagination else 'advertised-template',
                            'reference': GEMINI_PAGINATION_REFERENCE if documented_pagination else OPENSEARCH,
                            'advertisedParameterDefect': 'startIndex repeated page zero in the observed service' if documented_pagination else None},
             'catalogueComplete': reason is None and stable and total == len(unique),
             'limitations': ['Catalogue capture is not transactionally frozen; equal-count substitutions remain possible.',
                            'Metadata dates are not automatically data reference periods.',
                            'Contacts, account fields, abstracts and geographic records are excluded.']})


def product_state(text):
    match = re.search(r'window\.REDUX_DATA\s*=\s*', text)
    if not match:
        raise ValueError('Product catalogue state not found')
    end = text.find('</script>', match.end())
    if end < 0:
        raise ValueError('Unterminated product catalogue state')
    serialised = text[match.end():end].strip().rstrip(';')
    # A narrow lexical normalisation of bare undefined; quoted strings remain
    # byte-preserved. Any other JavaScript expression fails JSON parsing.
    serialised = re.sub(r'"(?:\\.|[^"\\])*"|\bundefined\b',
                        lambda m: 'null' if m[0] == 'undefined' else m[0], serialised)
    return json.loads(serialised)['search']['listings']['productListing']


def product_url(value):
    if not isinstance(value, str):
        raise ValueError('Product reference must be a URL')
    url = urljoin(PRODUCT_SEARCH, value)
    p = urlparse(url)
    if (p.scheme != 'https' or p.netloc != 'www.ordnancesurvey.co.uk'
            or not re.fullmatch(r'/products/[a-z0-9-]+', p.path) or p.query or p.fragment):
        raise ValueError('Unexpected product reference URL')
    return url


def product_ui_supplement(value, total):
    """Validate an authored browser observation, never treat it as HTTP capture."""
    keys = {'method', 'sourceUrl', 'observedOn', 'observedTotal', 'completionText', 'products'}
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError('Unexpected browser supplement fields')
    if (value['method'] != 'browserDOM' or value['sourceUrl'] != PRODUCT_SEARCH
            or type(value['observedTotal']) is not int or value['observedTotal'] != total
            or value['completionText'] != f'You have viewed {total} of {total}'):
        raise ValueError('Browser supplement does not reconcile the reported catalogue')
    if not isinstance(value['observedOn'], str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value['observedOn']):
        raise ValueError('Browser observation requires an ISO calendar date')
    date.fromisoformat(value['observedOn'])
    if not isinstance(value['products'], list) or not 1 <= len(value['products']) <= 100:
        raise ValueError('Browser supplement must contain 1..100 product references')
    observation = {k: v for k, v in value.items() if k != 'products'}
    observation['status'] = 'browser-observed'
    rows, seen = [], set()
    for item in value['products']:
        if not isinstance(item, dict) or set(item) != {'url', 'title'}:
            raise ValueError('Browser product reference fields changed')
        url = product_url(item['url'])
        if url != item['url'] or url in seen:
            raise ValueError('Browser references must have distinct canonical URLs')
        if not isinstance(item['title'], str) or not item['title'].strip() or len(item['title']) > 200:
            raise ValueError('Browser product title is invalid')
        seen.add(url)
        rows.append({'id': url, 'nativeIdentifier': None, 'idBasis': 'canonical-reference-url',
                     'url': url, 'title': clean_text(item['title']), 'kind': 'product-reference',
                     'callable': False, 'sourceObservation': observation})
    return rows, observation


def products(cap, ui_supplement=None):
    text, r = cap.get(PRODUCT_SEARCH, 'text')
    if text is None:
        return
    state = product_state(text); total = state['pagingInfo']['totalCount']; rows = {}
    for product in state['results']:
        url = product_url(product['uri'])
        if url in rows:
            raise ValueError('Duplicate embedded product reference')
        rows[url] = {'id': product['id'], 'url': url, 'title': clean_text(product['title']),
                     'kind': 'product-reference', 'callable': False,
                     'tags': {key: [{'id': tag['id'], 'label': clean_text(tag['label'])} for tag in value]
                              for key, value in product.get('tags', {}).items() if key in {'type', 'access', 'plan'}}}
    captured = len(rows)
    supplement_count, observation = 0, None
    if ui_supplement is not None:
        additions, observation = product_ui_supplement(ui_supplement, total)
        for addition in additions:
            if addition['url'] in rows:
                raise ValueError('Browser supplement overlaps the captured initial page')
            rows[addition['url']] = addition
        supplement_count = len(additions)
        if len(rows) > total:
            raise ValueError('Combined catalogue exceeds the reported total')
    cap.save('os-product-search', list(rows.values()), [r], {'unit': 'OS product search entry',
             'reportedTotal': total, 'retrievedUnique': captured, 'catalogueComplete': captured == total,
             'browserSupplementCount': supplement_count, 'browserObservation': observation,
             'combinedCoverage': {'reviewedUnique': len(rows), 'reportedTotal': total,
                                  'complete': len(rows) == total,
                                  'method': 'HTTP embedded state plus browser DOM' if observation else 'HTTP embedded state'},
             'sourcePaging': state['pagingInfo'],
             'limitations': ['Only the returned embedded catalogue state is parsed; no page script is executed.',
                            'The observed delivery API returned 401; no credentials are acquired or transport retried.',
                            'Browser supplement entries have no captured native UUID, HTTP status, response hash or retrievedAt.',
                            'Product/service marketing entries are not all independent datasets or admitted providers.']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('families', nargs='+', choices=['api-docs', 'guides', 'gemini', 'products'])
    parser.add_argument('--max-requests', type=int, default=4000)
    parser.add_argument('--product-ui-supplement', type=Path,
                        help='Reviewed JSON browser observation for product references absent from initial HTML')
    parser.add_argument('--gemini-documented-pagination', action='store_true',
                        help='Use reviewed GeoNetwork lowercase startindex and limit=10; retain advertised-template defect')
    args = parser.parse_args()
    if not 1 <= args.max_requests <= 4000:
        parser.error('Cumulative request ceiling must be 1..4000')
    cap = Capture(ROOT, args.max_requests)
    functions = {'api-docs': documents, 'guides': guides, 'gemini': gemini, 'products': products}
    for family in args.families:
        if family == 'products' and args.product_ui_supplement:
            products(cap, json.loads(args.product_ui_supplement.read_text(encoding='utf-8')))
        elif family == 'gemini' and args.gemini_documented_pagination:
            gemini(cap, documented_pagination=True)
        else:
            functions[family](cap)
    print('cumulative capture attempts', len(cap.ledger['requests']), flush=True)


if __name__ == '__main__':
    main()
