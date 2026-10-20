"""Provider-free synthetic Linked Identifiers security, durability and semantics."""
import copy
from datetime import datetime, timezone
from email.message import Message
import json
import io
import http.client
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, Mock, patch
from urllib.error import HTTPError
from jsonschema import Draft202012Validator

from scripts.okf_plus import linked_identifiers as m

KEY = 'synthetic-private-key-not-real'
OP = {'kind': 'feature', 'featureType': 'BLPU', 'id': '000000000001'}
METHOD = 'BLPU_UPRN_TopographicArea_TOID_5'


def response():
    return {'linkedIdentifier': {'identifier': OP['id'], 'identifierType': 'UPRN', 'featureType': 'BLPU'},
        'correlations': [{'correlationMethodIdentifier': METHOD, 'correlatedFeatureType': 'TopographicArea',
            'correlatedIdentifierType': 'TOID', 'searchedIdentifierVersionDate': 'synthetic-date',
            'searchedIdentifierVersionNumber': 1, 'correlatedIdentifiers': [
                {'identifier': 'osgb0000000000000001', 'confidence': 'native-version-label',
                 'correlationIdentifier': 'synthetic-correlation', 'versionDate': 'synthetic-target-date', 'versionNumber': 2}]}]}


def version_response():
    return {'methodIdentifier': METHOD, 'productCreationDate': 'synthetic-date',
        'identifier1Source': {'productName': 'AddressBase Premium', 'productPublicationDate': 'synthetic-publication',
                             'featureType': 'BLPU', 'identifierType': 'UPRN'},
        'identifier2Source': {'productName': 'OS MasterMap Topography Layer', 'productPublicationDate': 'synthetic-publication',
                             'featureType': 'TopographicArea', 'identifierType': 'TOID'}}


class LinkedIdentifiersTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name); self.output = self.parent / 'capture'
        self.now = datetime(2030, 1, 1, tzinfo=timezone.utc).timestamp()
        self.elapsed = 0; self.calls = []
        self.spec = {'schema': 'gis-ai-go.linked-identifiers-selection.v1',
            'operations': [copy.deepcopy(OP)], 'limits': dict(m.DEFAULT_LIMITS),
            'deadlineUtc': '2030-01-01T00:10:00Z', 'sourceProfileSha256': m.sha(m.PROFILE.read_bytes())}
        self.results = [(200, m.encoded(response()), None)]
    def clock(self): return self.elapsed
    def wall(self): return self.now + self.elapsed
    def sleep(self, seconds): self.elapsed += seconds
    def transport(self, path, key, maximum, timeout):
        self.calls.append((path, key, maximum, timeout)); self.elapsed += 0.1
        return self.results.pop(0)
    def run_capture(self, **kwargs):
        return m.capture(self.spec, self.output, key=KEY, clock=self.clock,
            wall_clock=self.wall, sleep=self.sleep, transport=kwargs.pop('transport', self.transport), **kwargs)
    def test_closed_selection_and_both_receipt_states_validate(self):
        schema = json.loads((m.ROOT / 'okf-plus/schemas/linked-identifiers.schema.json').read_text())
        validator = Draft202012Validator(schema)
        validator.validate(self.spec)
        validator.validate(self.run_capture())
        self.output = self.parent / 'failed'
        self.results = [(429, b'', None)]
        validator.validate(self.run_capture())

    def test_complete_capture_replay_and_private_modes(self):
        result = self.run_capture(); self.assertTrue(result['complete'])
        self.assertEqual(len(self.calls), 1); self.assertNotIn(KEY, self.calls[0][0])
        first = (self.output / 'observation-0000.json').read_bytes()
        self.assertTrue(self.run_capture()['complete']); self.assertEqual(len(self.calls), 1)
        self.assertEqual(first, (self.output / 'observation-0000.json').read_bytes())
        self.assertEqual(self.output.stat().st_mode & 0o777, 0o700)
        for path in self.output.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertNotIn(KEY.encode(), path.read_bytes())
    def test_full_relationship_versions_and_no_equivalence(self):
        self.run_capture(); observed = json.loads((self.output / 'observation-0000.json').read_bytes())
        self.assertEqual(observed['edges'][0]['confidence'], 'native-version-label')
        self.assertEqual(observed['edges'][0]['targetVersion']['versionNumber'], 2)
        self.assertEqual(observed['edges'][0]['searchedVersion']['searchedIdentifierVersionNumber'], 1)
        for key in ('snapshotIsolation', 'fieldEquivalence', 'geometryEquivalence', 'containmentEstablished'):
            self.assertFalse(observed[key])
    def test_empty_response_is_scoped_success(self):
        body = response(); body['correlations'] = []
        self.results = [(200, m.encoded(body), None)]
        self.assertTrue(self.run_capture()['complete'])
        observed = json.loads((self.output / 'observation-0000.json').read_bytes())
        self.assertEqual(observed['edges'], []); self.assertEqual(observed['scope'], 'complete-selected-response')
    def test_expired_deadline_never_calls_transport(self):
        self.spec['deadlineUtc'] = '2029-12-31T23:59:59Z'
        self.assertEqual(self.run_capture()['reason'], 'deadline-or-wall-budget'); self.assertEqual(self.calls, [])
    def test_deadline_rechecked_after_reservation(self):
        original = m.write_private
        def slow(path, raw, **kwargs):
            original(path, raw, **kwargs)
            if path.name == 'receipt.json': self.elapsed += 1000
        with patch.object(m, 'write_private', side_effect=slow):
            self.assertEqual(self.run_capture()['reason'], 'deadline-after-reservation')
        self.assertEqual(self.calls, [])
    def test_deadline_after_response_is_not_success(self):
        def late(*args): self.elapsed += 1000; return self.results.pop(0)
        self.assertFalse(self.run_capture(transport=late)['complete'])
        self.assertFalse((self.output / 'response-0000.json').exists())
    def test_reservation_and_uncertain_stop_are_durable(self):
        def crash(*args):
            receipt = json.loads((self.output / 'receipt.json').read_bytes())
            self.assertEqual(receipt['attempts'][0]['status'], 'pending')
            self.assertEqual(receipt['attempts'][0]['chargedBytes'], self.spec['limits']['responseBytes'])
            raise TimeoutError('secret ' + KEY)
        self.assertEqual(self.run_capture(transport=crash)['reason'], 'transport-uncertain')
        self.assertEqual(self.run_capture()['reason'], 'prior-failure-or-uncertain-attempt')
        self.assertEqual(self.calls, [])
    def test_http_failures_never_retry_or_become_empty_success(self):
        for status in (301, 307, 401, 403, 404, 429, 503):
            with self.subTest(status=status):
                self.output = self.parent / str(status)
                self.results = [(status, b'', None)]
                result = self.run_capture(); self.assertFalse(result['complete'])
                count = len(self.calls); self.run_capture(); self.assertEqual(len(self.calls), count)
    def test_byte_ceiling_preserves_incomplete_reservation(self):
        self.spec['limits']['responseBytes'] = 20
        self.results = [(200, b'x' * 20, None)]
        self.assertFalse(self.run_capture()['complete']); self.assertFalse((self.output / 'response-0000.json').exists())
    def test_request_ceiling_persists_across_resume(self):
        self.spec['operations'].append({'kind': 'version', 'method': METHOD})
        self.spec['limits']['maxRequests'] = 1
        self.assertEqual(self.run_capture()['reason'], 'request-budget')
        self.assertEqual(self.run_capture()['reason'], 'request-budget'); self.assertEqual(len(self.calls), 1)
    def test_changed_selection_or_budgets_cannot_replenish_capture(self):
        self.run_capture(); self.spec['limits']['maxBytes'] -= 1
        with self.assertRaisesRegex(ValueError, 'Immutable'): self.run_capture()
    def test_tampered_response_or_observation_refused(self):
        for name in ('response-0000.json', 'observation-0000.json'):
            self.output = self.parent / name.replace('.', '-')
            self.results = [(200, m.encoded(response()), None)]; self.run_capture()
            (self.output / name).write_bytes(b'{}')
            with self.assertRaises(ValueError): self.run_capture()
    def test_source_profile_binding_and_closed_inputs(self):
        for change in ({'sourceProfileSha256': '0' * 64}, {'url': 'https://evil.invalid'}, {'deadlineUtc': '2030-01-01'}):
            with self.subTest(change=change):
                value = copy.deepcopy(self.spec); value.update(change)
                with self.assertRaises(ValueError): m.validate_selection(value)
        for path in ('../other', 'id?key=x', 'id%2fother', 'id\\other', 'https://evil.invalid', 'x\nHeader'):
            with self.assertRaises(ValueError): m.route({'kind': 'feature', 'featureType': 'BLPU', 'id': path})
        with self.assertRaises(ValueError): m.route({'kind': 'untyped', 'id': '1'})
    def test_boolean_or_excessive_budgets_refused(self):
        for key, value in (('maxRequests', True), ('maxBytes', 0), ('maxWallSeconds', 301), ('responseBytes', 1048577), ('spacingSeconds', 2)):
            selected = copy.deepcopy(self.spec); selected['limits'][key] = value
            with self.assertRaises(ValueError): m.validate_selection(selected)
    def test_raw_and_escaped_key_reflection_never_retained(self):
        for escaped in (False, True):
            self.output = self.parent / str(escaped)
            body = response(); body['correlations'][0]['correlatedIdentifiers'][0]['confidence'] = KEY
            raw = m.encoded(body)
            if escaped: raw = raw.replace(KEY.encode(), ''.join('\\u%04x' % ord(c) for c in KEY).encode())
            self.results = [(200, raw, None)]
            self.assertFalse(self.run_capture()['complete'])
            self.assertFalse((self.output / 'response-0000.json').exists())
            self.assertNotIn(KEY, (self.output / 'receipt.json').read_text())
    def test_contract_mismatch_retains_private_diagnostic_without_success(self):
        body = response(); body['newProviderField'] = 'synthetic-new-value'
        raw = m.encoded(body); self.results = [(200, raw, None)]
        result = self.run_capture()
        self.assertFalse(result['complete']); self.assertEqual(result['reason'], 'response-contract-refused')
        attempt = result['attempts'][0]
        self.assertEqual(attempt['status'], 'diagnostic'); self.assertEqual(attempt['diagnosticSha256'], m.sha(raw))
        self.assertEqual(attempt['diagnosticBytes'], len(raw))
        self.assertEqual(attempt['chargedBytes'], self.spec['limits']['responseBytes'])
        self.assertEqual((self.output / 'diagnostic-0000.json').read_bytes(), raw)
        self.assertFalse((self.output / 'observation-0000.json').exists())
        self.assertNotIn('synthetic-new-value', (self.output / 'receipt.json').read_text())
        self.assertEqual(self.run_capture()['reason'], 'prior-failure-or-uncertain-attempt')
        self.assertEqual(len(self.calls), 1)
        schema = json.loads((m.ROOT / 'okf-plus/schemas/linked-identifiers.schema.json').read_text())
        Draft202012Validator(schema).validate(result)
        (self.output / 'diagnostic-0000.json').write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError, 'diagnostic checksum'): self.run_capture()

    def test_malformed_or_encoded_reflected_diagnostic_is_never_written(self):
        for variant in ('malformed', 'encoded-reflection'):
            self.output = self.parent / variant
            if variant == 'malformed': raw = b'{broken json'
            else:
                body = response(); body['newProviderField'] = KEY
                raw = m.encoded(body).replace(KEY.encode(), ''.join('\\u%04x' % ord(c) for c in KEY).encode())
            self.results = [(200, raw, None)]
            self.assertFalse(self.run_capture()['complete'])
            self.assertEqual(list(self.output.glob('diagnostic-*')), [])
            self.assertFalse((self.output / 'response-0000.json').exists())

    def test_schema_defects_do_not_grant_unknown_aliases(self):
        version = {'kind': 'version', 'method': METHOD}; body = version_response()
        self.assertEqual(m.validate_response(version, body), body)
        body['methodIdentfier'] = body.pop('methodIdentifier')
        with self.assertRaises(ValueError): m.validate_response(version, body)
        body = response(); del body['correlations'][0]['correlatedIdentifiers'][0]['confidence']
        with self.assertRaises(ValueError): m.validate_response(OP, body)
    def test_wrong_searched_type_or_identifier_is_refused(self):
        for key, value in (('identifier', 'different'), ('featureType', 'Street')):
            body = response(); body['linkedIdentifier'][key] = value
            with self.assertRaises(ValueError): m.validate_response(OP, body)
        operation = {'kind': 'identifier', 'identifierType': 'USRN', 'id': OP['id']}
        with self.assertRaises(ValueError): m.validate_response(operation, response())
    def test_unknown_fields_and_excessive_edges_are_not_silently_dropped(self):
        body = response(); body['geometry'] = {'coordinates': [0, 0]}
        with self.assertRaises(ValueError): m.validate_response(OP, body)
        body = response(); body['correlations'][0]['correlatedIdentifiers'] *= 1001
        with self.assertRaises(ValueError): m.validate_response(OP, body)
    def test_strict_json_duplicate_nonfinite_depth_and_utf8(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":1e999}', b'"\xff"', b'[' * 30 + b'0' + b']' * 30):
            with self.assertRaises(ValueError): m.strict_json(raw)
    def test_one_writer_and_symlink_refusal(self):
        with m.writer(self.output):
            with self.assertRaisesRegex(ValueError, 'active writer'): self.run_capture()
        link = self.parent / 'link'; link.symlink_to(self.output, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlinks'): m.capture(self.spec, link, key=KEY)
    def test_hardlink_or_nonregular_lock_refused(self):
        self.output.mkdir(mode=0o700); target = self.parent / 'target'; target.write_text('x'); target.chmod(0o600)
        os.link(target, self.output / 'writer.lock')
        with self.assertRaisesRegex(ValueError, 'writer lock'): self.run_capture()
    def test_durability_failure_prevents_network(self):
        with patch.object(m.os, 'fsync', side_effect=OSError('synthetic fsync failure')):
            with self.assertRaises(OSError): self.run_capture()
        self.assertEqual(self.calls, [])
    def test_unmarked_output_never_overwritten(self):
        self.output.mkdir(mode=0o700); (self.output / 'mine').write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'Unmarked'): self.run_capture()
        self.assertEqual((self.output / 'mine').read_text(), 'preserve')
    def test_transport_header_only_no_proxy_redirect_or_error_text(self):
        reply = Mock(); reply.status = 200; reply.read.return_value = b'{}'
        reply.headers = Message(); reply.headers['Content-Type'] = 'application/json'
        opener = MagicMock(); opener.open.return_value.__enter__.return_value = reply
        with patch.object(m, 'build_opener', return_value=opener) as build:
            self.assertEqual(m.fetch(m.route(OP), KEY, 100, 10), (200, b'{}', None))
            request = opener.open.call_args.args[0]
            self.assertEqual(request.get_header('Key'), KEY); self.assertNotIn(KEY, request.full_url)
            self.assertEqual(build.call_args.args[0].proxies, {})
            self.assertIsInstance(build.call_args.args[1], m.NoRedirect)
        self.assertIsNone(m.NoRedirect().redirect_request(None, None, 307, '', {}, 'https://evil.invalid'))
        failure = HTTPError('https://evil.invalid/?key=' + KEY, 403, KEY, {}, None)
        opener.open.side_effect = failure
        with patch.object(m, 'build_opener', return_value=opener): self.assertEqual(m.fetch(m.route(OP), KEY, 100, 10), (403, b'', None))
    def test_native_target_version_wrong_types_refused(self):
        for key, bad in (('versionDate', None), ('versionDate', []), ('versionNumber', True), ('versionNumber', '2')):
            body = response(); body['correlations'][0]['correlatedIdentifiers'][0][key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError): m.validate_response(OP, body)
        body = response(); item = body['correlations'][0]['correlatedIdentifiers'][0]
        del item['versionDate']; del item['versionNumber']
        self.assertEqual(m.graph(OP, body, '1' * 64, '2030-01-01T00:00:00Z')['edges'][0]['targetVersion'], {})

    def test_failed_media_or_encoding_stops_cleanly_on_resume(self):
        for failure in ('unsupported-media-type', 'unsupported-encoding'):
            self.output = self.parent / failure
            self.results = [(200, b'', failure)]
            self.assertFalse(self.run_capture()['complete'])
            count = len(self.calls)
            self.assertEqual(self.run_capture()['reason'], 'prior-failure-or-uncertain-attempt')
            self.assertEqual(len(self.calls), count)

    def test_method_endpoint_contradiction_refused(self):
        body = response()
        body['correlations'][0]['correlatedFeatureType'] = 'RoadLink'
        with self.assertRaisesRegex(ValueError, 'endpoints'): m.validate_response(OP, body)
        body = version_response(); body['identifier2Source']['featureType'] = 'RoadLink'
        with self.assertRaisesRegex(ValueError, 'endpoints'):
            m.validate_response({'kind': 'version', 'method': METHOD}, body)

    def test_product_name_must_be_one_of_source_declared_enum(self):
        body = version_response(); body['identifier1Source']['productName'] = 'Invented synthetic product'
        with self.assertRaises(ValueError): m.validate_response({'kind': 'version', 'method': METHOD}, body)

    def test_real_http_response_framing_completeness(self):
        class Socket:
            def __init__(self, raw): self.raw = raw
            def makefile(self, mode): return io.BytesIO(self.raw)
        body = m.encoded(response())
        cases = [
            (b'Content-Length: 9999\r\n', body, False),
            (b'Content-Length: ' + str(len(body)).encode() + b'\r\n', body, True),
            (b'Content-Length: 1\r\nContent-Length: 2\r\n', body, False),
            (b'Content-Length: +2\r\n', body, False),
            (b'Content-Length: 2\r\nTransfer-Encoding: chunked\r\n', b'0\r\n\r\n', False),
            (b'Transfer-Encoding: chunked\r\n', ('%x' % len(body)).encode() + b'\r\n' + body + b'\r\n0\r\n\r\n', True),
            (b'Transfer-Encoding: chunked\r\n', ('%x' % len(body)).encode() + b'\r\n' + body + b'\r\n', False),
            (b'Connection: close\r\n', body, True),
        ]
        for headers, wire_body, expected in cases:
            with self.subTest(headers=headers, expected=expected):
                raw = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n' + headers + b'\r\n' + wire_body
                reply = http.client.HTTPResponse(Socket(raw)); reply.begin()
                opener = Mock(); opener.open.return_value = reply
                with patch.object(m, 'build_opener', return_value=opener):
                    status, retained, failure = m.fetch(m.route(OP), KEY, 20000, 10)
                self.assertEqual(status == 200 and failure is None, expected)
                if expected: self.assertEqual(retained, body)
                else: self.assertEqual(retained, b'')

    def test_empty_response_still_requires_source_backed_node_pair(self):
        body = response(); body['correlations'] = []; body['linkedIdentifier']['identifierType'] = 'GUID'
        with self.assertRaisesRegex(ValueError, 'pairing'): m.validate_response(OP, body)

    def test_optional_publication_name_preserves_empty_and_absent(self):
        body = version_response()
        body['productPublicationName'] = ''
        body['identifier1Source']['productPublicationName'] = ''
        body['identifier2Source']['productPublicationName'] = ''
        self.spec['operations'] = [{'kind': 'version', 'method': METHOD}]
        self.results = [(200, m.encoded(body), None)]
        self.assertTrue(self.run_capture()['complete'])
        observed = json.loads((self.output / 'observation-0000.json').read_bytes())
        self.assertEqual(observed['productVersion'], body)
        schema = json.loads((m.ROOT / 'okf-plus/schemas/linked-identifiers.schema.json').read_text())
        Draft202012Validator(schema).validate(observed)
        absent = version_response()
        self.assertNotIn('productPublicationName', m.validate_response(self.spec['operations'][0], absent))

    def test_optional_publication_name_retains_type_and_text_bounds(self):
        for scope in (None, 'identifier1Source', 'identifier2Source'):
            for bad in (None, False, 1, [], {}, 'x' * 257, '\n'):
                with self.subTest(scope=scope, bad=repr(bad)):
                    body = version_response()
                    target = body if scope is None else body[scope]
                    target['productPublicationName'] = bad
                    with self.assertRaises(ValueError):
                        m.validate_response({'kind': 'version', 'method': METHOD}, body)

    def test_version_metadata_capture(self):
        self.spec['operations'] = [{'kind': 'version', 'method': METHOD}]
        self.results = [(200, m.encoded(version_response()), None)]
        self.assertTrue(self.run_capture()['complete'])
        observed = json.loads((self.output / 'observation-0000.json').read_bytes())
        self.assertEqual(observed['productVersion']['methodIdentifier'], METHOD); self.assertEqual(observed['edges'], [])


if __name__ == '__main__': unittest.main()
