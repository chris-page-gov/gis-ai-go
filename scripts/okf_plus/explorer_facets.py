"""Source-backed, finite facet dimensions for the large Explorer projection.

The complete source record stays authoritative. This module only selects named
scalar fields for navigation; it does not infer licences, publishers, units or
spatial reference systems from record names, links or descriptive prose.
"""
from __future__ import annotations

import math
import re
from urllib.parse import parse_qsl, unquote, urlsplit


# Order is presentation order, not semantic priority. The four suggested facets
# remain folded by the consumer; the remaining dimensions are available in All.
FACET_DEFINITIONS = (
    {'key': 'record_type', 'label': 'Record type', 'source_paths': ['type'], 'shown': True},
    {'key': 'source_family', 'label': 'Source family', 'source_paths': ['sourceFamily'], 'shown': True},
    {'key': 'tag', 'label': 'Tag', 'source_paths': ['tags[]'], 'shown': True},
    {'key': 'source_publisher', 'label': 'Publisher', 'source_paths': ['dcterms:publisher[].@id'], 'shown': False},
    {'key': 'review_status', 'label': 'Review status', 'source_paths': ['reviewStatus'], 'shown': True},
    {'key': 'assertion_status', 'label': 'Assertion status', 'source_paths': ['assertionStatus'], 'shown': False},
    {'key': 'lifecycle_status', 'label': 'Record lifecycle', 'source_paths': ['status'], 'shown': False},
    {'key': 'temporal_status', 'label': 'Temporal evidence', 'source_paths': ['temporal.status'], 'shown': False},
    {'key': 'temporal_kind', 'label': 'Temporal extent kind', 'source_paths': ['temporal.kind'], 'shown': False},
    {'key': 'update_frequency', 'label': 'Update frequency', 'source_paths': ['update.frequency.label'], 'shown': False},
    {'key': 'update_frequency_status', 'label': 'Update frequency evidence', 'source_paths': ['update.frequency.status'], 'shown': False},
    {'key': 'release_version', 'label': 'Source release version', 'source_paths': ['update.releaseVersion'], 'shown': False},
    {'key': 'retrieval_authority', 'label': 'Retrieval authority', 'source_paths': ['rights.retrievalAuthority'], 'shown': False},
    {'key': 'source_evidence_kind', 'label': 'Source evidence kind', 'source_paths': ['sources[].evidenceKind'], 'shown': False},
    {'key': 'unit', 'label': 'Source unit', 'source_paths': ['details.unit_of_measure', 'details.unit', 'qudt:unit'], 'shown': False},
    {'key': 'spatial_reference', 'label': 'Native spatial reference', 'source_paths': ['details.spatialReference'], 'shown': False},
    {'key': 'crs', 'label': 'Advertised CRS', 'source_paths': ['details.crs[]'], 'shown': False},
    {'key': 'storage_crs', 'label': 'Storage CRS', 'source_paths': ['details.storageCrs'], 'shown': False},
)

_CREDENTIAL_QUERY_KEYS = {
    'key', 'apikey', 'token', 'accesstoken', 'clientsecret', 'password',
    'signature', 'sig', 'authorization', 'secret',
}


def _values(value):
    """Retain exact nonblank scalar values, including explicit unknown states.

    Missing fields and nulls do not acquire a fabricated ``unknown`` value.
    JSON-LD value/IRI objects are read only at the explicitly selected field;
    other objects are never stringified or recursively mined for facet values.
    """
    result = set()

    def collect(item):
        if isinstance(item, list):
            for child in item:
                collect(child)
        elif isinstance(item, dict):
            if '@value' in item:
                collect(item['@value'])
            elif '@id' in item:
                collect(item['@id'])
        elif isinstance(item, str):
            if item.strip():
                result.add(item)
        elif isinstance(item, int) and not isinstance(item, bool):
            result.add(str(item))
        elif isinstance(item, float):
            if not math.isfinite(item):
                raise ValueError('Facet values must be finite source scalars')
            result.add(str(item))

    collect(value)
    return sorted(result)


def _object(value):
    return value if isinstance(value, dict) else {}


