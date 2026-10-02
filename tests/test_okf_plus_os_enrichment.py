"""Synthetic OS metadata contracts: no network, credentials or feature records."""
import hashlib
import json
import unittest
from copy import deepcopy

from scripts.okf_plus.os_enrichment import (
    API_INDEX, GEMINI_PATH, OPENSEARCH, PRODUCT_SEARCH, documents,
    extract_contracts, gemini, product_state, products, structure,
)


class Capture:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, kind='json'):
        self.calls.append((url, kind))
        value = self.responses[url]
        return value, {'url': url, 'status': 200 if value is not None else 503,
                       'retrievedAt': '2026-10-02T00:00:00Z',
                       'sha256': hashlib.sha256(json.dumps(value).encode()).hexdigest()}

    def save(self, name, records, receipts, coverage):
        self.result = {'family': name, 'records': records, 'receipts': receipts,
                       'coverage': coverage}


def fence(value):
    return '```json\n' + json.dumps(value) + '\n```\n'


def html_catalogue(count=2, total=3):
    rows = [{'id': f'synthetic-native-{i}', 'title': f'Synthetic product {i}',
             'uri': f'/products/synthetic-product-{i}', 'tags': {
                 'access': [{'id': 'synthetic-open', 'label': 'Open'}],
                 'unreviewed': [{'id': 'omit', 'label': 'Unreviewed category'}]}}
            for i in range(count)]
    state = {'search': {'listings': {'productListing': {'results': rows,
             'pagingInfo': {'totalCount': total, 'pageIndex': 0, 'pageSize': 60}}}}}
    return '<script>window.REDUX_DATA = ' + json.dumps(state) + ';</script>'


def supplement():
    return {'method': 'browserDOM', 'sourceUrl': PRODUCT_SEARCH,
            'observedOn': '2026-10-02', 'observedTotal': 3,
            'completionText': 'You have viewed 3 of 3', 'products': [
                {'url': 'https://www.ordnancesurvey.co.uk/products/synthetic-product-2',
                 'title': 'Synthetic product 2'}]}


TEMPLATE = ('https://osmetadata.astuntechnology.com' + GEMINI_PATH
            + '?f=json&q={searchTerms}&startIndex={startIndex?}')
XML = ('<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">'
       '<Url type="application/json" indexOffset="0" template="'
       + TEMPLATE.replace('&', '&amp;') + '"/></OpenSearchDescription>')


def gemini_url(offset):
    return TEMPLATE.replace('{searchTerms}', '').replace('{startIndex?}', str(offset))


def gemini_page(ids, total=3):
    return {'timed_out': False, '_shards': {'failed': 0}, 'hits': {
        'total': {'value': total, 'relation': 'eq'}, 'hits': [
            {'_id': i, '_source': {'uuid': i,
                'resourceTitleObject': {'default': 'Synthetic title ' + i},
                'resourceDate': [{'type': 'publication', 'date': '2026-10-01'}],
                'contact': 'Excluded synthetic contact', 'abstract': 'Excluded abstract'}}
            for i in ids]}}


