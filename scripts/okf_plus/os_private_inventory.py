#!/usr/bin/env python3
"""Resumable owner-private OS package inventory; never downloads feature files.

Only fixed catalogue and package-version metadata routes are admitted. Provider
URLs are evidence, never instructions. Account metadata stays in ignored artefacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, build_opener

from .harvest import ROOT, Redirect, deadline

BASE = 'https://api.os.uk'
PACKAGE = '/downloads/v1/dataPackages'
VERSION = re.compile(r'/downloads/v1/dataPackages/[A-Za-z0-9_-]{1,128}/versions/[A-Za-z0-9_.-]{1,128}')
RATE_URL = 'https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy.md'
MAX_BODY = 8 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024


def admitted(route):
    if route not in (PACKAGE, '/features/ngd/ofa/v1/collections', '/downloads/v1/products') and not VERSION.fullmatch(route):
        raise ValueError('Route outside private metadata inventory')
    return BASE + route


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', value):
        raise ValueError('Invalid source package identifier')
    return value


def save(path, value):
    temporary = path.with_suffix('.tmp')
    if path.is_symlink() or temporary.is_symlink():
        raise ValueError('Symlink output refused')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


class Inventory:
    def __init__(self, output, max_requests=500, wall_seconds=1800):
        # The CLI deliberately has no arbitrary destination or provider URL input.
        self.output = Path(output)
        for part in (self.output, *self.output.parents):
            if part.is_symlink():
                raise ValueError('Symlink output refused')
        self.output.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.output, 0o700)
        self.path = self.output / 'ledger.json'
        if self.path.is_symlink():
            raise ValueError('Symlink ledger refused')
        self.ledger = json.loads(self.path.read_text()) if self.path.exists() else {
            'schema': 'gis-ai-go.os-private-inventory.v1',
            'distribution': 'owner-private', 'execution': 'metadata-only',
            'ratePolicy': {'source': RATE_URL, 'requestsPerMinuteCeiling': 30,
                           'projectMode': 'unconfirmed', 'stopOn429': True},
            'requests': [],
        }
        if type(max_requests) is not int or not 1 <= max_requests <= 1000:
            raise ValueError('Request ceiling must be 1..1000')
        if type(wall_seconds) is not int or not 1 <= wall_seconds <= 3600:
            raise ValueError('Wall budget must be 1..3600 seconds')
        self.max_requests = max_requests
        self.ends = time.monotonic() + wall_seconds
        # A resumed process also waits one interval before its first wire call.
        self.next_request = time.monotonic() + 2.05
        self.opener = build_opener(Redirect())

    def get(self, route):
        url = admitted(route)
        for row in self.ledger['requests']:
            if row['route'] == route and row.get('status') == 200:
                if not re.fullmatch(r'[0-9a-f]{64}', row.get('sha256', '')):
                    raise ValueError('Invalid retained digest')
                source = self.output / (row['sha256'] + '.json')
                if source.is_symlink():
                    raise ValueError('Symlink retained response refused')
                raw = source.read_bytes()
                if hashlib.sha256(raw).hexdigest() != row['sha256']:
                    raise ValueError('Retained inventory checksum mismatch')
                return json.loads(raw)
        if any(r.get('status') == 429 for r in self.ledger['requests']):
            raise RuntimeError('Prior rate-limit stop requires a separately reviewed new capture')
        if len(self.ledger['requests']) >= self.max_requests:
            raise RuntimeError('Cumulative request ceiling reached')
        total = sum(r.get('bytes', 0) for r in self.ledger['requests'])
        if total >= MAX_TOTAL:
            raise RuntimeError('Cumulative byte ceiling reached')
        wait = max(0, self.next_request - time.monotonic())
        if time.monotonic() + wait + 25 > self.ends:
            raise RuntimeError('Wall budget reached; rerun resumes verified successes')
        time.sleep(wait)
        row = {'route': route, 'at': datetime.now(timezone.utc).isoformat(), 'status': 'pending'}
        self.ledger['requests'].append(row)
        save(self.path, self.ledger)
        headers = {'User-Agent': 'GIS-AI-GO-OKF-Plus/0.1 metadata-inventory', 'Accept': 'application/json'}
        start = time.monotonic()
        try:
            if route.startswith(PACKAGE):
                headers['key'] = os.environ['OS_API_KEY']
            with deadline(25), self.opener.open(Request(url, headers=headers), timeout=20) as response:
                raw = response.read(min(MAX_BODY, MAX_TOTAL - total) + 1)
                row['bytes'] = len(raw)
                if len(raw) > min(MAX_BODY, MAX_TOTAL - total):
                    raise ValueError('Response byte ceiling reached')
                parsed = json.loads(raw)
                digest = hashlib.sha256(raw).hexdigest()
                target = self.output / (digest + '.json')
                if target.is_symlink():
                    raise ValueError('Symlink output refused')
                fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                os.fchmod(fd, 0o600)
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(raw)
                row.update(status=response.status, sha256=digest)
                return parsed
        except Exception as error:
            row['status'] = error.code if isinstance(error, HTTPError) else 'failed'
            row['errorType'] = type(error).__name__
            if isinstance(error, HTTPError):
                row['retryAfter'] = error.headers.get('Retry-After')
            # URLs, response bodies and exception messages can contain account data.
            raise RuntimeError('Inventory request failed; inspect private receipt status') from None
        finally:
            row['elapsedSeconds'] = round(time.monotonic() - start, 6)
            self.next_request = start + 2.05
            save(self.path, self.ledger)

    def run(self):
        packages = self.get(PACKAGE)
        if not isinstance(packages, list):
            raise ValueError('Unknown package catalogue shape')
        collections = self.get('/features/ngd/ofa/v1/collections')
        products = self.get('/downloads/v1/products')
        versions = []
        for package in packages:
            pid = identifier(package['id'])
            for version in package.get('versions', []):
                vid = identifier(version['id'])
                # Construct routes from validated native IDs; never follow URLs.
                detail = self.get(PACKAGE + '/' + pid + '/versions/' + vid)
                versions.append({'packageId': pid, 'versionId': vid, 'detail': detail})
        result = {'schema': 'gis-ai-go.os-private-package-coverage.v1',
                  'distribution': 'owner-private', 'packageCount': len(packages),
                  'versionCount': len(versions),
                  'ngdCollectionCount': len(collections.get('collections', [])),
                  'openProductCount': len(products),
                  'globalEntitlementCompleteness': 'not-established',
                  'featureDataDownloaded': False,
                  'limits': ['Configured packages are not the complete PSGA entitlement.',
                             'Version metadata is not a completed data download.',
                             'Catalogue observations are not an atomic snapshot.'],
                  'versions': versions}
        save(self.output / 'coverage.json', result)
        return {k: v for k, v in result.items() if k != 'versions'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-requests', type=int, default=500)
    parser.add_argument('--wall-seconds', type=int, default=1800)
    args = parser.parse_args()
    output = ROOT / 'artifacts/okf-plus/private-os-inventory'
    # One writer. A crash leaves a visible lock for review, never a hidden writer.
    for part in (output, *output.parents):
        if part.is_symlink():
            raise ValueError('Symlink output refused')
    output.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = output / '.lock'
    fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.close(fd)
        print(json.dumps(Inventory(output, args.max_requests, args.wall_seconds).run()))
    finally:
        lock.unlink()


if __name__ == '__main__':
    main()
