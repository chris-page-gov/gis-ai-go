"""Project retained citations and explicit publishers for Explorer discovery.

These resources are record-to-source-reference associations, not downloadable
data distributions.  Link mode never fetches a provider response in Explorer.
"""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import re
from urllib.parse import quote, urlsplit

try:
    from .explorer_facets import publisher_rows, publisher_label_candidates
    from .model import digest, safe_reference
except ImportError:
    from explorer_facets import publisher_rows, publisher_label_candidates
    from model import digest, safe_reference


UNKNOWN_MEDIA_TYPE = 'not-established'
REFERENCE_SCOPE = (
    'Retained source citation only. Availability, response media type, described '
    'data downloadability and retrieval permission are not established by this link.'
)


def _sources(metadata, unprojected):
    """Keep every explicitly retained reference and its original JSON pointer."""
    found = {}

    def add(url, pointer, role, title=None):
        if url is None or url == '':
            return
        # The accepted GIS input profile already restricts source URLs to HTTPS.
        # Recheck here so a standalone caller cannot publish credentials or an
        # executable/relative URL through this generated navigation plane.
        safe_reference(url)
        if '{' in url or '}' in url:
            # Preserve unescaped native identifiers and URI templates in the
            # complete record. They are not concrete, canonical browser links;
            # silently rewriting them would change the retained source value.
            unprojected.append({'source_field': pointer, 'url_sha256': digest(url),
                                'reason': 'unescaped-or-template-source-url'})
            return
        if (any(character in url for character in "\"'<>\\^`{|}") or
                re.search(r'%(?![0-9a-fA-F]{2})', url) or '%' in urlsplit(url).netloc):
            raise ValueError('Unsafe source-reference URL text')
        item = found.setdefault(url, {'source_fields': [], 'roles': set(), 'labels': set()})
        item['source_fields'].append(pointer)
        item['roles'].add(role)
        if isinstance(title, str) and title.strip():
            item['labels'].add(title)

    add(metadata.get('resource'), '/resource', 'landing-page')
    sources = metadata.get('sources', [])
    if not isinstance(sources, list):
        raise ValueError('Retained source references must be an array')
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ValueError('Retained source reference must be an object')
        add(source.get('resource'), f'/sources/{index}/resource', 'evidence-citation', source.get('referenceTitle'))
    return found