class OsEnrichmentTests(unittest.TestCase):
    def test_openapi_projection_retains_security_constraints_and_not_callability(self):
        spec = {'openapi': '3.0.1', 'info': {'title': 'Synthetic service', 'version': '1'},
            'security': [{'apiKey': []}], 'paths': {'/metadata': {
                'parameters': [{'name': 'version', 'in': 'query', 'schema': {'type': 'integer'}}],
                'get': {'responses': {'200': {'content': {'application/json': {'schema': {
                    'type': 'object', 'properties': {'id': {'type': 'string', 'readOnly': True}},
                    'required': ['id'], 'additionalProperties': False}}}}}},
                'post': {'security': [], 'requestBody': {'required': True, 'content': {
                    'application/json': {'schema': {'$ref': '#/components/schemas/Input'}}}},
                    'responses': {'201': {'$ref': '#/components/responses/Created'}}}}},
            'components': {'schemas': {'Input': {'type': 'object', 'description': 'Excluded guide prose',
                'properties': {'value': {'type': 'string', 'writeOnly': True, 'example': 'Excluded example'}}}},
                'securitySchemes': {'apiKey': {'type': 'apiKey', 'in': 'header', 'name': 'x-api-key'}},
                'responses': {'Created': {'description': 'Excluded guide prose'}}}}
        result, errors = extract_contracts(fence(spec))
        self.assertEqual(errors, [])
        contract = result[0]
        get, post = contract['operations']
        self.assertEqual(get['documentedSecurity'], [{'apiKey': []}])
        self.assertEqual(get['securityDeclaration'], 'root')
        self.assertEqual(post['documentedSecurity'], [])
        self.assertEqual(post['securityDeclaration'], 'operation')
        self.assertEqual(get['httpMethodSemantics'], 'safe-method')
        self.assertEqual(post['httpMethodSemantics'], 'potential-state-change')
        self.assertTrue(all(not op['callable'] for op in contract['operations']))
        self.assertEqual(get['parameters'][0]['name'], 'version')
        self.assertEqual(contract['unresolvedComponentClasses'], ['responses'])
        self.assertEqual(contract['schemas']['Input']['properties']['value'], {'type': 'string', 'writeOnly': True})
        self.assertNotIn('Excluded', json.dumps(contract))
        self.assertEqual(len(contract['fragmentSha256']), 64)

    def test_missing_security_is_unknown_and_examples_are_not_contracts(self):
        doc = fence({'openapi': '3.1.0', 'paths': {'/metadata': {'get': {'responses': {}}}}})
        doc += fence({'sample': 'not a contract'}) + '```json\n{bad}\n```\n'
        rows, errors = extract_contracts(doc)
        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]['operations'][0]['documentedSecurity'])
        self.assertEqual(rows[0]['operations'][0]['securityDeclaration'], 'not-declared')
        self.assertEqual(errors, [{'jsonFence': 3, 'error': 'invalid-json'}])

    def test_nested_schema_facts_survive_without_documentation_or_extensions(self):
        value = {'oneOf': [{'type': 'null'}, {'type': 'array', 'items': {'enum': ['A', 'B'],
            'description': 'Excluded'}, 'maxItems': 3}], '$defs': {'closed': False},
            'description': 'Excluded', 'examples': ['Excluded'], 'x-guide': 'Excluded'}
        result = structure(value)
        self.assertEqual(result['$defs']['closed'], False)
        self.assertEqual(result['oneOf'][1]['items'], {'enum': ['A', 'B']})
        self.assertNotIn('Excluded', json.dumps(result))

    def test_index_titles_with_escaped_brackets_and_missing_pages_keep_denominator(self):
        url = 'https://docs.os.uk/os-apis/synthetic.md'
        other = 'https://docs.os.uk/os-apis/missing.md'
        cap = Capture({API_INDEX: f'- [Template \\[month\\]]({url})\n- [Other]({other})\n',
                       url: '# Synthetic\n', other: None})
        documents(cap)
        self.assertEqual(cap.result['coverage']['reportedTotal'], 2)
        self.assertEqual(cap.result['coverage']['retrievedUnique'], 1)
        self.assertFalse(cap.result['coverage']['catalogueComplete'])

    def test_index_cannot_introduce_feature_or_external_requests(self):
        for url in ['https://api.os.uk/features/ngd/ofa/v1/collections/example/items',
                    'https://example.invalid/os-apis/test.md',
                    'https://docs.os.uk/os-apis/test.md?token=synthetic']:
            cap = Capture({API_INDEX: f'- [Unexpected]({url})\n'})
            with self.subTest(url=url), self.assertRaises(ValueError):
                documents(cap)
            self.assertEqual(cap.calls, [(API_INDEX, 'text')])

    def test_product_parser_normalises_only_bare_undefined_without_running_script(self):
        text = html_catalogue().replace('"pageIndex": 0', '"pageIndex": undefined')
        text = text.replace('Synthetic product 0', 'undefined')
        state = product_state(text)
        self.assertIsNone(state['pagingInfo']['pageIndex'])
        self.assertEqual(state['results'][0]['title'], 'undefined')
        malicious = text.replace('"pageIndex": undefined', '"pageIndex": fetch("https://example.invalid")')
        with self.assertRaises(ValueError):
            product_state(malicious)

    def test_initial_html_is_partial_and_does_not_follow_load_more(self):
        cap = Capture({PRODUCT_SEARCH: html_catalogue()})
        products(cap)
        self.assertEqual(cap.calls, [(PRODUCT_SEARCH, 'text')])
        self.assertEqual(cap.result['coverage']['retrievedUnique'], 2)
        self.assertFalse(cap.result['coverage']['catalogueComplete'])
        self.assertNotIn('unreviewed', json.dumps(cap.result))

    def test_browser_supplement_is_distinct_provenance_not_fabricated_http(self):
        cap = Capture({PRODUCT_SEARCH: html_catalogue()})
        products(cap, supplement())
        result = cap.result
        self.assertFalse(result['coverage']['catalogueComplete'])
        self.assertEqual(result['coverage']['retrievedUnique'], 2)
        self.assertTrue(result['coverage']['combinedCoverage']['complete'])
        self.assertEqual(len(result['records']), 3)
        browser = result['records'][-1]
        self.assertIsNone(browser['nativeIdentifier'])
        self.assertEqual(browser['id'], browser['url'])
        self.assertEqual(browser['sourceObservation']['status'], 'browser-observed')
        self.assertFalse({'sha256', 'retrievedAt', 'responseSha256'} & set(browser['sourceObservation']))
        self.assertEqual(len(result['receipts']), 1)
        self.assertEqual(cap.calls, [(PRODUCT_SEARCH, 'text')])

    def test_browser_supplement_rejects_conflicting_or_unproved_evidence(self):
        changes = [lambda v: v.update(method='HTTP'), lambda v: v.update(observedTotal=4),
            lambda v: v.update(completionText='Partial results'), lambda v: v.update(observedOn='2026-02-31'),
            lambda v: v.update(sha256='fabricated'),
            lambda v: v['products'][0].update(url='https://example.invalid/product'),
            lambda v: v['products'][0].update(url='/products/synthetic-product-2'),
            lambda v: v['products'][0].update(url='https://www.ordnancesurvey.co.uk/products/synthetic-product-0'),
            lambda v: v['products'].append(deepcopy(v['products'][0]))]
        for mutate in changes:
            value = supplement(); mutate(value)
            cap = Capture({PRODUCT_SEARCH: html_catalogue()})
            with self.subTest(value=value), self.assertRaises(ValueError):
                products(cap, value)

    def test_product_reference_cannot_redirect_or_include_credentials(self):
        for target in ['https://example.invalid/products/example', '//example.invalid/products/example',
                       'http://www.ordnancesurvey.co.uk/products/example', '/products/example?key=synthetic']:
            text = html_catalogue().replace('/products/synthetic-product-0', target)
            cap = Capture({PRODUCT_SEARCH: text})
            with self.subTest(target=target), self.assertRaises(ValueError):
                products(cap)
            self.assertEqual(cap.calls, [(PRODUCT_SEARCH, 'text')])

    def test_gemini_uses_advertised_offsets_and_excludes_personal_and_guide_fields(self):
        cap = Capture({OPENSEARCH: XML, gemini_url(0): gemini_page(['A', 'B']),
                       gemini_url(2): gemini_page(['C'])})
        gemini(cap)
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual([x[0] for x in cap.calls], [OPENSEARCH, gemini_url(0), gemini_url(2)])
        self.assertNotIn('Excluded', json.dumps(cap.result))
        self.assertEqual(cap.result['records'][0]['resourceDate'][0]['type'], 'publication')

    def test_gemini_duplicates_and_changed_denominator_cannot_claim_complete(self):
        for last in [gemini_page(['B']), gemini_page(['C'], 4), gemini_page([])]:
            cap = Capture({OPENSEARCH: XML, gemini_url(0): gemini_page(['A', 'B']),
                           gemini_url(2): last, gemini_url(3): gemini_page([], 4)})
            with self.subTest(last=last):
                gemini(cap)
                self.assertFalse(cap.result['coverage']['catalogueComplete'])

    def test_gemini_reviewed_parameter_correction_is_explicit_and_retained(self):
        first = gemini_url(0).replace('startIndex=', 'startindex=') + '&limit=10'
        second = gemini_url(2).replace('startIndex=', 'startindex=') + '&limit=10'
        cap = Capture({OPENSEARCH: XML, first: gemini_page(['A', 'B']), second: gemini_page(['C'])})
        gemini(cap, documented_pagination=True)
        self.assertTrue(cap.result['coverage']['catalogueComplete'])
        self.assertEqual([x[0] for x in cap.calls], [OPENSEARCH, first, second])
        pagination = cap.result['coverage']['pagination']
        self.assertIn('startIndex=', pagination['advertisedTemplate'])
        self.assertIn('startindex=', pagination['traversalTemplate'])
        self.assertEqual(pagination['method'], 'reviewed-documented-lowercase-parameter')

    def test_gemini_partial_search_results_stop_without_next_request(self):
        changes = [lambda v: v.update(timed_out=True),
                   lambda v: v['_shards'].update(failed=1),
                   lambda v: v['hits']['total'].update(relation='gte')]
        for mutate in changes:
            page = gemini_page(['A']); mutate(page)
            cap = Capture({OPENSEARCH: XML, gemini_url(0): page})
            with self.subTest(page=page):
                gemini(cap)
                self.assertFalse(cap.result['coverage']['catalogueComplete'])
                self.assertEqual(len(cap.calls), 2)

    def test_gemini_template_drift_or_xml_entities_cannot_introduce_requests(self):
        for value in [XML.replace('startIndex', 'offset'), XML.replace('osmetadata.astuntechnology.com', 'example.invalid'),
                      '<!DOCTYPE x [<!ENTITY x SYSTEM "file:///synthetic">]>' + XML]:
            cap = Capture({OPENSEARCH: value})
            with self.subTest(value=value), self.assertRaises(ValueError):
                gemini(cap)
            self.assertEqual(cap.calls, [(OPENSEARCH, 'text')])


if __name__ == '__main__':
    unittest.main()
