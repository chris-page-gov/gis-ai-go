"""Offline relationship-first candidates in Linked Identifiers endpoint namespaces.

Native-reference candidates require those same endpoint types. NGD OSID/Building
and ONS GSS comparisons need separate reviewed bridges and are not implemented.
No network, joins or spatial execution occurs here.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .linked_identifiers import (FEATURES, IDENTIFIERS, METHODS, closed, encoded,
                                 enum, method_definition, validate_method_pair, node, node_type, read_regular, sha, strict_json, text)
from .query_planner import _credential_free


def plan_relationships(spec):
    closed(spec, ('schema', 'source', 'targetType', 'purpose', 'candidates', 'spatialFallback'), ('targetSemantics',))
    if spec['schema'] != 'gis-ai-go.relationship-plan-input.v1': raise ValueError('Unknown relationship plan schema')
    if len(encoded(spec)) > 256 * 1024: raise ValueError('Relationship plan byte bound')
    _credential_free(spec)
    node(spec['source']); text(spec['purpose'], 1024)
    target = spec['targetType']; closed(target, ('featureType', 'identifierType'))
    node_type(target)
    semantics = enum(spec.get('targetSemantics', 'source-declared'), {'source-declared', 'building-outline', 'road-surface'})
    fallback = spec['spatialFallback']
    closed(fallback, ('requested', 'reason', 'evidence'))
    if type(fallback['requested']) is not bool: raise ValueError('Explicit spatial fallback choice required')
    text(fallback['reason'], 1024)
    if not isinstance(fallback['evidence'], list) or len(fallback['evidence']) > 8: raise ValueError('Invalid fallback evidence')
    for evidence in fallback['evidence']: text(evidence)
    candidates = spec['candidates']
    if not isinstance(candidates, list) or len(candidates) > 32: raise ValueError('Candidate count bound')
    accepted, unresolved, constraints, ids = [], [], [], set()
    for candidate in candidates:
        closed(candidate, ('id', 'kind', 'source', 'targetType', 'relationship', 'sourceEvidence',
                           'scopeStatus', 'versionStatus', 'observationStatus'), ('method', 'estimatedRequests', 'targetSemantics'))
        cid = text(candidate['id'], 128)
        if cid in ids: raise ValueError('Duplicate relationship candidate')
        ids.add(cid)
        enum(candidate['kind'], {'linked-identifiers', 'native-reference'})
        node(candidate['source'])
        closed(candidate['targetType'], ('featureType', 'identifierType'))
        node_type(candidate['targetType'])
        text(candidate['relationship'], 1024)
        evidence = candidate['sourceEvidence']
        if not isinstance(evidence, list) or not 1 <= len(evidence) <= 8: raise ValueError('Source evidence required')
        for item in evidence:
            closed(item, ('reference', 'sha256'))
            text(item['reference'], 1024)
            if not isinstance(item['sha256'], str) or len(item['sha256']) != 64 or any(c not in '0123456789abcdef' for c in item['sha256']):
                raise ValueError('Exact source digest required')
        enum(candidate['scopeStatus'], {'supported', 'unresolved', 'incompatible'})
        enum(candidate['versionStatus'], {'supported', 'unresolved', 'incompatible'})
        enum(candidate['observationStatus'], {'not-observed', 'observed', 'empty-response', 'denied', 'incomplete'})
        if candidate['kind'] == 'linked-identifiers':
            enum(candidate.get('method'), METHODS)
            validate_method_pair(candidate['method'], candidate['source'], candidate['targetType'])
            definition = method_definition(candidate['method'])
            constraints.append({'candidateId': cid, 'method': candidate['method'],
                'meaning': definition['meaning'], 'limits': definition['limits'],
                'sourceEvidence': {'reference': definition['source']['url'], 'sha256': definition['source']['sha256']}})
        elif 'method' in candidate: raise ValueError('Native reference cannot claim an API method')
        if 'estimatedRequests' in candidate and (type(candidate['estimatedRequests']) is not int or not 0 <= candidate['estimatedRequests'] <= 20):
            raise ValueError('Invalid bounded request estimate')
        reasons = []
        declared = candidate.get('targetSemantics', 'source-declared')
        enum(declared, {'source-declared', 'building-outline', 'road-surface'})
        if candidate['kind'] == 'linked-identifiers' and candidate['targetType']['featureType'] == 'TopographicArea':
            # Method 5 is a TopographicArea cross-reference, not a building-only classification.
            native_semantics = 'source-declared' if candidate['method'] == 'BLPU_UPRN_TopographicArea_TOID_5' else 'road-surface'
            if 'targetSemantics' in candidate and declared != native_semantics: reasons.append('method-semantic-contradiction')
            declared = native_semantics
        if semantics != 'source-declared' and declared != semantics: reasons.append('target-semantics-unproven')
        if candidate['source'] != spec['source']: reasons.append('source-identity-mismatch')
        if candidate['targetType'] != target: reasons.append('target-type-mismatch')
        if candidate['scopeStatus'] != 'supported': reasons.append('relationship-scope-' + candidate['scopeStatus'])
        if candidate['versionStatus'] != 'supported': reasons.append('source-version-' + candidate['versionStatus'])
        if candidate['observationStatus'] in {'denied', 'incomplete'}: reasons.append('observation-' + candidate['observationStatus'])
        if reasons: unresolved.append({'id': cid, 'reasons': reasons})
        else: accepted.append(candidate)
    # No implicit priority for native references over the requested API investigation.
    # Costs are descriptive estimates, not evidence that different links are equal.
    accepted.sort(key=lambda item: item['id'])
    return {'schema': 'gis-ai-go.relationship-plan.v1', 'inputSha256': sha(encoded(spec)),
        'strategy': 'source-backed-relationships-before-spatial', 'candidates': accepted,
        'unresolved': unresolved, 'sourceConstraints': constraints, 'automaticExecution': False, 'joinsEstablished': False,
        'transitiveIdentity': False, 'fieldEquivalence': False, 'geographicEquivalence': False,
        'spatialFallback': {'requested': fallback['requested'], 'status':
            'separate-review-required' if fallback['requested'] else 'not-requested',
            'reason': fallback['reason'], 'evidence': fallback['evidence']},
        'limits': ['Candidates compare source scope and version evidence; neither source kind wins automatically.',
                   'A method can originate from spatial matching without permitting a new local spatial match.',
                   'Empty, denied and incomplete observations do not establish absence of a relationship.',
                   'Chaining edges preserves each method; it does not establish identity, containment or access.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(plan_relationships(strict_json(read_regular(args.input, 256 * 1024))), indent=2))
        return 0
    except Exception:
        print(json.dumps({'complete': False, 'reason': 'relationship-plan-contract-refused'}))
        return 2


if __name__ == '__main__': raise SystemExit(main())