def _publisher_iri(value):
    """Check a source publisher's web IRI without rewriting its identity."""
    if (not isinstance(value, str) or not value or
            any(ord(character) <= 32 or ord(character) == 127 for character in value) or
            any(character in value for character in ("'", '|', '^')) or
            any(character in value for character in '\\"<>`{}') or
            re.search(r'%(?![0-9a-fA-F]{2})', value)):
        raise ValueError('Publisher identity must be a safe absolute HTTP(S) IRI')
    try:
        parts = urlsplit(value)
        port = parts.port
        if (parts.scheme not in ('http', 'https') or not parts.hostname or
                parts.username is not None or parts.password is not None or
                '%' in parts.netloc or port is not None and not 1 <= port <= 65535):
            raise ValueError('Unsafe publisher identity')
    except ValueError as error:
        raise ValueError('Publisher identity must be a safe absolute HTTP(S) IRI') from error
    for key, _ in parse_qsl(parts.query, keep_blank_values=True):
        normal = re.sub('[^a-z0-9]', '', unquote(unquote(key)).lower())
        if normal in _CREDENTIAL_QUERY_KEYS:
            raise ValueError('Credential parameter in publisher identity')
    return value


def publisher_label_candidates(metadata):
    """Return only explicit publisher identities, with source display labels.

    A source-family name or a literal publisher name cannot establish a web
    identity. Such values remain in the complete metadata but do not mint a
    publisher entity. Different IRIs with the same label remain distinct.
    Conflicting display labels for one IRI fall back to that IRI; source order
    must not silently choose an authoritative preferred label.
    """
    raw = metadata.get('dcterms:publisher')
    items = raw if isinstance(raw, list) else [raw]
    publishers = {}
    for item in items:
        if not isinstance(item, dict) or '@id' not in item:
            continue
        identifier = _publisher_iri(item['@id'])
        candidates = publishers.setdefault(identifier, set())
        for key in ('skos:prefLabel', 'rdfs:label', 'schema:name'):
            labels = _values(item.get(key))
            if labels:
                candidates.update(labels)
                break
    return [{'id': identifier, 'labels': sorted(labels)} for identifier, labels in sorted(publishers.items())]


def publisher_rows(metadata):
    """Return explicit identities without choosing conflicting source labels."""
    return [{'id': row['id'], 'label': row['labels'][0] if len(row['labels']) == 1 else row['id']}
            for row in publisher_label_candidates(metadata)]


def facet_values(metadata):
    """Project the named source fields into exact multivalued facet values.

    Use these same lists in static postings, search result rows and full Reader
    rows. Source/native spellings and identifiers stay unchanged; for example,
    an ArcGIS ``27700`` is not silently equated with an OGC EPSG URI.
    """
    temporal = _object(metadata.get('temporal'))
    update = _object(metadata.get('update'))
    frequency = _object(update.get('frequency'))
    rights = _object(metadata.get('rights'))
    details = _object(metadata.get('details'))
    sources = metadata.get('sources')
    sources = sources if isinstance(sources, list) else []
    values = {
        'record_type': _values(metadata.get('type')),
        'source_family': _values(metadata.get('sourceFamily')),
        'tag': _values(metadata.get('tags')),
        'source_publisher': [publisher['id'] for publisher in publisher_rows(metadata)],
        'review_status': _values(metadata.get('reviewStatus')),
        'assertion_status': _values(metadata.get('assertionStatus')),
        'lifecycle_status': _values(metadata.get('status')),
        'temporal_status': _values(temporal.get('status')),
        'temporal_kind': _values(temporal.get('kind')),
        'update_frequency': _values(frequency.get('label')),
        'update_frequency_status': _values(frequency.get('status')),
        'release_version': _values(update.get('releaseVersion')),
        'retrieval_authority': _values(rights.get('retrievalAuthority')),
        'source_evidence_kind': _values([_object(source).get('evidenceKind') for source in sources]),
        'unit': _values([details.get('unit_of_measure'), details.get('unit'), metadata.get('qudt:unit')]),
        'spatial_reference': _values(details.get('spatialReference')),
        'crs': _values(details.get('crs')),
        'storage_crs': _values(details.get('storageCrs')),
    }
    if set(values) != {definition['key'] for definition in FACET_DEFINITIONS}:
        raise AssertionError('Every declared facet must have one explicit source mapping')
    return values


def presentation_facets():
    """Canonical consumer presentation entries; no application fork required."""
    return [
        {'key': definition['key'], 'label': definition['label'],
         'default_state': 'shown' if definition['shown'] else 'hidden'}
        for definition in FACET_DEFINITIONS
    ]
