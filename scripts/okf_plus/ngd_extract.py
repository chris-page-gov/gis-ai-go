"""Bounded private NGD selection extraction. Payloads remain until profiling succeeds.

No snapshot isolation is claimed. A resumed selection retains its original cumulative
budgets; increase those budgets explicitly to continue an interrupted selection.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit, parse_qs
from urllib.request import Request, build_opener, HTTPRedirectHandler

try:
    from .harvest import deadline
except ImportError:
    from harvest import deadline

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://api.os.uk/features/ngd/ofa/v1/collections/'
CRS84 = 'http://www.opengis.net/def/crs/OGC/1.3/CRS84'
CRS = {str(n): f'http://www.opengis.net/def/crs/EPSG/0/{n}' for n in (27700, 7405, 4326, 3857)}
CRS['CRS84'] = CRS84
MAX_PAGE_BYTES = 8 * 1024 * 1024


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def sync_directory(directory):
    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def private_atomic_write(destination, raw):
    """Persist private bytes and their directory entry before returning."""
    destination = Path(destination)
    temporary = destination.with_name(destination.name + '.tmp')
    for item in (destination, temporary, *destination.parents):
        if item.is_symlink():
            raise ValueError('Symlinks are forbidden')
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, 'wb') as stream:
        os.fchmod(stream.fileno(), 0o600)
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(destination)
    sync_directory(destination.parent)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url, key, maximum, timeout):
    """Return status and bounded bytes; never expose credential-bearing exceptions."""
    maximum = min(maximum, MAX_PAGE_BYTES)
    request = Request(url, headers={'key': key, 'Accept': 'application/geo+json',
                                   'User-Agent': 'GIS-AI-GO-OKF-Plus/0.1 transient-extract'})
    try:
        with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            return response.status, response.read(maximum + 1), {'content-crs': response.headers.get('Content-Crs')}
    except HTTPError as error:
        return error.code, error.read(maximum + 1), {}
    except Exception:
        return 0, b'', {}


def selection(collection, bbox, bbox_crs, crs, osids, queryables, id_filter_operator='or'):
    if not isinstance(collection, str) or not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', collection):
        raise ValueError('Invalid collection identifier')
    if bbox_crs not in ('CRS84', '27700') or crs not in CRS:
        raise ValueError('Unsupported coordinate reference system')
    if id_filter_operator not in ('or', 'in'):
        raise ValueError('Unsupported identifier filter operator')
    if len(bbox) != 4 or any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in bbox):
        raise ValueError('Bounding box requires four finite numbers')
    if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
        raise ValueError('Bounding box must have increasing axes')
    if bbox_crs == 'CRS84' and not (-180 <= bbox[0] < bbox[2] <= 180 and -90 <= bbox[1] < bbox[3] <= 90):
        raise ValueError('CRS84 bounding box outside longitude/latitude range')
    if len(osids) > 100 or any(not isinstance(x, str) or not re.fullmatch(r'[A-Za-z0-9:_-]{1,128}', x) for x in osids):
        raise ValueError('Invalid or excessive native OS identifiers')
    ids = sorted(set(osids))
    if ids and (not isinstance(queryables, dict) or queryables.get('collectionId') != collection
                or 'osid' not in queryables.get('properties', {})):
        raise ValueError('Collection-bound queryables evidence for osid is required')
    return {'collection': collection, 'bbox': list(bbox), 'bboxCrs': bbox_crs, 'crs': crs,
            'osids': ids, 'idFilterOperator': id_filter_operator,
            'queryablesSha256': sha(encoded(queryables)) if ids else None}


def extract(collection, bbox, *, key, bbox_crs='CRS84', crs='27700', osids=(),
            queryables=None, limit=100, max_requests=10, max_bytes=32*1024*1024,
            max_wall_seconds=120, requests_per_minute=30, transport=fetch,
            clock=time.monotonic, sleep=time.sleep, refresh=False, id_filter_operator='or'):
    selected = selection(collection, bbox, bbox_crs, crs, osids, queryables, id_filter_operator)
    if not isinstance(key, str) or not key or any(c in key for c in '\r\n'):
        raise ValueError('A private API key is required')
    for value in (limit, max_requests, max_bytes, max_wall_seconds, requests_per_minute):
        if type(value) is not int or value < 1:
            raise ValueError('Budgets must be positive integers')
    if limit > 100 or requests_per_minute > 30:
        raise ValueError('Page/rate ceiling exceeded')
    selected['limit'] = limit
    directory = ROOT / 'artifacts/okf-plus/private-ngd-extractions' / sha(encoded(selected))
    # Reject symlinks in the complete path, including pre-existing parent folders.
    for path in (directory, *directory.parents):
        if path.is_symlink():
            raise ValueError('Symlinks are forbidden')
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    lock_path = directory / 'writer.lock'
    if lock_path.is_symlink():
        raise ValueError('Symlinks are forbidden')
    with lock_path.open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Selection already has an active writer') from None
        receipt_path = directory / 'receipt.json'
        if receipt_path.is_symlink():
            raise ValueError('Symlinks are forbidden')
        if refresh and receipt_path.exists():
            prior = json.loads(receipt_path.read_bytes())
            if prior.get('reason') == 'rate-limited':
                return prior
            if not prior.get('payloadDiscarded'):
                raise ValueError('Refresh requires verified payload disposal first')
            history = directory / 'history'
            if history.is_symlink():
                raise ValueError('Symlinks are forbidden')
            history.mkdir(mode=0o700, exist_ok=True)
            receipt_digest = sha(receipt_path.read_bytes())
            archive = history / (receipt_digest + '.json')
            if archive.is_symlink():
                raise ValueError('Symlinks are forbidden')
            prior_profile = ROOT / prior['profilePath']
            for item in (prior_profile, *prior_profile.parents):
                if item.is_symlink():
                    raise ValueError('Symlinks are forbidden')
            if not prior_profile.resolve().is_relative_to(ROOT / 'artifacts'):
                raise ValueError('Historical profile must remain private')
            profile_raw = prior_profile.read_bytes()
            if sha(profile_raw) != prior['profileSha256']:
                raise ValueError('Historical profile checksum mismatch')
            profile_archive = history / (receipt_digest + '.profile.json')
            if profile_archive.is_symlink():
                raise ValueError('Symlinks are forbidden')
            private_atomic_write(profile_archive, profile_raw)
            private_atomic_write(archive, receipt_path.read_bytes())
            receipt_path.unlink()
            sync_directory(directory)
        return _run(directory, selected, key, max_requests, max_bytes,
                    max_wall_seconds, requests_per_minute, transport, clock, sleep)


def _run(directory, selected, key, request_cap, byte_cap, wall_cap, rate, transport, clock, sleep):
    receipt_path = directory / 'receipt.json'
    def path(name):
        result = directory / name
        if result.is_symlink():
            raise ValueError('Symlinks are forbidden')
        return result
    receipt = {'selection': selected, 'complete': False, 'snapshotIsolation': False,
               'requests': 0, 'bytes': 0, 'wallSeconds': 0, 'pages': [], 'reason': 'not-started',
               'responseByteCeiling': MAX_PAGE_BYTES}
    if receipt_path.exists():
        receipt = json.loads(path('receipt.json').read_bytes())
        if receipt['selection'] != selected:
            raise ValueError('Selection receipt mismatch')
        if receipt.get('payloadDiscarded'):
            return dict(receipt, complete=False, reason='needs-reacquisition')
        if receipt.get('reason') == 'rate-limited':
            return receipt
    started = clock()
    previous_wall = receipt['wallSeconds']
    def save(reason):
        receipt['reason'] = reason
        receipt['wallSeconds'] = previous_wall + clock() - started
        private_atomic_write(path('receipt.json'), encoded(receipt))
        return receipt
    seen = {}
    offset = 0
    exhausted = False
    observed_matched = None
    def consume(raw):
        nonlocal observed_matched
        data = json.loads(raw)
        features = data.get('features')
        if data.get('type') != 'FeatureCollection' or not isinstance(features, list) or len(features) > selected['limit']:
            raise ValueError('invalid-page')
        if 'numberReturned' in data and (type(data['numberReturned']) is not int or data['numberReturned'] != len(features)):
            raise ValueError('returned-count-mismatch')
        matched = data.get('numberMatched')
        if matched is not None and matched != 'unknown':
            if type(matched) is not int or matched < offset + len(features):
                raise ValueError('matched-count-mismatch')
            if observed_matched is not None and matched != observed_matched:
                raise ValueError('matched-count-drift')
            observed_matched = matched
        for feature in features:
            if not isinstance(feature, dict) or feature.get('type') != 'Feature':
                raise ValueError('invalid-feature')
            properties = feature.get('properties')
            if properties is not None and not isinstance(properties, dict):
                raise ValueError('invalid-properties')
            identity = feature.get('id')
            if identity is None:
                identity = (properties or {}).get('osid')
            if not isinstance(identity, (str, int)) or isinstance(identity, bool):
                raise ValueError('missing-native-identity')
            identity = str(identity)
            digest = sha(encoded(feature))
            if identity in seen:
                raise ValueError('duplicate-drift' if seen[identity] != digest else 'duplicate-native-identity')
            seen[identity] = digest
        links = data.get('links', [])
        if not isinstance(links, list):
            raise ValueError('invalid-links')
        next_links = [x for x in links if isinstance(x, dict) and x.get('rel') == 'next']
        if len(next_links) > 1:
            raise ValueError('ambiguous-next-links')
        if next_links:
            target = urlsplit(next_links[0].get('href', ''))
            query = parse_qs(target.query)
            expected_path = urlsplit(BASE + selected['collection'] + '/items').path
            if target.scheme != 'https' or target.netloc != 'api.os.uk' or target.path != expected_path or query.get('offset') != [str(offset + len(features))]:
                raise ValueError('next-link-mismatch')
        if not features and next_links:
            raise ValueError('empty-page-with-next')
        if (not features or (isinstance(data.get('links'), list) and not next_links and len(features) < selected['limit'])) and observed_matched is not None and offset + len(features) != observed_matched:
            raise ValueError('exhaustion-count-mismatch')
        return features, not features or (isinstance(data.get('links'), list) and not next_links and len(features) < selected['limit'])
    for page in receipt['pages']:
        if not re.fullmatch(r'page-[0-9]{6}\.json', page['file']) or page['offset'] != offset:
            raise ValueError('Invalid cached page receipt')
        raw = path(page['file']).read_bytes()
        if sha(raw) != page['sha256']:
            raise ValueError('Cached page checksum mismatch')
        if len(raw) > MAX_PAGE_BYTES or page.get('responseTruncated'):
            return save('response-byte-budget' if len(raw) > MAX_PAGE_BYTES else 'byte-budget')
        if page.get('contentCrs') != CRS[selected['crs']]:
            return save('content-crs-mismatch')
        try:
            features, exhausted = consume(raw)
        except (ValueError, TypeError, AttributeError):
            return save('invalid-or-inconsistent-page')
        offset += len(features)
    if receipt.get('complete'):
        if not exhausted or not path('features.ndjson').is_file() or sha(path('features.ndjson').read_bytes()) != receipt.get('ndjsonSha256'):
            raise ValueError('Complete receipt lacks complete payload')
        return receipt
    if receipt['bytes'] > byte_cap:
        return save('byte-budget')
    if previous_wall + clock() - started >= wall_cap:
        return save('wall-budget')
    last_request = clock()  # Conservative spacing also applies after process restart.
    while not exhausted:
        if receipt['requests'] >= request_cap:
            return save('request-budget')
        if receipt['bytes'] >= byte_cap:
            return save('byte-budget')
        delay = max(0, 60 / rate - (clock() - last_request))
        if previous_wall + clock() - started + delay >= wall_cap:
            return save('wall-budget')
        sleep(delay)
        params = {'bbox': ','.join(str(x) for x in selected['bbox']), 'crs': CRS[selected['crs']],
                  'limit': selected['limit'], 'offset': offset}
        if selected['bboxCrs'] != 'CRS84':
            params['bbox-crs'] = CRS[selected['bboxCrs']]
        if selected['osids']:
            if selected['idFilterOperator'] == 'in':
                identifier_filter = "osid IN (" + ','.join("'" + x + "'" for x in selected['osids']) + ')'
            else:
                identifier_filter = '(' + ' OR '.join("osid = '" + x + "'" for x in selected['osids']) + ')'
            params.update({'filter-lang': 'cql-text', 'filter': identifier_filter})
        url = BASE + selected['collection'] + '/items?' + urlencode(params)
        receipt['requests'] += 1
        # Persist intent first: a crash cannot silently replenish a request allowance.
        save('request-started')
        remaining_wall = wall_cap - (previous_wall + clock() - started)
        if remaining_wall <= 0:
            return save('wall-budget')
        try:
            response_max = min(MAX_PAGE_BYTES, byte_cap - receipt['bytes'])
            with deadline(min(20, remaining_wall)):
                status, raw, headers = transport(url, key, response_max, min(20, remaining_wall))
        except Exception:
            return save('transport-failed')
        last_request = clock()
        receipt['bytes'] += len(raw)
        receipt['lastHttpStatus'] = status
        if status != 200:
            return save('rate-limited' if status == 429 else 'http-failed')
        filename = f'page-{len(receipt["pages"]):06d}.json'
        path(filename).write_bytes(raw)
        os.chmod(path(filename), 0o600)
        content_crs = next((value for name, value in headers.items() if name.lower() == 'content-crs'), None)
        content_crs = content_crs.strip().strip('<>') if isinstance(content_crs, str) else None
        # Retain only a validated CRS value; no arbitrary provider headers enter receipts.
        valid_crs = content_crs if content_crs == CRS[selected['crs']] else None
        receipt['pages'].append({'file': filename, 'sha256': sha(raw), 'bytes': len(raw), 'offset': offset,
                                 'contentCrs': valid_crs, 'responseTruncated': len(raw) > response_max})
        if len(raw) > response_max:
            return save('response-byte-budget' if len(raw) > MAX_PAGE_BYTES else 'byte-budget')
        if valid_crs is None:
            return save('content-crs-mismatch')
        if receipt['bytes'] > byte_cap:
            return save('byte-budget')
        if previous_wall + clock() - started > wall_cap:
            return save('wall-budget')
        try:
            features, exhausted = consume(raw)
        except (ValueError, TypeError, AttributeError):
            return save('invalid-or-inconsistent-page')
        offset += len(features)
        save('page-retained')
    output = path('features.ndjson')
    with output.open('wb') as stream:
        os.chmod(output, 0o600)
        for page in receipt['pages']:
            for feature in json.loads(path(page['file']).read_bytes())['features']:
                stream.write(encoded(feature) + b'\n')
    receipt.update({'complete': True, 'featureCount': len(seen), 'ndjson': 'features.ndjson',
                    'ndjsonSha256': sha(output.read_bytes())})
    return save('exhausted')


def discard_payloads(directory, profile_path):
    """Dispose only selection-bound, completely profiled payloads under the writer lock."""
    directory, profile_path = Path(directory), Path(profile_path)
    for item in (directory, *directory.parents):
        if item.is_symlink():
            raise ValueError('Symlinks are forbidden')
    directory = directory.resolve()
    private_root = ROOT / 'artifacts/okf-plus/private-ngd-extractions'
    if directory.parent != private_root.resolve() or not re.fullmatch('[a-f0-9]{64}', directory.name):
        raise ValueError('Disposal requires a private selection directory')
    if not profile_path.is_absolute():
        profile_path = ROOT / profile_path
    for item in (profile_path, *profile_path.parents, directory, *directory.parents):
        if item.is_symlink():
            raise ValueError('Symlinks are forbidden')
    profile_path = profile_path.resolve()
    if not profile_path.is_relative_to(ROOT / 'artifacts'):
        raise ValueError('Profile must remain in private artifacts')
    def checked(name):
        target = directory / name
        if target.is_symlink():
            raise ValueError('Symlinks are forbidden')
        return target
    with checked('writer.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Selection already has an active writer') from None
        receipt = json.loads(checked('receipt.json').read_bytes())
        profile_raw = profile_path.read_bytes()
        profile = json.loads(profile_raw)
        if (receipt.get('complete') is not True or profile.get('scanComplete') is not True
                or profile.get('profile') != 'okf-plus-transient-feature-profile.v1'
                or profile.get('recordCount') != receipt.get('featureCount')
                or profile.get('inputSha256') != receipt.get('ndjsonSha256')
                or profile.get('retrievalRecipe', {}).get('selectionDigest') != directory.name
                or sha(encoded(receipt.get('selection'))) != directory.name
                or not isinstance(profile.get('fields'), list)
                or any(row.get('cardinalityComplete') is not True for row in profile['fields'])):
            raise ValueError('Complete selection-bound profile is required before disposal')
        targets = [checked('features.ndjson')]
        for page in receipt['pages']:
            if not re.fullmatch(r'page-[0-9]{6}\.json', page['file']):
                raise ValueError('Invalid page filename')
            target = checked(page['file'])
            if not receipt.get('payloadDiscarded') and sha(target.read_bytes()) != page['sha256']:
                raise ValueError('Cached page checksum mismatch')
            targets.append(target)
        if not receipt.get('payloadDiscarded') and sha(targets[0].read_bytes()) != receipt['ndjsonSha256']:
            raise ValueError('NDJSON checksum mismatch')
        receipt.update(payloadDiscarded=True, profilePath=str(profile_path.relative_to(ROOT)),
                       profileSha256=sha(profile_raw))
        # Persist the verified profile as well as the disposal receipt before deleting.
        private_atomic_write(profile_path, profile_raw)
        private_atomic_write(checked('receipt.json'), encoded(receipt))
        for target in targets:
            target.unlink(missing_ok=True)
        return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--collection', required=True)
    parser.add_argument('--bbox', type=float, nargs=4, required=True)
    parser.add_argument('--bbox-crs', default='CRS84', choices=('CRS84', '27700'))
    parser.add_argument('--crs', default='27700', choices=tuple(CRS))
    parser.add_argument('--osid', action='append', default=[])
    parser.add_argument('--id-filter-operator', choices=('or', 'in'), default='or')
    parser.add_argument('--queryables', type=Path)
    parser.add_argument('--max-requests', type=int, default=10)
    parser.add_argument('--max-bytes', type=int, default=32*1024*1024)
    parser.add_argument('--max-wall-seconds', type=int, default=120)
    parser.add_argument('--requests-per-minute', type=int, default=30)
    parser.add_argument('--refresh', action='store_true', help='Reacquire a verified, discarded selection; retain old receipt history')
    args = parser.parse_args()
    evidence = json.loads(args.queryables.read_text()) if args.queryables else None
    result = extract(args.collection, args.bbox, key=os.environ.get('OS_API_KEY', ''),
                     bbox_crs=args.bbox_crs, crs=args.crs, osids=args.osid, queryables=evidence,
                     max_requests=args.max_requests, max_bytes=args.max_bytes,
                     max_wall_seconds=args.max_wall_seconds, requests_per_minute=args.requests_per_minute,
                     refresh=args.refresh, id_filter_operator=args.id_filter_operator)
    print(json.dumps({k: result[k] for k in ('complete', 'reason', 'requests', 'bytes')}))


if __name__ == '__main__':
    main()
