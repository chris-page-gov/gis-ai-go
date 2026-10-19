"""Offline candidate recipes from explicit native-field capability evidence.

No semantic equivalence, endpoint parameters or execution authority are inferred.
Input: coverage_id, requested_fields [{stable_id,native_field,collection_id}],
routes [{route_id,coverage_id,collection_id,fields:[same field objects],kind,
request:{...}, optional projection:{supported,parameter,evidence},
estimated_requests,estimated_bytes,acquisition_seconds,processing_seconds}].
Optional route field_mappings [{requested_stable_id,route_field:{stable_id,
native_field,collection_id},equivalent:true,evidence}] supply reviewed physical
mappings. Multiple independent requests need no join capability; a single route
with fields from multiple collections requires cross_collection_capability evidence.
No result joins are inferred. Optional output_requirement {kind:table|map|analysis,
required_capabilities:[native-values|geometry|portrayal]} filters routes using
explicit output_capabilities {capability:{supported,evidence}} before costing.
Kind is descriptive; portrayal never implies native values or renderer admission.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path

from .retrieval_plan import _number, _range

MAX_ROUTES = 16
MAX_FIELDS = 256
MAX_INPUT_BYTES = 1024 * 1024
OUTPUT_CAPABILITIES = {'native-values', 'geometry', 'portrayal'}


def _identity(field):
    if not isinstance(field, dict) or set(field) != {'stable_id', 'native_field', 'collection_id'}:
        raise ValueError('Each field needs stable_id, native_field and collection_id')
    for value in field.values():
        if not isinstance(value, str) or not value.strip() or len(value) > 512:
            raise ValueError('Field identifiers must be non-empty bounded strings')
    return tuple(field[key] for key in ('stable_id', 'native_field', 'collection_id'))


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise ValueError('Expected non-empty bounded text')
    return value


def _proven(value):
    return (isinstance(value, dict) and value.get('supported') is True
            and isinstance(value.get('evidence'), str) and 0 < len(value['evidence']) <= 2048
            and bool(value['evidence'].strip()))


def plan_query(spec):
    if not isinstance(spec, dict) or set(spec) - {'coverage_id', 'requested_fields', 'routes', 'merge_capability', 'output_requirement'}:
        raise ValueError('Unknown planner input')
    coverage = _text(spec.get('coverage_id'))
    requirement = spec.get('output_requirement')
    if requirement is not None:
        if (not isinstance(requirement, dict) or set(requirement) != {'kind', 'required_capabilities'}
                or not isinstance(requirement['kind'], str)
                or requirement['kind'] not in {'table', 'map', 'analysis'}):
            raise ValueError('Output requirement needs explicit kind and required capabilities')
        required = requirement['required_capabilities']
        if (not isinstance(required, list) or not 1 <= len(required) <= 3
                or any(not isinstance(item, str) or item not in OUTPUT_CAPABILITIES for item in required)
                or len(set(required)) != len(required)):
            raise ValueError('Output capabilities must be unique native-values, geometry or portrayal')
    fields, routes = spec.get('requested_fields'), spec.get('routes')
    if not isinstance(fields, list) or not 1 <= len(fields) <= MAX_FIELDS:
        raise ValueError('Requested field count must be 1..256')
    wanted = {_identity(field): field for field in fields}
    if len(wanted) != len(fields) or len({key[0] for key in wanted}) != len(fields):
        raise ValueError('Duplicate or ambiguous stable field identity')
    if not isinstance(routes, list) or not 0 <= len(routes) <= MAX_ROUTES:
        raise ValueError('Route count must be 0..16')
    candidates, rejected, ids = [], [], set()
    allowed = {'route_id', 'coverage_id', 'collection_id', 'fields', 'kind', 'request',
               'projection', 'estimated_requests', 'estimated_bytes',
               'acquisition_seconds', 'processing_seconds', 'field_mappings',
               'cross_collection_capability', 'output_capabilities'}
    for route in routes:
        if not isinstance(route, dict) or set(route) - allowed:
            raise ValueError('Unknown route fields')
        rid = _text(route.get('route_id'))
        if rid in ids:
            raise ValueError('Duplicate route_id')
        ids.add(rid)
        output_capabilities = route.get('output_capabilities', {})
        if (not isinstance(output_capabilities, dict)
                or set(output_capabilities) - OUTPUT_CAPABILITIES):
            raise ValueError('Unknown output capability')
        if requirement is not None:
            missing_capabilities = [name for name in requirement['required_capabilities']
                if not _proven(output_capabilities.get(name))]
            if missing_capabilities:
                rejected.append({'route_id': rid, 'reason': 'output-capability-unproven',
                                 'required_capabilities': missing_capabilities})
                continue
        rcoverage, collection = _text(route.get('coverage_id')), _text(route.get('collection_id'))
        available = route.get('fields')
        if not isinstance(available, list) or len(available) > MAX_FIELDS:
            raise ValueError('Route fields must be a bounded list')
        native = {_identity(field) for field in available}
        if any(identity[2] != collection for identity in native) and not _proven(route.get('cross_collection_capability')):
            rejected.append({'route_id': rid, 'reason': 'single-route-cross-collection-capability-unproven'})
            continue
        if route.get('kind') not in ('api', 'download'):
            raise ValueError('Route kind must be api or download')
        request = route.get('request')
        if not isinstance(request, dict) or len(json.dumps(request)) > 16384:
            raise ValueError('Request descriptor must be a bounded object')
        # Supplied descriptors remain untrusted, inert metadata, including any URL.
        costs = {key: None for key in ('estimated_requests', 'estimated_bytes',
                                      'acquisition_seconds', 'processing_seconds')}
        for key in costs:
            value = route.get(key)
            if value is not None:
                try:
                    costs[key] = (_range(value, key) if key.endswith('_seconds') else
                                  _number(value, key, integer=True))
                except OverflowError:
                    raise ValueError('Cost exceeds finite numeric bounds') from None
        mapping = {identity: {'requested': wanted[identity], 'route_field': wanted[identity],
                    'method': 'exact-identity', 'evidence': None} for identity in native & wanted.keys()}
        mappings = route.get('field_mappings', [])
        if not isinstance(mappings, list) or len(mappings) > MAX_FIELDS:
            raise ValueError('Field mappings must be a bounded list')
        requested_by_id = {identity[0]: identity for identity in wanted}
        seen_mappings = set()
        for item in mappings:
            if not isinstance(item, dict) or set(item) != {'requested_stable_id', 'route_field', 'equivalent', 'evidence'}:
                raise ValueError('Reviewed mapping requires requested identity, route field, equivalence and evidence')
            requested_id = _text(item['requested_stable_id'])
            physical = _identity(item['route_field'])
            if requested_id not in requested_by_id or physical not in native:
                raise ValueError('Mapping must bind a requested identity to an available route field')
            if requested_id in seen_mappings:
                raise ValueError('Ambiguous repeated requested identity in route mappings')
            seen_mappings.add(requested_id)
            if item['equivalent'] is not True:
                raise ValueError('Only explicitly reviewed equivalence mappings are admitted')
            _text(item['evidence'])
            target = requested_by_id[requested_id]
            if target in mapping and _identity(mapping[target]['route_field']) != physical:
                raise ValueError('Mapping conflicts with exact field identity')
            mapping[target] = {'requested': wanted[target], 'route_field': item['route_field'],
                               'method': 'reviewed-equivalence', 'evidence': item['evidence']}
        matched = sorted(mapping)
        if rcoverage != coverage or not matched:
            rejected.append({'route_id': rid, 'reason': 'coverage-mismatch' if rcoverage != coverage else 'no-exact-field-identity'})
            continue
        projection = route.get('projection')
        server = route['kind'] == 'api' and _proven(projection)
        if server:
            _text(projection.get('parameter'))
        recipe = {'route_id': rid, 'collection_id': collection, 'kind': route['kind'],
                  'request': request, 'execution': False,
                  'field_mapping': [mapping[key] for key in matched],
                  'serverProjection': ({'parameter': projection['parameter'],
                    'values': [mapping[key]['route_field']['native_field'] for key in matched], 'evidence': projection['evidence']} if server else None),
                  'localProjection': [] if server else [mapping[key]['route_field']['native_field'] for key in matched],
                  'mode': 'server-projection' if server else 'download-local-projection' if route['kind'] == 'download' else 'full-record-local-projection',
                  'unproven': ['Provider request descriptor, rights and capabilities require separate verification.'] +
                    ([] if server else ['Server-side field projection is not established; no parameter generated.']), **costs}
        if requirement is not None:
            recipe['outputCapabilityEvidence'] = {name: output_capabilities[name]['evidence']
                for name in requirement['required_capabilities']}
        candidates.append((set(matched), recipe))
    feasible = []
    for size in range(1, len(candidates) + 1):
        for subset in itertools.combinations(candidates, size):
            if set().union(*(item[0] for item in subset)) != wanted.keys():
                continue
            recipes = [item[1] for item in subset]
            totals = {}
            for key in ('estimated_requests', 'estimated_bytes'):
                totals[key] = sum(r[key] for r in recipes) if all(r[key] is not None for r in recipes) else None
            total_time = None
            if all(r['acquisition_seconds'] is not None and r['processing_seconds'] is not None for r in recipes):
                total_time = {bound: sum(r[key][bound] for r in recipes for key in
                    ('acquisition_seconds', 'processing_seconds')) for bound in ('min', 'max')}
            feasible.append({'recipes': recipes, 'result_mode': 'bundled-independent-results',
                             'joins': False, 'total_seconds': total_time, **totals})
    if feasible and all(item['total_seconds'] is not None for item in feasible):
        basis = 'Supplied sequential acquisition plus processing upper bounds; no parallelism inferred.'
        key = lambda item: (item['total_seconds']['max'], len(item['recipes']))
    elif feasible and all(item['estimated_requests'] is not None for item in feasible):
        basis = 'Fewer supplied requests; timing evidence is incomplete and fastest route is unproven.'
        key = lambda item: (item['estimated_requests'], len(item['recipes']))
    else:
        basis = 'Fewer route descriptors only; request, byte or timing efficiency is unproven.'
        key = lambda item: len(item['recipes'])
    feasible.sort(key=key)
    covered = set().union(*(item[0] for item in candidates)) if candidates else set()
    result = {'profile': 'okf-plus-offline-query-plan.v1', 'execution': False,
            'candidateOnly': True, 'coverage_id': coverage, 'joins': False,
            'selected': feasible[0] if feasible else None, 'alternatives': feasible[:20],
            'omitted_alternatives': max(0, len(feasible) - 20),
            'missing_fields': [wanted[key] for key in sorted(wanted.keys() - covered)],
            'rejected_routes': rejected, 'rationale': basis,
            'unproven': ['Exact field identity is required unless an explicit reviewed equivalence mapping supplies evidence; names never imply equivalence.',
                'Independent request results are bundled without joins; a single route across collections requires explicit capability evidence and coverage identifiers must match exactly.',
                'No complete executable request or retrieval authority is established.'] +
                (['Fields exist but no complete cover is available.'] if not feasible and not (wanted.keys() - covered) else [])}

    if requirement is not None:
        result['output_requirement'] = requirement
        result['outputFitEstablished'] = bool(feasible)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args(argv)
    try:
        with args.input.open('rb') as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('Input exceeds byte limit')
        result = plan_query(json.loads(raw))
        print(json.dumps(result, allow_nan=False, indent=2))
    except (ValueError, OSError, UnicodeError) as error:
        parser.exit(2, f'Invalid query plan: {error}\n')


if __name__ == '__main__':
    main()
