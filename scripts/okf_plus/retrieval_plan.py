"""Offline, evidence-input retrieval estimates; never invokes a provider.

JSON input uses optional ``api`` and ``bulk`` objects. Durations and measured
throughput are explicit {"min": number, "max": number} ranges. A route's
``coverage`` must be the same non-empty identifier before comparing routes.
``rate_ceiling`` is request starts per second: 30 requests/minute is 0.5,
not 30. All durations are seconds and all transfer quantities are bytes.
"""
import argparse
import json
import math
from pathlib import Path

MAX_INPUT_BYTES = 65536
MAX_NUMBER = 10 ** 18
API_FIELDS = {'count', 'page_size', 'rate_ceiling', 'latency_seconds',
              'bytes_per_page', 'processing_seconds', 'coverage'}
BULK_FIELDS = {'known_bytes', 'throughput_bytes_per_second', 'unpack_seconds',
               'processing_seconds', 'coverage'}


def _number(value, name, *, integer=False, positive=False):
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or abs(value) > MAX_NUMBER
            or value < 0 or (positive and value < 1e-18)
            or (integer and not isinstance(value, int))):
        raise ValueError(f'{name}: expected bounded finite {"integer" if integer else "number"}')
    return value


def _range(value, name, *, positive=False):
    if not isinstance(value, dict) or set(value) != {'min', 'max'}:
        raise ValueError(f'{name}: expected min/max range')
    low = _number(value['min'], name, positive=positive)
    high = _number(value['max'], name, positive=positive)
    if low > high:
        raise ValueError(f'{name}: min exceeds max')
    return {'min': low, 'max': high}


def _sum(*ranges):
    if any(value is None for value in ranges):
        return None
    return {key: sum(value[key] for value in ranges) for key in ('min', 'max')}


def plan_retrieval(spec):
    """Return deterministic estimates from supplied measurements only."""
    if not isinstance(spec, dict) or set(spec) - {'api', 'bulk'}:
        raise ValueError('expected object with api and/or bulk')
    result = {'metadata_only': True, 'execution': False, 'routes': {},
              'comparison': {'preferred': None, 'reason': 'Comparable complete estimates unavailable.'}}
    for route, fields in (('api', API_FIELDS), ('bulk', BULK_FIELDS)):
        if route not in spec:
            continue
        data = spec[route]
        if not isinstance(data, dict) or set(data) - fields:
            raise ValueError(f'{route}: unknown fields or invalid object')
        coverage = data.get('coverage')
        if coverage is not None and (not isinstance(coverage, str) or not coverage.strip()
                                     or len(coverage) > 512):
            raise ValueError('coverage: expected non-empty identifier, at most 512 characters')
        validated = {}
        for key, value in data.items():
            if key == 'coverage' or value is None:
                continue
            if key.endswith('_seconds') or key == 'throughput_bytes_per_second':
                validated[key] = _range(value, key, positive=key == 'throughput_bytes_per_second')
            else:
                validated[key] = _number(value, key,
                    integer=key in {'count', 'page_size', 'bytes_per_page', 'known_bytes'},
                    positive=key in {'page_size', 'rate_ceiling'})
        required = ({'count', 'page_size', 'rate_ceiling', 'latency_seconds'}
                    if route == 'api' else {'known_bytes', 'throughput_bytes_per_second'})
        unknowns = [f'Missing {key}.' for key in sorted(required - validated.keys())]
        acquisition = None
        details = {}
        if not unknowns:
            if route == 'api':
                pages = (validated['count'] + validated['page_size'] - 1) // validated['page_size']
                interval = 1 / validated['rate_ceiling']
                acquisition = {key: (0 if pages == 0 else validated['latency_seconds'][key]
                    + (pages - 1) * max(interval, validated['latency_seconds'][key]))
                    for key in ('min', 'max')}
                details['pages'] = pages
                details['estimated_transfer_bytes'] = (pages * validated['bytes_per_page']
                    if 'bytes_per_page' in validated else None)
            else:
                speed = validated['throughput_bytes_per_second']
                acquisition = {'min': validated['known_bytes'] / speed['max'],
                               'max': validated['known_bytes'] / speed['min']}
        processing_fields = (['processing_seconds'] if route == 'api'
                             else ['unpack_seconds', 'processing_seconds'])
        for key in processing_fields:
            if key not in validated:
                unknowns.append(f'Missing {key}.')
        processing = _sum(*(validated.get(key) for key in processing_fields))
        assumptions = (['Sequential requests; ceiling is a supplied documented limit, not a measured speed.',
                        'rate_ceiling is request starts per second; convert per-minute limits before planning.',
                        'Count and page size cover the stated selection; latency includes transfer.']
                       if route == 'api' else
                       ['Known byte count and measured throughput cover the stated selection.'])
        assumptions.append('No retries, queueing, setup delays or future rate/throughput changes modelled; ranges are scenarios, not confidence intervals.')
        result['routes'][route] = dict(acquisition_seconds=acquisition,
            processing_seconds=processing, total_seconds=_sum(acquisition, processing),
            coverage=coverage, unknowns=unknowns, assumptions=assumptions, **details)
    api, bulk = result['routes'].get('api'), result['routes'].get('bulk')
    if api and bulk and api['coverage'] and api['coverage'] == bulk['coverage']:
        left, right = api['total_seconds'], bulk['total_seconds']
        if left and right:
            preferred = ('api' if left['max'] < right['min'] else
                         'bulk' if right['max'] < left['min'] else None)
            result['comparison'] = {'preferred': preferred, 'reason':
                'Complete supplied estimates for matching coverage; ranges overlap.' if preferred is None
                else 'Complete supplied estimates for matching coverage; preferred route is faster across the supplied ranges.'}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON evidence inputs; no network requests')
    args = parser.parse_args(argv)
    try:
        with args.input.open('rb') as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('input exceeds 65536 bytes')
        print(json.dumps(plan_retrieval(json.loads(raw)), allow_nan=False, indent=2))
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, f'Invalid retrieval plan: {exc}\n')


if __name__ == '__main__':
    main()
