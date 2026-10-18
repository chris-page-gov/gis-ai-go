"""Shared, durable per-service OS pacing for metadata and on-demand retrieval.

The aggregate limiter deliberately shares pacing across keys used in one
workspace. It neither claims provider quota accounting nor stores credentials.
"""
from contextlib import contextmanager
from email.utils import parsedate_to_datetime
import fcntl
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time

DEFAULT_INTERVAL = 1.5
SERVICES = frozenset({'documentation', 'ngd-features', 'downloads', 'gemini-catalogue', 'product-search'})


def retry_at(value, now):
    if value and re.fullmatch(r'[0-9]+', value.strip()):
        digits = value.strip().lstrip('0') or '0'
        if len(digits) > 300:
            raise ValueError('Retry-After numeric duration requires manual review')
        # Exact integer arithmetic avoids float rounding shortening a long wait.
        return math.ceil(now) + int(digits)
    if value:
        try:
            parsed = parsedate_to_datetime(value)
            if parsed.tzinfo is not None:
                return max(now, parsed.timestamp())
        except (ValueError, TypeError, OverflowError):
            pass
    return now + 60


class SharedRateLimiter:
    def __init__(self, root, clock=time.time):
        self.path = Path(root) / 'artifacts/okf-plus/os-service-rate-state.json'
        self.clock = clock

    @contextmanager
    def _state(self):
        for path in (self.path, *self.path.parents):
            if path.is_symlink():
                raise ValueError('Rate checkpoint cannot contain symbolic links')
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        lock_path = self.path.with_suffix('.lock')
        if lock_path.is_symlink():
            raise ValueError('Rate lock cannot be a symbolic link')
        with lock_path.open('a') as lock:
            os.chmod(lock_path, 0o600)
            fcntl.flock(lock, fcntl.LOCK_EX)
            try:
                state = json.loads(self.path.read_text()) if self.path.exists() else {'profile': 'okf-os-service-pacing.v1', 'services': {}}
                if state.get('profile') != 'okf-os-service-pacing.v1':
                    raise ValueError('Unsupported rate checkpoint')
                yield state
                with tempfile.NamedTemporaryFile(dir=self.path.parent, prefix='.rate-', delete=False) as stream:
                    temporary = Path(stream.name)
                    os.fchmod(stream.fileno(), 0o600)
                    stream.write((json.dumps(state, sort_keys=True, allow_nan=False) + '\n').encode())
                    stream.flush(); os.fsync(stream.fileno())
                try:
                    temporary.replace(self.path)
                finally:
                    temporary.unlink(missing_ok=True)
            finally:
                fcntl.flock(lock, fcntl.LOCK_UN)

    def reserve_attempt(self, service, interval=DEFAULT_INTERVAL):
        if service not in SERVICES or not isinstance(interval, (int, float)) or not math.isfinite(interval) or interval < DEFAULT_INTERVAL:
            raise ValueError('Unsupported service or pacing interval')
        with self._state() as state:
            now = self.clock()
            value = state['services'].setdefault(service, {'nextAllowedAt': 0})
            if value.get('blocked'):
                raise RuntimeError('Service is blocked by an unrepresentable Retry-After; inspect its private checkpoint')
            previous_interval = value.get('minimumInterval', DEFAULT_INTERVAL)
            if (not isinstance(previous_interval, (int, float)) or not math.isfinite(previous_interval)
                    or previous_interval < DEFAULT_INTERVAL):
                raise ValueError('Invalid persisted pacing interval')
            # A stricter known account/shared-project budget remains effective
            # across every caller. Relaxing it needs explicit reconfiguration,
            # never an incidental request using the default operator interval.
            effective_interval = max(previous_interval, interval)
            value['minimumInterval'] = effective_interval
            target = value['nextAllowedAt']
            if not isinstance(target, (int, float)) or not math.isfinite(target):
                raise ValueError('Invalid rate checkpoint timestamp')
            if effective_interval > previous_interval and 'lastReservedAt' in value:
                last = value['lastReservedAt']
                if not isinstance(last, (int, float)) or not math.isfinite(last):
                    raise ValueError('Invalid previous reservation timestamp')
                target = max(target, last + effective_interval)
                value['nextAllowedAt'] = target
            delay = max(0, target - now) if target < 10 ** 15 else max(0, target - math.floor(now))
            if delay == 0:
                value['nextAllowedAt'] = now + effective_interval
                value['lastReservedAt'] = now
                value['attemptReservations'] = value.get('attemptReservations', 0) + 1
            return {'allowed': delay == 0, 'notBefore': max(now, target), 'delay': delay}

    def defer_retry_after(self, service, header):
        if service not in SERVICES:
            raise ValueError('Unsupported service')
        with self._state() as state:
            value = state['services'].setdefault(service, {'nextAllowedAt': 0})
            try:
                value['nextAllowedAt'] = max(value['nextAllowedAt'], retry_at(header, self.clock()))
            except ValueError:
                value['blocked'] = 'unrepresentable-provider-retry-after'
            blocked, target = value.get('blocked'), value['nextAllowedAt']
        if blocked:
            raise RuntimeError('Provider Retry-After needs review; service durably blocked')
        return target
