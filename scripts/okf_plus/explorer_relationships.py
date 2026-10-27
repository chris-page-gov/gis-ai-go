"""Project source-declared links between retained records into Explorer rows.

This is a deterministic presentation of explicit JSON-LD references. Markdown
links, tags, similar names and learning steps never create domain assertions.
The additive GIS schema is deliberately not a Bundle Wiki conformance claim.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
from functools import lru_cache
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlsplit

from jsonschema import Draft202012Validator

try:
    from .context_projection import canonical, sha
    from .model import PREFIXES, load_json
except ImportError:
    from context_projection import canonical, sha
    from model import PREFIXES, load_json


SCHEMA = 'gis-ai-go.explorer-relationship.v1'
DERIVATION = 'explicit-jsonld-retained-record-reference-v1'
MAX_OMISSION_EXAMPLES = 4
STATUS = {'normalised': 'normalized', 'normalized': 'normalized',
          'official': 'official', 'inferred': 'inferred', 'model-derived': 'model-derived'}

# Labels describe these declared vocabulary properties; they do not infer a
# relationship from a title, a Markdown link or an arbitrary JSON field.
PREDICATES = {
    'skos:related': ('related', 'related concept', 'related concept'),
    'skos:broader': ('broader', 'has broader concept', 'has narrower concept'),
    'skos:narrower': ('narrower', 'has narrower concept', 'has broader concept'),
    'skos:relatedMatch': ('related match', 'has related match', 'has related match'),
    'dcterms:isPartOf': ('part of', 'is part of', 'has part'),
    'dcterms:hasPart': ('has part', 'has part', 'is part of'),
}
SCOPE = (
    'An explicit typed association between retained metadata or concept records. '
    'Its predicate and source assertion status are preserved. It does not '
    'establish geographic feature topology, feature identity, data availability, '
    'access permission or additional reuse rights.'
)
OMISSION_SCOPE = (
    'Only explicit top-level JSON-LD references whose source and target both '
    'resolve to retained record routes are graph rows. External references and '
    'nested semantic entities remain in the complete source metadata; their '
    'absence from this graph is not evidence that they have no relationships.'
)


def _iri(value, label):
    if (not isinstance(value, str) or not value
            or re.search(r'''[\s<>"'\\\x00-\x1f\x7f]''', value)
            or re.search(r'%(?![0-9a-fA-F]{2})', value)):
        raise ValueError('Invalid ' + label + ' IRI')
    parsed = urlsplit(value)
    if parsed.scheme == 'urn':
        if not parsed.path:
            raise ValueError('Invalid ' + label + ' IRI')
        return value
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError('Invalid ' + label + ' IRI port') from error
    if (parsed.scheme not in ('http', 'https') or not parsed.hostname
            or parsed.username or parsed.password or port is not None and not 1 <= port <= 65535):
        raise ValueError('Unsafe ' + label + ' IRI')
    forbidden = {'key', 'apikey', 'token', 'accesstoken', 'clientsecret', 'password',
                 'signature', 'sig', 'authorization', 'secret'}
    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        key = re.sub('[^a-z0-9]', '', unquote(unquote(key)).lower())
        if key in forbidden:
            raise ValueError('Credential parameter in ' + label + ' IRI')
    return value


def _predicate(key):
    if key.startswith(('http://', 'https://')):
        return _iri(key, 'predicate')
    prefix, _, local = key.partition(':')
    if prefix not in PREFIXES or not local:
        raise ValueError('Undeclared explicit relationship predicate: ' + key)
    return _iri(PREFIXES[prefix] + local, 'predicate')


def _pointer(value):
    return value.replace('~', '~0').replace('/', '~1')


def _capture_timestamp(value):
    if (not isinstance(value, str)
            or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', value)):
        raise ValueError('Explicit UTC relationship capture timestamp is required')
    datetime.fromisoformat(value.replace('Z', '+00:00'))


def _source_value(parent, pointer):
    current = parent
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        try:
            current = current[int(part)] if isinstance(current, list) else current[part]
        except (KeyError, IndexError, ValueError, TypeError) as error:
            raise ValueError('Relationship evidence pointer does not resolve in its source record') from error
    return current


@lru_cache(maxsize=1)
def _validator():
    path = Path(__file__).resolve().parents[2] / 'okf-plus/schemas/explorer-relationship.schema.json'
    schema = load_json(path.read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_relationships(relationships, routes=None, semantic=None):
    """Validate every generated row and its semantic identity, not a sample."""
    validator = _validator()
    ids = set()
    for row in relationships:
        validator.validate(row)
        _capture_timestamp(row['observed_at'])
        for key in ('source_iri', 'target_iri', 'predicate'):
            _iri(row[key], key)
        identity = {'source': row['source_iri'], 'predicate': row['predicate'], 'target': row['target_iri']}
        expected = 'urn:gis-ai-go:relationship:sha256:' + sha(canonical(identity))
        if row['id'] != expected or row['id'] in ids:
            raise ValueError('Duplicate or mismatched relationship assertion identity')
        ids.add(row['id'])
        if routes is not None and (routes.get(row['source_iri']) != row['source']
                                   or routes.get(row['target_iri']) != row['target']):
            raise ValueError('Relationship endpoint does not resolve to its retained record route')
        if row['assertion_status'] != STATUS[row['source_assertion_status']]:
            raise ValueError('Relationship source assertion status was changed')
        if row['provenance']['source_record'] != row['source_iri']:
            raise ValueError('Relationship provenance refers to a different source record')
        parent = semantic[row['source_iri']] if semantic is not None else None
        if parent is not None:
            if (sha(canonical(parent)) != row['provenance']['source_record_sha256']
                    or parent.get('assertionStatus') != row['source_assertion_status']
                    or parent.get('rights') != row['rights']['inherited_record_rights']):
                raise ValueError('Relationship governance differs from its retained source record')
        for evidence in row['evidence']:
            _iri(evidence['url'], 'evidence')
            if (evidence['source_artifact'] != 'okf-plus/' + row['source']
                    or evidence['source_sha256'] != row['provenance']['source_record_sha256']
                    or _predicate(evidence['source_field']) != row['predicate']):
                raise ValueError('Relationship evidence refers to a different source field or record')
            if sha(canonical(evidence['source_value'])) != evidence['source_value_sha256']:
                raise ValueError('Relationship evidence source value checksum mismatch')
            if evidence['source_value'].get('@id') != row['target_iri']:
                raise ValueError('Relationship evidence target differs from the assertion')
            if parent is not None and _source_value(parent, evidence['locator']) != evidence['source_value']:
                raise ValueError('Relationship evidence value differs from its source pointer')
    return len(relationships)


def _references(parent):
    """Yield explicit record-root references; do not recurse into JSON literals."""
    for key, value in sorted(parent.items()):
        if key.startswith('@') or ':' not in key:
            continue
        values = value if isinstance(value, list) else [value]
        for index, item in enumerate(values):
            if not isinstance(item, dict) or '@id' not in item:
                continue
            target = _iri(item['@id'], 'reference target')
            pointer = '/' + _pointer(key) + ('/' + str(index) if isinstance(value, list) else '')
            yield key, _predicate(key), target, pointer, item


def _evidence(row, parent, key, pointer, value, revision):
    source_artifact = 'okf-plus/' + row['route']
    url = ('https://github.com/chris-page-gov/gis-ai-go/blob/' + revision + '/' + source_artifact
           if revision else row['id'])
    return {
        'url': _iri(url, 'normalised source'),
        'type': 'explicit-jsonld-record-reference',
        'source_field': key,
        'locator': pointer,
        'source_artifact': source_artifact,
        'source_sha256': sha(canonical(parent)),
        'source_hash_canonicalization': 'canonical-json-utf8',
        'source_value': deepcopy(value),
        'source_value_sha256': sha(canonical(value)),
        'source_value_hash_canonicalization': 'canonical-json-utf8',
        'field_provenance': 'Retained normalised JSON-LD front matter; not a new source capture.',
    }


def project_relationships(rows, semantic, *, captured_at, source_revision=None):
    """Return ``(rows, coverage)`` for explicit internal record associations.

    ``rows`` uses the existing complete Reader routes. ``semantic`` is the
    validated ``@id`` → complete front-matter mapping used by that Reader.
    Omission groups commit every unprojected reference occurrence using a
    digest of sorted occurrence identities, with bounded examples for review.
    """
    _capture_timestamp(captured_at)
    if source_revision is not None and not re.fullmatch('[0-9a-f]{40}', source_revision):
        raise ValueError('Relationship source revision must be a complete commit SHA')
    routes = {row['id']: row['route'] for row in rows}
    by_id = {row['id']: row for row in rows}
    if (len(routes) != len(rows) or len(set(routes.values())) != len(rows)
            or set(routes) != set(semantic)):
        raise ValueError('Relationship input identities or Reader routes differ')
    for identifier, route in routes.items():
        _iri(identifier, 'source record')
        if (not isinstance(route, str) or not re.fullmatch(r'records(?:/[A-Za-z0-9._~-]+)+', route)
                or any(part in ('.', '..') for part in route.split('/'))):
            raise ValueError('Unsafe relationship Reader route')
        if semantic[identifier].get('@id') != identifier:
            raise ValueError('Semantic record identity differs from its relationship route')

    labels = {_predicate(key): values for key, values in PREDICATES.items()}
    result = {}
    source_counts = Counter()
    projected_counts = Counter()
    omitted = defaultdict(list)
    projected_occurrences = 0
    for identifier in sorted(routes):
        row, parent = by_id[identifier], semantic[identifier]
        for key, predicate, target, pointer, value in _references(parent):
            source_counts[predicate] += 1
            occurrence = {'source_iri': identifier, 'predicate': predicate,
                          'target_iri': target, 'source_pointer': pointer}
            if target not in routes:
                omitted[(predicate, 'external-or-nested-target-not-a-retained-record')].append(occurrence)
                continue
            if predicate not in labels:
                raise ValueError('Unsupported internal record relationship predicate: ' + predicate)
            source_status = parent.get('assertionStatus')
            if source_status not in STATUS:
                raise ValueError('Unknown source relationship assertion status')
            if not isinstance(parent.get('rights'), dict) or not isinstance(parent['rights'].get('metadata'), str):
                raise ValueError('Source relationship metadata rights are required')
            identity = {'source': identifier, 'predicate': predicate, 'target': target}
            assertion_id = 'urn:gis-ai-go:relationship:sha256:' + sha(canonical(identity))
            evidence = _evidence(row, parent, key, pointer, value, source_revision)
            projected_occurrences += 1
            projected_counts[predicate] += 1
            if assertion_id in result:
                result[assertion_id]['evidence'].append(evidence)
                continue
            synthetic = parent.get('reviewStatus') == 'synthetic'
            kind, label, inverse = labels[predicate]
            result[assertion_id] = {
                'schema': SCHEMA, 'id': assertion_id,
                'source': routes[identifier], 'target': routes[target],
                'source_iri': identifier, 'target_iri': target, 'predicate': predicate,
                'kind': kind, 'label': label, 'inverse_label': inverse,
                'assertion_status': STATUS[source_status],
                'source_assertion_status': source_status,
                'assertion_scope': 'synthetic-fixture' if synthetic else 'real-world',
                'scope': SCOPE,
                'authority': {'class': 'synthetic' if synthetic else 'derived',
                              'label': 'GIS AI GO deterministic projection of retained typed links',
                              'source': evidence['url']},
                'derivation': DERIVATION,
                'observed_at': captured_at,
                'freshness': 'unknown',
                'review_status': parent.get('reviewStatus', 'not-recorded'),
                'source_lifecycle_status': parent.get('status', 'not-recorded'),
                'evidence': [evidence],
                'rights': {'source': evidence['url'], 'assertion': parent['rights']['metadata'],
                           'inherited_record_rights': deepcopy(parent['rights']),
                           'no_rights_expansion': True},
                'provenance': {'source_record': identifier,
                               'source_record_sha256': sha(canonical(parent)),
                               'source_record_hash_canonicalization': 'canonical-json-utf8',
                               'sources': deepcopy(parent.get('sources', [])),
                               **({'source_revision': source_revision} if source_revision else {})},
            }

    relationships = sorted(result.values(), key=lambda item: (item['source'], item['predicate'], item['target'], item['id']))
    for row in relationships:
        row['evidence'].sort(key=lambda item: (item['source_field'], item['locator']))
    validate_relationships(relationships, routes, semantic)

    groups = []
    for (predicate, reason), occurrences in sorted(omitted.items()):
        occurrences.sort(key=canonical)
        groups.append({'predicate': predicate, 'reason': reason, 'count': len(occurrences),
                       'occurrence_ids_sha256': sha(canonical([sha(canonical(item)) for item in occurrences])),
                       'examples': occurrences[:MAX_OMISSION_EXAMPLES],
                       'examples_omitted': max(0, len(occurrences) - MAX_OMISSION_EXAMPLES)})
    omitted_count = sum(item['count'] for item in groups)
    return relationships, {
        'schema': 'gis-ai-go.explorer-relationship-coverage.v1',
        'scope': OMISSION_SCOPE,
        'input_records': len(rows),
        'explicit_top_level_reference_occurrences': sum(source_counts.values()),
        'retained_record_reference_occurrences': projected_occurrences,
        'projected_assertions': len(relationships),
        'duplicate_reference_occurrences': projected_occurrences - len(relationships),
        'unprojected_reference_occurrences': omitted_count,
        'source_predicate_counts': dict(sorted(source_counts.items())),
        'projected_predicate_counts': dict(sorted(projected_counts.items())),
        'unprojected_groups': groups,
        'all_internal_record_references_projected': True,
        'all_projected_assertions_schema_validated': len(relationships),
        'metadata_records_unchanged': True,
    }
