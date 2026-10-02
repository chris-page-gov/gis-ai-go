"""Count actual vocabulary positions in the closed local OKF+ context, offline.

This is a usage inventory, not a general JSON-LD processor or RDF validation.
No text mining, remote context loading, inference or vocabulary retrieval occurs.
"""
from __future__ import annotations

from collections import Counter, defaultdict

try:
    from .model import CONTEXT, CTX, PREFIXES
except ImportError:
    from model import CONTEXT, CTX, PREFIXES

ROLES = ('predicateOccurrences', 'typeReferences', 'objectReferences', 'datatypeReferences')


def expanded_iri(value, *, alias=False):
    if not isinstance(value, str) or value.startswith('@'):
        return None
    if alias and value in CTX:
        definition = CTX[value]
        value = definition.get('@id') if isinstance(definition, dict) else definition
    if not isinstance(value, str):
        return None
    prefix, separator, suffix = value.partition(':')
    if separator and prefix in PREFIXES:
        return PREFIXES[prefix] + suffix
    if value.startswith(('https://', 'http://', 'urn:')):
        return value
    return None


def vocabulary_usage(records, register, revision, input_digest):
    counts = defaultdict(Counter)
    record_uses = defaultdict(set)
    rdf_type = PREFIXES['rdf'] + 'type'

    def add(iri, role, record_id):
        if iri:
            counts[iri][role] += 1
            record_uses[iri].add(record_id)

    def walk(value, record_id, object_position=False, coercion=None):
        if coercion == '@json':
            return
        if isinstance(value, list):
            for child in value:
                walk(child, record_id, object_position, coercion)
            return
        if not isinstance(value, dict):
            if object_position and coercion == '@id':
                add(expanded_iri(value), 'objectReferences', record_id)
            elif object_position and coercion == '@vocab':
                add(expanded_iri(value, alias=True), 'objectReferences', record_id)
            return  # Ordinary strings, including URI-looking prose, are literals.
        if '@context' in value and value['@context'] not in (CONTEXT, CTX):
            raise ValueError('Vocabulary report requires the pinned local context')
        if '@value' in value:
            if value.get('@type') != '@json':
                add(expanded_iri(value.get('@type'), alias=True), 'datatypeReferences', record_id)
            return  # Neither typed values nor opaque JSON are semantic subgraphs.
        if object_position:
            add(expanded_iri(value.get('@id')), 'objectReferences', record_id)
        types = value.get('@type', [])
        for typ in types if isinstance(types, list) else [types]:
            if typ == '@json':
                return
            iri = expanded_iri(typ, alias=True)
            if iri:
                add(rdf_type, 'predicateOccurrences', record_id)
                add(iri, 'typeReferences', record_id)
        for key, child in value.items():
            if key in {'@graph', '@included', '@set', '@list'}:
                walk(child, record_id, object_position=object_position if key in {'@set', '@list'} else False)
                continue
            if key.startswith('@'):
                if key not in {'@context', '@id', '@type', '@index'}:
                    raise ValueError('Unsupported keyword in vocabulary usage graph: ' + key)
                continue
            iri = expanded_iri(key, alias=True)
            if not iri or child is None or child == []:
                continue
            # One named property occurrence per node, even for multi-value arrays.
            add(iri, 'predicateOccurrences', record_id)
            definition = CTX.get(key)
            coercion = definition.get('@type') if isinstance(definition, dict) else None
            walk(child, record_id, object_position=True, coercion=coercion)

    for index, row in enumerate(records):
        walk(row, row.get('@id', f'record:{index}'))

    standards = {}
    for item in register.get('standards', []):
        prefix = item['prefix']
        if prefix in standards or prefix not in PREFIXES:
            raise ValueError('Duplicate or undeclared standards-register prefix')
        standards[prefix] = item

    def term(iri, registered=False):
        uses = counts.get(iri, {})
        return {'iri': iri, 'registeredTerm': registered,
                **{role: uses.get(role, 0) for role in ROLES},
                'recordCount': len(record_uses.get(iri, ())), 'used': bool(uses)}

    namespaces = []
    matched = set()
    for prefix, namespace in sorted(PREFIXES.items()):
        registered = standards.get(prefix)
        expected = {namespace + suffix for suffix in registered.get('terms', [])} if registered else set()
        observed = {iri for iri in counts if iri.startswith(namespace)}
        matched.update(observed)
        terms = [term(iri, iri in expected) for iri in sorted(expected | observed)]
        namespaces.append({'prefix': prefix, 'namespace': namespace,
                           'registeredStandard': registered is not None,
                           'source': registered.get('source') if registered else None,
                           'mappingReview': registered.get('mappingReview') if registered else 'local-or-unregistered-namespace',
                           'used': bool(observed), 'terms': terms,
                           'totals': {role: sum(t[role] for t in terms) for role in ROLES},
                           'unusedRegisteredTerms': sorted(expected - observed),
                           'additionalUsedTerms': sorted(observed - expected)})
    outside = sorted(set(counts) - matched)
    return {
        'schema': 'gis-ai-go.okf-plus-vocabulary-usage.v1',
        'revision': revision, 'inputDigest': input_digest, 'recordCount': len(records),
        'context': CONTEXT, 'status': 'usage-evidence-not-semantic-certification',
        'countingRules': [
            'Only the semantic record graph is counted; the bundle wrapper is excluded.',
            'Predicate occurrences count a present, non-null property once per node, independently of value-array length.',
            'Each @type class reference also counts its implicit rdf:type predicate; typed literals count datatype references separately.',
            'Object references are object-position @id nodes or context-coerced IRIs; defining subject IDs are excluded.',
            'Context declarations, ordinary literal text and opaque @json contents do not establish vocabulary use.',
            'Counts do not prove vocabulary conformance, semantic mapping correctness, entailment or domain sufficiency.',
        ],
        'totals': {role: sum(c[role] for c in counts.values()) for role in ROLES},
        'namespaces': namespaces,
        'unusedRegisteredPrefixes': sorted(p for p in standards if not next(n for n in namespaces if n['prefix'] == p)['used']),
        'unusedDeclaredPrefixes': sorted(n['prefix'] for n in namespaces if not n['used']),
        'usedUnregisteredPrefixes': sorted(n['prefix'] for n in namespaces if n['used'] and not n['registeredStandard']),
        'outsideDeclaredNamespaces': {
            'distinctIris': len(outside),
            **{role: sum(counts[iri][role] for iri in outside) for role in ROLES},
            'sampleIris': outside[:12], 'sampleComplete': len(outside) <= 12,
            'note': 'These include ordinary resource identifiers; an object URL is not necessarily an ontology term.',
        },
    }
