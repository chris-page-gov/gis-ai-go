"""Offline private route agreement observations and candidate OS support drafts.

Inputs: routes (2..8), each with route_id, call {method,url,params,key_binding},
context {collection,version,crs,time,units}, source_independence (bool),
receipt_sha256, records, identity_path (list), fields (requested ID -> exact
native path). Different paths require reviewed_mappings [{field,evidence}].
Optional tolerance {field:{absolute,reason,units,crs}} and normalization
{reviewed:true,evidence,contexts_aligned:true} refer to supplied already-normalised
records; this module never transforms source values. HTTP status comparisons use
http_status, selector_id and expected_behavior_refs on route inputs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

ROOT = Path(__file__).resolve().parents[2]
SECRET_NAMES = {'key', 'apikey', 'token', 'accesstoken', 'authorization', 'password',
                'secret', 'clientsecret', 'signature', 'credential'}


def _name(value):
    return ''.join(c for c in value.lower() if c.isalnum())


def _safe(value, parent='', depth=0):
    if depth > 32: raise ValueError('Comparison metadata depth ceiling')
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or _name(key) in SECRET_NAMES:
                raise ValueError('Credential fields are forbidden; provide binding names only')
            _safe(item, key, depth + 1)
    elif isinstance(value, list):
        for item in value: _safe(item, parent, depth + 1)
    elif isinstance(value, str):
        if len(value) > 8192 or value.lower().startswith(('bearer ', 'basic ')):
            raise ValueError('Unsafe or excessive metadata text')
        if '://' in value:
            parsed = urlsplit(value)
            if parsed.username or parsed.password or any(_name(k) in SECRET_NAMES for k, _ in parse_qsl(parsed.query)):
                raise ValueError('Credential URL metadata is forbidden')
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Non-finite value')


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise ValueError('Expected bounded non-empty text')
    return value


def _path(value):
    if not isinstance(value, list) or not 1 <= len(value) <= 16 or any(not isinstance(v, str) or not v for v in value):
        raise ValueError('Expected explicit bounded native path')
    return value


def _at(record, path):
    for part in path:
        if not isinstance(record, dict) or part not in record:
            return False, None
        record = record[part]
    return True, record


def _typed_equal(left, right):
    return type(left) is type(right) and json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)


def compare_routes(spec):
    if not isinstance(spec, dict): raise ValueError('Expected comparison object')
    _safe(spec)
    if len(json.dumps(spec)) > 2 * 1024 * 1024: raise ValueError('Comparison input byte ceiling')
    routes = spec.get('routes')
    if not isinstance(routes, list) or not 2 <= len(routes) <= 8:
        raise ValueError('Route count must be 2..8')
    private_values = spec.get('include_private_values', False)
    if type(private_values) is not bool: raise ValueError('Private-values flag must be boolean')
    method = _text(spec.get('methodology'))
    code = _text(spec.get('code_reference'))
    requested = spec.get('requested_fields', [])
    if not isinstance(requested, list) or len(requested) > 128 or len(set(requested)) != len(requested):
        raise ValueError('Requested fields must be a unique bounded list')
    for field in requested: _text(field)
    ids = set()
    for route in routes:
        rid = _text(route.get('route_id'))
        if rid in ids: raise ValueError('Duplicate route identity')
        ids.add(rid)
        call = route.get('call')
        if not isinstance(call, dict) or set(call) != {'method', 'url', 'params', 'key_binding'}:
            raise ValueError('Exact sanitised call and key binding name required')
        for key in ('method', 'url', 'key_binding'): _text(call[key])
        if not re.fullmatch(r'[A-Z][A-Z0-9_]{0,127}', call['key_binding']):
            raise ValueError('Use an environment binding name, never a credential value')
        if not isinstance(call['params'], dict): raise ValueError('Call params must be an object')
        digest = route.get('receipt_sha256')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in 'abcdef0123456789' for c in digest):
            raise ValueError('Raw-response receipt SHA256 required')
        context = route.get('context')
        if not isinstance(context, dict) or set(context) != {'collection', 'version', 'crs', 'time', 'units'}:
            raise ValueError('Explicit collection/version/CRS/time/units context required')
        if any(value is None or value == '' for value in context.values()):
            raise ValueError('Unknown contexts must not be represented as comparable')
        if type(route.get('source_independence')) is not bool:
            raise ValueError('Source independence flag required')
        records = route.get('records', [])
        if not isinstance(records, list) or len(records) > 10000: raise ValueError('Record ceiling exceeded')
        if records: _path(route.get('identity_path'))
        fields = route.get('fields', {})
        if not isinstance(fields, dict) or len(fields) > 128: raise ValueError('Field mapping ceiling exceeded')
        for path in fields.values(): _path(path)
        if 'http_status' in route and (type(route['http_status']) is not int or not 100 <= route['http_status'] <= 599):
            raise ValueError('Invalid HTTP status')
    normalization = spec.get('normalization', {})
    if not isinstance(normalization, dict): raise ValueError('Normalization must be reviewed metadata')
    if normalization: _text(normalization.get('evidence'))
    aligned = (normalization.get('reviewed') is True and normalization.get('contexts_aligned') is True
               and bool(normalization.get('evidence')))
    mappings = spec.get('reviewed_mappings', [])
    if not isinstance(mappings, list) or len(mappings) > 128: raise ValueError('Mapping ceiling exceeded')
    reviewed = set()
    for mapping in mappings:
        if set(mapping) != {'field', 'evidence'}: raise ValueError('Mapping needs field and evidence')
        if mapping['field'] in reviewed: raise ValueError('Ambiguous repeated reviewed mapping')
        reviewed.add(_text(mapping['field'])); _text(mapping['evidence'])
    tolerances = spec.get('tolerances', {})
    if not isinstance(tolerances, dict) or len(tolerances) > 128: raise ValueError('Tolerance ceiling exceeded')
    for tolerance in tolerances.values():
        amount = tolerance.get('absolute')
        if isinstance(amount, bool) or not isinstance(amount, (float, int)) or amount < 0 or amount > 1e18:
            raise ValueError('Tolerance must be explicit bounded nonnegative number')
        for key in ('reason', 'units', 'crs'): _text(tolerance.get(key))
    observations, discrepancies = [], []
    left = routes[0]
    for right in routes[1:]:
        pair = {'routes': [left['route_id'], right['route_id']], 'comparable': True,
                'not_comparable': [], 'fields': [], 'http_status_discrepancy': False}
        contexts_equal = left['context'] == right['context']
        if not contexts_equal and not aligned:
            pair['comparable'] = False; pair['not_comparable'].append('Context mismatch without reviewed normalization')
        if 'http_status' in left and 'http_status' in right:
            same_selector = left.get('selector_id') and left.get('selector_id') == right.get('selector_id')
            if same_selector and pair['comparable']:
                pair['http_status_discrepancy'] = left['http_status'] != right['http_status']
                if pair['http_status_discrepancy']:
                    discrepancies.append({'kind': 'http-status', 'routes': pair['routes']})
                elif left['http_status'] >= 400 or right['http_status'] >= 400:
                    discrepancies.append({'kind': 'http-error', 'routes': pair['routes']})
            else:
                pair['not_comparable'].append('HTTP comparison needs matching explicit selector identity and context')
        def indexed(route):
            result = {}
            for record in route.get('records', []):
                present, identity = _at(record, route['identity_path'])
                if not present or isinstance(identity, (dict, list)) or identity is None:
                    raise ValueError('Native record identity missing or non-scalar')
                key = (type(identity).__name__, json.dumps(identity, sort_keys=True))
                if key in result: raise ValueError('Duplicate native record identity')
                result[key] = record
            return result
        lrows, rrows = indexed(left), indexed(right)
        for field in requested:
            lp, rp = left.get('fields', {}).get(field), right.get('fields', {}).get(field)
            row = {'field': field, 'comparable': pair['comparable'] and lp is not None and rp is not None and (lp == rp or field in reviewed),
                   'matched_records': len(lrows.keys() & rrows.keys()), 'missing_left_records': len(rrows.keys() - lrows.keys()),
                   'missing_right_records': len(lrows.keys() - rrows.keys()), 'missing_left_values': 0, 'missing_right_values': 0,
                   'null_observations': 0, 'type_differences': 0, 'N': 0, 'equal': 0, 'unequal': 0, 'concordance_fraction': None}
            if not row['comparable']:
                row['reason'] = 'Unknown field equivalence or mismatched context'; pair['not_comparable'].append(field)
                pair['fields'].append(row); continue
            tolerance = tolerances.get(field)
            if tolerance and any(tolerance[key] != route['context'][key] for route in (left, right) for key in ('units', 'crs')):
                raise ValueError('Tolerance requires identical explicit units and CRS on both routes')
            for identity in sorted(lrows.keys() & rrows.keys()):
                la, lv = _at(lrows[identity], lp); ra, rv = _at(rrows[identity], rp)
                row['missing_left_values'] += not la; row['missing_right_values'] += not ra
                if not la or not ra: continue
                row['N'] += 1
                row['null_observations'] += lv is None or rv is None
                row['type_differences'] += type(lv) is not type(rv)
                equal = _typed_equal(lv, rv)
                if tolerance and type(lv) is type(rv) and isinstance(lv, (int, float)) and not isinstance(lv, bool):
                    equal = abs(lv - rv) <= tolerance['absolute']
                row['equal' if equal else 'unequal'] += 1
                if not equal and private_values:
                    row.setdefault('private_differences', []).append({'identity': identity[1], 'left': lv, 'right': rv})
            row['concordance_fraction'] = row['equal'] / row['N'] if row['N'] else None
            if row['unequal'] or any(row[key] for key in ('missing_left_records','missing_right_records','missing_left_values','missing_right_values')):
                discrepancies.append({'kind': 'field-observation', 'routes': pair['routes'], 'field': field})
            pair['fields'].append(row)
        observations.append(pair)
    case = None
    if discrepancies:
        case = {'profile': 'okf-plus-private-os-support-case.v1', 'distribution': 'private',
            'candidateOnly': True, 'execution': False, 'sendingAdmitted': False,
            'methodology': method, 'code_reference': code, 'discrepancies': discrepancies,
            'calls': [{key: route.get(key) for key in ('route_id','call','context','receipt_sha256','http_status','selector_id','expected_behavior_refs')} for route in routes],
            'mapping_evidence': mappings, 'normalization_evidence': normalization, 'tolerances': tolerances,
            'observations': observations}
    return {'profile': 'okf-plus-private-route-comparison.v1', 'distribution': 'private',
        'execution': False, 'candidateOnly': True, 'observations': observations, 'support_case': case,
        'limitations': ['N and concordance are descriptive agreement only, not statistical confidence or truth.',
            'Same-backend agreement is not independent evidence. Source-independence flags are supplied claims, not verified.',
            'Reviewed normalization refers to supplied aligned inputs; no transformation was executed.'],
        'source_independence_claims': {r['route_id']: r['source_independence'] for r in routes}}


def draft_markdown(result):
    case = result['support_case']
    if case is None: return None
    return '# Private candidate OS support case\n\nUnsent draft. Descriptive observations do not establish provider error or independent truth.\n\n```json\n' + json.dumps(case, indent=2, ensure_ascii=False) + '\n```\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path); parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        from .passages import no_symlinks
        output = no_symlinks(args.output)
        if not output.is_relative_to(ROOT / 'artifacts') or output.exists():
            raise ValueError('Output must be a new directory under ignored artifacts/')
        with args.input.open('rb') as stream: raw = stream.read(2 * 1024 * 1024 + 1)
        if len(raw) > 2 * 1024 * 1024: raise ValueError('Input byte ceiling exceeded')
        result = compare_routes(json.loads(raw))
        output.mkdir(parents=True, mode=0o700)
        (output / 'comparison.json').write_text(json.dumps(result, indent=2, allow_nan=False))
        (output / 'comparison.json').chmod(0o600)
        draft = draft_markdown(result)
        if draft is not None:
            (output / 'support-case-draft.md').write_text(draft)
            (output / 'support-case-draft.md').chmod(0o600)
    except (ValueError, OSError) as error:
        parser.exit(2, f'Invalid private comparison: {error}\n')


if __name__ == '__main__': main()