def project_resources(rows, semantic):
    """Return resources, publishers, per-record fields and complete coverage.

    ``rows`` uses the validated search-index identity/route contract, while
    ``semantic`` maps those record IDs to their unchanged full metadata.  An
    entity is never minted for a guessed publisher or a source-family label.
    """
    resources = []
    by_record = {}
    publishers = {}
    publisher_record_ids = defaultdict(set)
    publisher_labels = defaultdict(set)
    publisher_resources = defaultdict(int)
    distinct_urls = set()
    records_with_publisher_property = 0
    records_with_unresolved_publisher_property = 0
    records_with_multiple_publishers = 0
    source_field_count = 0
    unprojected = []

    for row in rows:
        record_id = row.get('id')
        route = row.get('route')
        if not isinstance(record_id, str) or not record_id or record_id in by_record:
            raise ValueError('Source-reference projection requires unique record IDs')
        if not isinstance(route, str) or not route.startswith('records/'):
            raise ValueError('Source-reference projection requires an exact Reader route')
        metadata = semantic.get(record_id)
        if not isinstance(metadata, dict) or metadata.get('@id') != record_id:
            raise ValueError('Source-reference metadata identity mismatch')
        dataset_name = route.removeprefix('records/')
        reference_rows = []
        record_digest = digest(metadata)
        missing_links = []
        for url, source in sorted(_sources(metadata, missing_links).items()):
            identifier = 'source-reference-' + digest([record_id, url])
            labels = sorted(source['labels'])
            # A contradictory set of supplied labels must not silently acquire
            # one preferred source title. The exact URL is always available.
            title = labels[0] if len(labels) == 1 else url
            reference = {
                'id': identifier,
                'dataset': dataset_name,
                'route': 'resource/' + identifier,
                'name': title,
                'url': url,
                'host': urlsplit(url).hostname,
                'resource_type': 'source-reference',
                'description': REFERENCE_SCOPE,
                'source_access': {
                    'url': url, 'label': 'Retained source reference',
                    'media_type': UNKNOWN_MEDIA_TYPE, 'display_mode': 'link',
                },
                'provenance': {
                    'schema': 'gis-ai-go.explorer-source-reference.v1',
                    'record_id': record_id,
                    'record_route': route,
                    'record_sha256': record_digest,
                    'canonicalisation': 'canonical-json-utf8-with-final-newline',
                    'source_fields': sorted(set(source['source_fields'])),
                    'reference_roles': sorted(source['roles']),
                    'source_labels': labels,
                    'derivation': 'explicit-retained-reference-projection',
                    'scope': REFERENCE_SCOPE,
                },
                'rights': deepcopy(metadata.get('rights', {})),
                'downloadability': 'not-established',
                'execution_admitted': False,
            }
            resources.append(reference)
            reference_rows.append(reference)
            distinct_urls.add(url)
            source_field_count += len(reference['provenance']['source_fields'])
        unprojected.extend({'record_id': record_id, **item} for item in missing_links)

        explicit_publishers = publisher_rows(metadata)
        for candidate in publisher_label_candidates(metadata):
            publisher_labels[candidate['id']].update(candidate['labels'])
        if 'dcterms:publisher' in metadata:
            records_with_publisher_property += 1
            if not explicit_publishers:
                records_with_unresolved_publisher_property += 1
        if len(explicit_publishers) > 1:
            records_with_multiple_publishers += 1
        source_publishers = []
        for publisher in explicit_publishers:
            iri, label = publisher['id'], publisher['label']
            source_publishers.append({'name': iri, 'title': label})
            publisher_record_ids[iri].add(record_id)
            publisher_resources[iri] += len(reference_rows)
            if label != iri:
                publisher_labels[iri].add(label)
            publishers.setdefault(iri, {'id': iri, 'name': iri,
                'route': 'publisher/' + quote(iri, safe='-._~'), 'concept_id': iri})
        # The consumer's scalar publisher field draws "published by" edges.
        # An arbitrary primary publisher must not be chosen from co-publishers.
        sole = source_publishers[0] if len(source_publishers) == 1 else None
        by_record[record_id] = {
            'publisher': sole['name'] if sole else '',
            'publisher_title': sole['title'] if sole else '',
            'source_publishers': source_publishers,
            'resource_count': len(reference_rows),
            'resource_ids': sorted(item['id'] for item in reference_rows),
            'resource_hosts': sorted({item['host'] for item in reference_rows}),
        }

    for iri, publisher in publishers.items():
        labels = sorted(publisher_labels[iri])
        publisher.update({
            'title': labels[0] if len(labels) == 1 else iri,
            'dataset_count': len(publisher_record_ids[iri]),
            'resource_count': publisher_resources[iri],
            'source_labels': labels,
            'provenance': {
                'schema': 'gis-ai-go.explorer-publisher-reference.v1',
                'source_property': 'dcterms:publisher',
                'record_count': len(publisher_record_ids[iri]),
                'record_ids_sha256': digest(sorted(publisher_record_ids[iri])),
                'label_status': 'source-stated' if len(labels) == 1 else (
                    'conflicting-source-labels' if labels else 'not-recorded'),
                'derivation': 'explicit-retained-publisher-identity',
            },
        })
    resources.sort(key=lambda item: item['id'])
    publisher_output = [publishers[iri] for iri in sorted(publishers)]
    coverage = {
        'schema': 'gis-ai-go.explorer-resource-coverage.v1',
        'input_records': len(rows),
        'source_reference_associations': len(resources),
        'distinct_source_urls': len(distinct_urls),
        'projected_source_field_occurrences': source_field_count,
        'unprojected_source_field_occurrences': len(unprojected),
        'unprojected_source_fields': sorted(unprojected, key=lambda item: (item['record_id'], item['source_field'])),
        'records_with_source_references': sum(bool(item['resource_ids']) for item in by_record.values()),
        'publisher_entities': len(publisher_output),
        'records_with_publisher_property': records_with_publisher_property,
        'records_with_projected_publishers': sum(bool(item['source_publishers']) for item in by_record.values()),
        'records_with_unresolved_publisher_property': records_with_unresolved_publisher_property,
        'records_with_multiple_publishers': records_with_multiple_publishers,
        'downloadability': 'not-established',
        'resource_scope': 'Record-to-source-reference associations; not downloadable data distributions.',
    }
    return resources, publisher_output, by_record, coverage
