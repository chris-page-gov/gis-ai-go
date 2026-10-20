"""Bounded private OS Linked Identifiers capture; no hosted tool or graph crawl.

Provider bytes and identifiers remain private. A receipt binds one explicitly
selected observation, not entitlement, temporal equivalence or spatial truth.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import time
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler, ProxyHandler

from .harvest import deadline

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://api.os.uk/search/links/v1/'
PROFILE = ROOT / 'okf-plus/profile/os-linked-identifiers-capabilities.json'
FEATURES = {'BLPU', 'ORRoadNode', 'ORRoadLink', 'Road', 'RoadLink', 'Street', 'TopographicArea'}
IDENTIFIERS = {'GUID', 'TOID', 'UPRN', 'USRN'}
NODE_TYPES = {'BLPU': 'UPRN', 'Street': 'USRN', 'ORRoadLink': 'GUID',
              'ORRoadNode': 'GUID', 'Road': 'TOID', 'RoadLink': 'TOID', 'TopographicArea': 'TOID'}
PRODUCTS = {'AddressBase Premium', 'OS MasterMap Highways Network - Roads',
            'OS MasterMap Topography Layer', 'OS Open Roads'}
METHODS = {
    'RoadLink_TOID_TopographicArea_TOID_2', 'Road_TOID_TopographicArea_TOID_3',
    'Street_USRN_TopographicArea_TOID_4', 'BLPU_UPRN_TopographicArea_TOID_5',
    'RoadLink_TOID_Road_TOID_7', 'RoadLink_TOID_Street_USRN_8',
    'BLPU_UPRN_RoadLink_TOID_9', 'Road_TOID_Street_USRN_10',
    'BLPU_UPRN_Street_USRN_11', 'ORRoadLink_GUID_RoadLink_TOID_12',
    'ORRoadNode_GUID_RoadLink_TOID_13',
}
MAX_JSON = 2 * 1024 * 1024
DEFAULT_LIMITS = {'maxRequests': 20, 'maxBytes': 8 * 1024 * 1024,
                  'maxWallSeconds': 300, 'responseBytes': 1024 * 1024,
                  'spacingSeconds': 2.05}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def closed(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ValueError('Unexpected or missing contract fields')


def text(value, maximum=256, *, minimum=1):
    if (not isinstance(value, str) or not minimum <= len(value) <= maximum
            or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in value)):
        raise ValueError('Invalid bounded source text')
    return value


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,36}', value):
        raise ValueError('Invalid native identifier')
    return value


def enum(value, values):
    if not isinstance(value, str) or value not in values:
        raise ValueError('Unadmitted source type or method')
    return value


def utc(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value):
        raise ValueError('An explicit UTC deadline with seconds is required')
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        raise ValueError('Invalid UTC deadline') from None


def route(operation):
    if not isinstance(operation, dict):
        raise ValueError('Invalid operation')
    kind = operation.get('kind')
    if kind == 'identifier':
        closed(operation, ('kind', 'identifierType', 'id'))
        return 'identifierTypes/' + enum(operation['identifierType'], IDENTIFIERS) + '/' + identifier(operation['id'])
    if kind == 'feature':
        closed(operation, ('kind', 'featureType', 'id'))
        return 'featureTypes/' + enum(operation['featureType'], FEATURES) + '/' + identifier(operation['id'])
    if kind == 'version':
        closed(operation, ('kind', 'method'))
        return 'productVersionInfo/' + enum(operation['method'], METHODS)
    raise ValueError('Unadmitted operation')


def validate_selection(value):
    closed(value, ('schema', 'operations', 'limits', 'deadlineUtc', 'sourceProfileSha256'))
    if value['schema'] != 'gis-ai-go.linked-identifiers-selection.v1':
        raise ValueError('Unknown selection schema')
    utc(value['deadlineUtc'])
    if value['sourceProfileSha256'] != sha(PROFILE.read_bytes()):
        raise ValueError('Capability profile binding differs')
    operations = value['operations']
    if not isinstance(operations, list) or not 1 <= len(operations) <= 20:
        raise ValueError('Operation count must be 1..20')
    routes = [route(item) for item in operations]
    if len(set(routes)) != len(routes):
        raise ValueError('Duplicate selected operation')
    limits = value['limits']
    closed(limits, DEFAULT_LIMITS)
    for name in ('maxRequests', 'maxBytes', 'maxWallSeconds', 'responseBytes'):
        if type(limits[name]) is not int or not 1 <= limits[name] <= DEFAULT_LIMITS[name]:
            raise ValueError('Budget exceeds the admitted positive integer ceiling')
    spacing = limits['spacingSeconds']
    if type(spacing) not in (int, float) or not math.isfinite(spacing) or not 2.05 <= spacing <= 60:
        raise ValueError('Request spacing must be 2.05..60 seconds')
    return value


def strict_json(raw):
    if len(raw) > MAX_JSON:
        raise ValueError('JSON byte bound exceeded')
    def pairs(items):
        result = {}
        for key, item in items:
            if key in result:
                raise ValueError('Duplicate JSON property')
            result[key] = item
        return result
    def invalid(_value):
        raise ValueError('Non-finite JSON value')
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)
        def walk(item, depth=0):
            if depth > 24:
                raise ValueError('JSON depth bound exceeded')
            if isinstance(item, dict):
                for key, child in item.items():
                    text(key); walk(child, depth + 1)
            elif isinstance(item, list):
                if len(item) > 2000:
                    raise ValueError('JSON array bound exceeded')
                for child in item: walk(child, depth + 1)
            elif isinstance(item, str):
                if len(item) > 4096 or any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                    raise ValueError('JSON text bound exceeded')
            elif isinstance(item, float) and not math.isfinite(item):
                raise ValueError('Non-finite JSON value')
        walk(value)
        return value
    except (UnicodeError, RecursionError, json.JSONDecodeError):
        raise ValueError('Invalid bounded UTF-8 JSON') from None


def version_fields(value, prefix=''):
    keys = (prefix + 'VersionDate', prefix + 'VersionNumber') if prefix else ('versionDate', 'versionNumber')
    for key in keys:
        if key not in value: continue
        item = value[key]
        if key.endswith('Date'):
            text(item, 128)  # Native lexical form; no inferred validity interval.
        elif type(item) not in (int, float) or not math.isfinite(item) or item < 0:
            raise ValueError('Invalid native version number')


def node_type(value):
    enum(value['identifierType'], IDENTIFIERS); enum(value['featureType'], FEATURES)
    if NODE_TYPES[value['featureType']] != value['identifierType']:
        raise ValueError('Identifier and feature type pairing is not source-backed')


def node(value):
    closed(value, ('identifier', 'identifierType', 'featureType'))
    identifier(value['identifier']); node_type(value)
    return value


def method_definition(method):
    return next(item for item in strict_json(PROFILE.read_bytes())['methods']
                if item['correlationMethodIdentifier'] == enum(method, METHODS))


def validate_method_pair(method, source, target):
    ends = method_definition(method)['endpoints']
    pair = {(source['featureType'], source['identifierType']),
            (target['featureType'], target['identifierType'])}
    expected = {(item['featureType'], item['identifierType']) for item in ends}
    if pair != expected:
        raise ValueError('Observed typed endpoints contradict the declared method')


def validate_response(operation, value):
    """Validate complete selected responses; unknown fields fail, never disappear."""
    if operation['kind'] == 'version':
        # The source required-list typo is recorded in the capability profile.
        # Admit only its declared methodIdentifier property, not an invented alias.
        closed(value, ('methodIdentifier', 'productCreationDate', 'identifier1Source', 'identifier2Source'),
               ('productPublicationName',))
        if value['methodIdentifier'] != operation['method']:
            raise ValueError('Version metadata method differs from selection')
        text(value['productCreationDate'], 128)
        if 'productPublicationName' in value: text(value['productPublicationName'], minimum=0)
        for name in ('identifier1Source', 'identifier2Source'):
            source = value[name]
            closed(source, ('productName', 'productPublicationDate', 'featureType', 'identifierType'), ('productPublicationName',))
            enum(source['productName'], PRODUCTS); text(source['productPublicationDate'], 128)
            enum(source['featureType'], FEATURES); enum(source['identifierType'], IDENTIFIERS)
            if 'productPublicationName' in source: text(source['productPublicationName'], minimum=0)
        validate_method_pair(operation['method'], value['identifier1Source'], value['identifier2Source'])
        return value
    closed(value, ('linkedIdentifier', 'correlations'))
    searched = node(value['linkedIdentifier'])
    if searched['identifier'] != operation['id']:
        raise ValueError('Searched identifier differs from selection')
    kind_key = 'identifierType' if operation['kind'] == 'identifier' else 'featureType'
    if searched[kind_key] != operation[kind_key]:
        raise ValueError('Searched type differs from selection')
    if not isinstance(value['correlations'], list) or len(value['correlations']) > 32:
        raise ValueError('Correlation group bound exceeded')
    total = 0
    for group in value['correlations']:
        closed(group, ('correlationMethodIdentifier', 'correlatedFeatureType', 'correlatedIdentifierType', 'correlatedIdentifiers'),
               ('searchedIdentifierVersionDate', 'searchedIdentifierVersionNumber'))
        enum(group['correlationMethodIdentifier'], METHODS); enum(group['correlatedFeatureType'], FEATURES)
        enum(group['correlatedIdentifierType'], IDENTIFIERS); version_fields(group, 'searchedIdentifier')
        validate_method_pair(group['correlationMethodIdentifier'], searched,
            {'featureType': group['correlatedFeatureType'], 'identifierType': group['correlatedIdentifierType']})
        if not isinstance(group['correlatedIdentifiers'], list): raise ValueError('Expected correlated identifier array')
        for item in group['correlatedIdentifiers']:
            closed(item, ('identifier', 'confidence', 'correlationIdentifier'), ('versionDate', 'versionNumber'))
            identifier(item['identifier']); text(item['confidence'], 128); text(item['correlationIdentifier'], 256)
            version_fields(item)
            total += 1
            if total > 1000: raise ValueError('Relationship count bound exceeded')
    return value


def reject_reflection(value, key):
    if isinstance(value, dict):
        for name, item in value.items():
            reject_reflection(name, key); reject_reflection(item, key)
    elif isinstance(value, list):
        for item in value: reject_reflection(item, key)
    elif isinstance(value, str) and key in value:
        raise ValueError('Credential reflection refused')


def graph(operation, value, response_sha256, observed_at):
    """Directed observations only: do not infer inverses, transitivity or equivalence."""
    validate_response(operation, value)
    base = {'schema': 'gis-ai-go.linked-identifiers-observation.v1', 'operation': operation,
            'responseSha256': response_sha256, 'observedAt': observed_at,
            'sourceProfileSha256': sha(PROFILE.read_bytes()),
            'scope': 'complete-selected-response', 'snapshotIsolation': False,
            'fieldEquivalence': False, 'geometryEquivalence': False, 'containmentEstablished': False}
    if operation['kind'] == 'version':
        return dict(base, productVersion=value, edges=[])
    edges = []
    for gi, group in enumerate(value['correlations']):
        for ii, target in enumerate(group['correlatedIdentifiers']):
            edges.append({'source': value['linkedIdentifier'],
                'target': {'identifier': target['identifier'], 'identifierType': group['correlatedIdentifierType'],
                           'featureType': group['correlatedFeatureType']},
                'method': group['correlationMethodIdentifier'], 'confidence': target['confidence'],
                'correlationIdentifier': target['correlationIdentifier'],
                'searchedVersion': {k: v for k, v in group.items() if k.startswith('searchedIdentifierVersion')},
                'targetVersion': {k: v for k, v in target.items() if k.startswith('version')},
                'sourcePointer': f'/correlations/{gi}/correlatedIdentifiers/{ii}'})
    return dict(base, searched=value['linkedIdentifier'], edges=edges,
                emptyGroups=sum(not group['correlatedIdentifiers'] for group in value['correlations']))


def safe_path(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        if part.is_symlink(): raise ValueError('Symlinks are forbidden')
    return path


def read_regular(path, maximum=MAX_JSON):
    path = safe_path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > maximum:
            raise ValueError('Expected bounded single-link regular file')
        raw = b''
        while len(raw) <= maximum:
            part = os.read(fd, min(65536, maximum + 1 - len(raw)))
            if not part: break
            raw += part
        after = os.fstat(fd)
        if ((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                or len(raw) != before.st_size):
            raise ValueError('Source changed during bounded read')
        return raw
    finally:
        os.close(fd)


def sync(directory):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try: os.fsync(fd)
    finally: os.close(fd)


def write_private(path, raw, *, replace=False):
    path = safe_path(path)
    if path.exists() and not replace: raise ValueError('Existing file is preserved')
    if path.exists(): read_regular(path)
    fd, temp = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), 0o600); stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        if replace: os.replace(temp, path)
        else: os.link(temp, path, follow_symlinks=False)
        os.unlink(temp) if os.path.exists(temp) else None
        sync(path.parent)
    finally:
        if os.path.exists(temp): os.unlink(temp)


@contextmanager
def writer(directory):
    directory = safe_path(directory)
    if not directory.exists():
        if not directory.parent.is_dir(): raise ValueError('Output parent must already exist')
        directory.mkdir(mode=0o700); sync(directory.parent)
    mode = directory.stat()
    if not stat.S_ISDIR(mode.st_mode) or mode.st_uid != os.getuid() or stat.S_IMODE(mode.st_mode) != 0o700:
        raise ValueError('Expected owner-only output directory')
    lock = safe_path(directory / 'writer.lock')
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
            raise ValueError('Invalid writer lock')
        try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError('An active writer already owns this capture') from None
        yield directory
    finally: os.close(fd)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(path, key, maximum, timeout):
    # Accept only an internally constructed path, including at the transport seam.
    if path not in {route({'kind': 'version', 'method': method}) for method in METHODS}:
        parts = path.split('/')
        if len(parts) != 3: raise ValueError('Unadmitted transport route')
        if parts[0] == 'identifierTypes': route({'kind': 'identifier', 'identifierType': parts[1], 'id': parts[2]})
        elif parts[0] == 'featureTypes': route({'kind': 'feature', 'featureType': parts[1], 'id': parts[2]})
        else: raise ValueError('Unadmitted transport route')
    request = Request(BASE + path, headers={'key': key, 'Accept': 'application/json',
        'Accept-Encoding': 'identity', 'User-Agent': 'GIS-AI-GO-OKF-Plus/0.1 linked-identifiers'})
    try:
        with build_opener(ProxyHandler({}), NoRedirect()).open(request, timeout=timeout) as response:
            if response.headers.get('Content-Encoding', 'identity').lower() != 'identity': return 200, b'', 'unsupported-encoding'
            if response.headers.get_content_type() != 'application/json': return 200, b'', 'unsupported-media-type'
            lengths = response.headers.get_all('Content-Length', [])
            transfers = response.headers.get_all('Transfer-Encoding', [])
            if (len(lengths) > 1 or len(transfers) > 1 or (lengths and transfers)
                    or (transfers and transfers[0].strip().lower() != 'chunked')):
                return 200, b'', 'invalid-framing'
            declared = None
            if lengths:
                if not re.fullmatch(r'[0-9]{1,10}', lengths[0]): return 200, b'', 'invalid-framing'
                declared = int(lengths[0])
                if declared >= maximum: return 200, b'', 'invalid-framing'
            # http.client verifies chunk termination when a bounded read reaches
            # EOF. Without length/transfer framing, EOF is the message delimiter.
            raw = response.read(maximum)
            if declared is not None and len(raw) != declared:
                return 200, b'', 'invalid-framing'
            return response.status, raw, None
    except HTTPError as error:
        status = error.code
        error.close()  # No reflective error body, redirect URL or headers retained.
        return status, b'', None
    except Exception:
        return 0, b'', 'transport-uncertain'


def capture(selection, output, *, key, transport=fetch, clock=time.monotonic,
            wall_clock=time.time, sleep=time.sleep):
    selection = strict_json(encoded(validate_selection(selection)))
    if not isinstance(key, str) or not 8 <= len(key) <= 512 or not re.fullmatch(r'[!-~]+', key):
        raise ValueError('A private printable API key binding is required')
    selection_hash = sha(encoded(selection)); limits = selection['limits']
    end = utc(selection['deadlineUtc'])
    with writer(output) as directory:
        ledger_path = directory / 'receipt.json'
        if ledger_path.exists():
            ledger = strict_json(read_regular(ledger_path))
            closed(ledger, ('schema', 'selection', 'selectionSha256', 'attempts', 'reason', 'complete'))
            if ledger['schema'] != 'gis-ai-go.linked-identifiers-receipt.v1' or ledger['selection'] != selection or ledger['selectionSha256'] != selection_hash:
                raise ValueError('Immutable capture selection differs')
        else:
            if set(p.name for p in directory.iterdir()) != {'writer.lock'}:
                raise ValueError('Unmarked existing output is preserved')
            ledger = {'schema': 'gis-ai-go.linked-identifiers-receipt.v1', 'selection': selection,
                      'selectionSha256': selection_hash, 'attempts': [], 'reason': 'not-started', 'complete': False}
        def save(reason, complete=False):
            ledger.update(reason=reason, complete=complete)
            write_private(ledger_path, encoded(ledger), replace=ledger_path.exists())
            return ledger
        completed = {}
        for index, attempt in enumerate(ledger['attempts']):
            closed(attempt, ('operationIndex', 'status', 'chargedBytes', 'chargedWallSeconds'),
                   ('responseSha256', 'responseBytes', 'observedAt', 'observationSha256', 'failure',
                    'diagnosticSha256', 'diagnosticBytes', 'diagnosticReason'))
            if (type(attempt['operationIndex']) is not int or not 0 <= attempt['operationIndex'] < len(selection['operations'])
                    or type(attempt['chargedBytes']) is not int or not 0 <= attempt['chargedBytes'] <= limits['responseBytes']
                    or type(attempt['chargedWallSeconds']) not in (int, float)
                    or not math.isfinite(attempt['chargedWallSeconds']) or not 0 <= attempt['chargedWallSeconds'] <= limits['maxWallSeconds']):
                raise ValueError('Invalid retained attempt allowance')
            if attempt['status'] == 'diagnostic':
                raw = read_regular(directory / f'diagnostic-{index:04}.json', limits['responseBytes'])
                if sha(raw) != attempt.get('diagnosticSha256') or len(raw) != attempt.get('diagnosticBytes'):
                    raise ValueError('Retained diagnostic checksum differs')
                reject_reflection(strict_json(raw), key)
            if attempt['status'] != 200: return save('prior-failure-or-uncertain-attempt')
            if attempt['operationIndex'] in completed: raise ValueError('Duplicate completed operation')
            raw = read_regular(directory / f'response-{index:04}.json', limits['responseBytes'])
            if sha(raw) != attempt.get('responseSha256') or len(raw) != attempt.get('responseBytes') or len(raw) != attempt['chargedBytes']:
                raise ValueError('Retained response checksum or charge differs')
            expected = graph(selection['operations'][attempt['operationIndex']], strict_json(raw), sha(raw), attempt['observedAt'])
            observed = read_regular(directory / f'observation-{index:04}.json')
            if sha(observed) != attempt.get('observationSha256') or observed != encoded(expected):
                raise ValueError('Retained observation differs from full response')
            completed[attempt['operationIndex']] = True
        if (len(ledger['attempts']) > limits['maxRequests']
                or sum(item['chargedBytes'] for item in ledger['attempts']) > limits['maxBytes']
                or sum(item['chargedWallSeconds'] for item in ledger['attempts']) > limits['maxWallSeconds']):
            raise ValueError('Retained cumulative allowance exceeded')
        for operation_index, operation in enumerate(selection['operations']):
            if operation_index in completed: continue
            charged = sum(item['chargedBytes'] for item in ledger['attempts'])
            used_wall = sum(item['chargedWallSeconds'] for item in ledger['attempts'])
            if len(ledger['attempts']) >= limits['maxRequests']: return save('request-budget')
            remaining = min(limits['maxWallSeconds'] - used_wall, end - wall_clock())
            spacing = limits['spacingSeconds']
            if remaining <= spacing: return save('deadline-or-wall-budget')
            maximum = min(limits['responseBytes'], limits['maxBytes'] - charged)
            if maximum < 2: return save('byte-budget')
            start = clock(); sleep(spacing)
            remaining = min(limits['maxWallSeconds'] - used_wall - (clock() - start), end - wall_clock())
            if remaining <= 0: return save('deadline-or-wall-budget')
            timeout = min(20, remaining)
            attempt = {'operationIndex': operation_index, 'status': 'pending', 'chargedBytes': maximum,
                       'chargedWallSeconds': min(limits['maxWallSeconds'] - used_wall, spacing + timeout)}
            ledger['attempts'].append(attempt); save('request-reserved')
            # Recheck after durable reservation: fsync time cannot extend expiry.
            remaining = min(timeout, end - wall_clock(), limits['maxWallSeconds'] - used_wall - (clock() - start))
            if remaining <= 0: return save('deadline-after-reservation')
            try:
                with deadline(remaining): status, raw, failure = transport(route(operation), key, maximum, remaining)
            except Exception:
                return save('transport-uncertain')
            if type(status) is not int or not isinstance(raw, bytes) or len(raw) >= maximum:
                return save('invalid-or-bounded-response')
            if key.encode() in raw:
                return save('credential-reflection-refused')
            if failure is not None or status != 200:
                attempt['status'] = status if status not in (0, 200) else 'uncertain'
                attempt['failure'] = failure if failure in {'unsupported-encoding', 'unsupported-media-type', 'transport-uncertain', 'invalid-framing'} else 'http-failed'
                return save('rate-limited' if status == 429 else 'provider-or-transport-failure')
            if wall_clock() >= end or clock() - start + used_wall >= limits['maxWallSeconds']:
                return save('deadline-or-wall-budget')
            try:
                value = strict_json(raw)
                reject_reflection(value, key)
            except (ValueError, TypeError, KeyError, OverflowError):
                return save('malformed-or-reflected-response-refused')
            try:
                validate_response(operation, value)
            except (ValueError, TypeError, KeyError, OverflowError):
                index = len(ledger['attempts']) - 1
                write_private(directory / f'diagnostic-{index:04}.json', raw)
                attempt.update(status='diagnostic', diagnosticSha256=sha(raw), diagnosticBytes=len(raw),
                               diagnosticReason='response-contract-refused')
                return save('response-contract-refused')
            try:
                observed_at = datetime.fromtimestamp(wall_clock(), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                observation = encoded(graph(operation, value, sha(raw), observed_at))
                if len(observation) > MAX_JSON: raise ValueError('Observation output bound exceeded')
            except (ValueError, TypeError, KeyError, OverflowError):
                return save('response-contract-refused')
            index = len(ledger['attempts']) - 1
            write_private(directory / f'response-{index:04}.json', raw)
            write_private(directory / f'observation-{index:04}.json', observation)
            attempt.update(status=200, chargedBytes=len(raw), chargedWallSeconds=clock() - start,
                           responseSha256=sha(raw), responseBytes=len(raw), observedAt=observed_at,
                           observationSha256=sha(observation))
            save('response-verified')
        return save('selected-operations-complete', True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selection', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = capture(strict_json(read_regular(args.selection)), args.output, key=os.environ.get('OS_API_KEY', ''))
        print(json.dumps({'complete': result['complete'], 'reason': result['reason'], 'attempts': len(result['attempts'])}))
        return 0 if result['complete'] else 2
    except Exception:
        print(json.dumps({'complete': False, 'reason': 'local-contract-or-storage-refusal'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
