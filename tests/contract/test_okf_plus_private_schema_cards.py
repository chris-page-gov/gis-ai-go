"""Independent full-value reconstruction and reference tests for private schemas."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import unittest

from scripts.okf_plus.private_schema_cards import schema_cards

URL = 'https://api.os.uk/features/ngd/ofa/v1/collections/synthetic-1/schema'
WHEN = '2026-10-18T00:00:00Z'


def canonical_hash(value):
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False) + '\n').encode()
    return hashlib.sha256(raw).hexdigest()


def unescape(key):
    return key.replace('~1', '/').replace('~0', '~')


def value_at(document, pointer):
    result = document
    for key in pointer[1:].split('/') if pointer else []:
        key = unescape(key)
        result = result[int(key)] if isinstance(result, list) else result[key]
    return result


class PrivateSchemaCardsTests(unittest.TestCase):
    def emit(self, document):
        raw = json.dumps(document, ensure_ascii=False).encode()
        emitted = schema_cards(raw, URL, WHEN)
        cards = [json.loads(body.decode().split('\n---\n', 1)[0][4:]) for _, body in emitted]
        self.assertTrue(all(len(body) <= 16384 for _, body in emitted))
        self.assertEqual(len({card['@id'] for card in cards}), len(cards))
        for card in cards:
            source = card['source']
            expected = value_at(document, source['jsonPointer'])
            self.assertEqual(source['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(source['valueSha256'], canonical_hash(expected))
            self.assertFalse(card['facts']['trustedInstructions'])
            self.assertEqual(card['facts']['privacy'], 'private-source')
            if 'fragment' in source:
                fragment = source['fragment']
                text = card['facts']['text'].encode()
                self.assertEqual(fragment['sha256'], hashlib.sha256(text).hexdigest())
                self.assertEqual(expected.encode()[fragment['byteStart']:fragment['byteEnd']], text)
        return cards

    def reconstruct(self, cards):
        anchors = {card['source']['jsonPointer']: card for card in cards if 'fragment' not in card['source']}

        def reconstruct_value(pointer):
            card = anchors[pointer]
            facts = card['facts']
            if 'schema' in facts:
                return deepcopy(facts['schema'])
            self.assertEqual(facts['representation'], 'complete-linked-parts')
            children = [candidate for candidate in cards if candidate.get('parent') == card['@id']]
            if facts['sourceValueType'] == 'str':
                children.sort(key=lambda candidate: candidate['source']['fragment']['index'])
                self.assertEqual(len(children), facts['partCount'])
                offset = 0
                for child in children:
                    self.assertEqual(child['source']['fragment']['byteStart'], offset)
                    offset = child['source']['fragment']['byteEnd']
                return ''.join(child['facts']['text'] for child in children)
            direct = {candidate['source']['jsonPointer'].removeprefix(pointer + '/'): candidate
                      for candidate in children}
            if facts['sourceValueType'] == 'dict':
                return {unescape(key): reconstruct_value(candidate['source']['jsonPointer'])
                        for key, candidate in direct.items()}
            self.assertEqual(facts['sourceValueType'], 'list')
            self.assertEqual({int(key) for key in direct}, set(range(len(direct))))
            return [reconstruct_value(direct[str(index)]['source']['jsonPointer']) for index in range(len(direct))]

        root = anchors['']
        if 'rootMetadata' in root['facts']:
            result = deepcopy(root['facts']['rootMetadata'])
        else:
            self.assertEqual(root['facts']['rootMetadataRepresentation'], 'complete-linked-parts')
            result = {unescape(pointer[1:]): reconstruct_value(pointer)
                      for pointer, card in anchors.items()
                      if pointer.startswith('/') and '/' not in pointer[1:] and pointer != '/properties'}
        if root['facts'].get('propertiesDeclared', True):
            result['properties'] = {unescape(pointer.removeprefix('/properties/')): reconstruct_value(pointer)
                                    for pointer, card in anchors.items() if card['kind'] == 'schema-field'}
        return result

    def test_complete_schema_reconstructs_root_metadata_nested_constraints_and_large_values(self):
        long_text = 'Synthetic height interpretation with café and 🌍 qualifiers. ' * 650
        document = {
            '$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'Synthetic full schema', 'description': long_text,
            'type': 'object', 'additionalProperties': False,
            'required': ['height', 'providerMissingField'],
            '$defs': {'Measure': {'description': long_text, 'type': ['number', 'null'], 'minimum': 0}},
            'properties': {
                'height': {'description': long_text, '$ref': '#/$defs/Measure', 'unit': 'metres',
                           'verticalDatum': 'SyntheticDatum', 'examples': [None, 0, 45.6],
                           'allOf': [{'maximum': 1000}, {'not': {'const': -1}}]},
                'a/b~c': {'enum': [None, False, 0, 'short', long_text, {'native': ['one', 2]}]},
                'blocked': False,
            },
        }
        cards = self.emit(document)
        self.assertEqual(self.reconstruct(cards), document)
        field = next(card for card in cards if card['kind'] == 'schema-field' and card['nativeIdentifier'] == 'height')
        self.assertTrue(field['facts']['required'])
        missing = next(card for card in cards if card['kind'] == 'schema-required-name')
        self.assertEqual(missing['facts']['declarationStatus'], 'required-without-declared-property')

    def test_oversized_field_retains_traversable_explicit_local_reference(self):
        document = {'$defs': {'Measure': {'type': 'number'}},
                    'properties': {'height': {'description': 'Synthetic qualifiers. ' * 2000,
                                              '$ref': '#/$defs/Measure'}}}
        cards = self.emit(document)
        by_id = {card['@id']: card for card in cards}
        field = next(card for card in cards if card['kind'] == 'schema-field')
        reachable = {field['@id']}
        pending = [field['@id']]
        while pending:
            current = by_id[pending.pop()]
            links = [item['@id'] for item in current.get('related', [])]
            links += [card['@id'] for card in cards if card.get('parent') == current['@id']]
            for target in links:
                self.assertIn(target, by_id)
                if target not in reachable:
                    reachable.add(target)
                    pending.append(target)
        self.assertTrue(any(by_id[target]['source']['jsonPointer'] == '/$defs/Measure' for target in reachable))

    def test_uri_encoded_local_reference_and_pointer_escaping_resolve_without_external_fetch(self):
        document = {'$defs': {'Measure /~': {'type': ['number', 'null']}},
                    'properties': {'height': {'allOf': [{'$ref': '#/%24defs/Measure%20~1~0'}]},
                                   'remote': {'$ref': 'https://not-a-request.invalid/schema'},
                                   'missing': {'$ref': '#/$defs/not-present'}}}
        cards = self.emit(document)
        by_id = {card['@id']: card for card in cards}
        field = next(card for card in cards if card['kind'] == 'schema-field' and card['nativeIdentifier'] == 'height')
        self.assertEqual(len(field['related']), 1)
        target = by_id[field['related'][0]['@id']]
        self.assertEqual(target['source']['jsonPointer'], '/$defs/Measure ~1~0')
        self.assertEqual(target['facts']['schema'], document['$defs']['Measure /~'])
        self.assertEqual(self.reconstruct(cards), document)

    def test_recursive_references_preserve_finite_graph_and_all_null_enum_values(self):
        document = {'$defs': {'Node': {'type': 'object', 'properties': {'next': {'$ref': '#/$defs/Node'}}}},
                    'properties': {'node': {'$ref': '#/$defs/Node'},
                                   'quality': {'type': ['string', 'null'], 'enum': [None, 'Known', 'Unknown']}}}
        cards = self.emit(document)
        self.assertLess(len(cards), 20)
        self.assertEqual(self.reconstruct(cards), document)
        codes = [card['facts']['schema'] for card in cards if card['kind'] == 'schema-enum-value']
        self.assertEqual(codes, [None, 'Known', 'Unknown'])

    def test_json_escape_expansion_still_respects_byte_bound_and_roundtrips(self):
        document = {'properties': {'height': {'description': '\u0000\u0001\u001f\\\"' * 6000}}}
        self.assertEqual(self.reconstruct(self.emit(document)), document)

    def test_nested_schema_resource_never_links_to_wrong_document_root(self):
        document = {'$defs': {'Measure': {'type': 'string'}},
                    'properties': {'height': {'$id': 'https://example.org/synthetic-child-schema',
                                              '$defs': {'Measure': {'type': 'number'}},
                                              '$ref': '#/$defs/Measure'}}}
        cards = self.emit(document)
        by_id = {card['@id']: card for card in cards}
        field = next(card for card in cards if card['kind'] == 'schema-field')
        for link in field['related']:
            target = by_id[link['@id']]
            self.assertEqual(target['source']['jsonPointer'], '/properties/height/$defs/Measure')
        if not field['related']:
            self.assertTrue(any('unresolved' in gap.casefold() or 'resource' in gap.casefold() for gap in field['gaps']))
        self.assertEqual(self.reconstruct(cards), document)

    def test_encoded_leading_pointer_slash_is_a_local_reference(self):
        document = {'$defs': {'Measure': {'type': 'number'}},
                    'properties': {'height': {'$ref': '#%2F%24defs%2FMeasure'}}}
        cards = self.emit(document)
        by_id = {card['@id']: card for card in cards}
        field = next(card for card in cards if card['kind'] == 'schema-field')
        self.assertEqual(len(field['related']), 1)
        target = by_id[field['related'][0]['@id']]
        self.assertEqual(target['source']['jsonPointer'], '/$defs/Measure')

    def test_absent_and_explicit_empty_properties_reconstruct_distinctly(self):
        for document in ({}, {'properties': {}}, {'description': 'Synthetic root. ' * 2000},
                         {'description': 'Synthetic root. ' * 2000, 'properties': {}}):
            with self.subTest(properties_declared='properties' in document):
                cards = self.emit(document)
                root = next(card for card in cards if card['kind'] == 'private-schema')
                self.assertEqual(root['facts']['propertiesDeclared'], 'properties' in document)
                self.assertEqual(self.reconstruct(cards), document)


if __name__ == '__main__':
    unittest.main()
