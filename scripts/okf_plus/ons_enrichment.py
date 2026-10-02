#!/usr/bin/env python3
"""Metadata-only ONS/Nomis enrichment through the shared bounded Capture.

No network work occurs on import. The caller controls request admission, pacing,
body limits and the cumulative ledger ceiling through Capture. Latest ONS versions
are a current snapshot, not a traversal of the historical edition/version graph.
Nomis overview release dates are deliberately never used as observation periods.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlencode, urlsplit

try:
    from .harvest import Capture, ROOT, clean_text
except ImportError:  # Direct script invocation.
    from harvest import Capture, ROOT, clean_text

ONS_BASE = 'https://api.beta.ons.gov.uk/v1'
NOMIS_BASE = 'https://www.nomisweb.co.uk/api/v01/dataset'
NOMIS_SELECT = 'DatasetInfo,Coverage,DateMetadata,Dimensions,DimensionMetadata'
NOMIS_ID_RE = re.compile(r'NM_[0-9]+_[0-9]+')
CENSUS_TYPES = frozenset({'cantabular_flexible_table', 'cantabular_multivariate_table'})
VERSION_RE = re.compile(
    r'/v1/datasets/([A-Za-z0-9_-]+)/editions/([A-Za-z0-9_-]+)/versions/([0-9]+)'
)


def _source(cap, name):
    raw = (cap.public / (name + '.json')).read_bytes()
    data = json.loads(raw)
    records = data['records']
    if not isinstance(records, list) or any(not isinstance(x, dict) for x in records):
        raise ValueError('Source records must be objects')
    ids = [x.get('id') for x in records]
    if any(not isinstance(x, str) for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('Source identifiers must be unique strings')
    return records, hashlib.sha256(raw).hexdigest()


def _existing(cap, name, source_hash):
    path = cap.public / (name + '.json')
    if not path.exists():
        return {}, []
    data = json.loads(path.read_text())
    if data['coverage'].get('inputSha256') != source_hash:
        raise ValueError('Enrichment input changed; retain prior snapshot before replacing it')
    return {x['id']: x for x in data['records']}, data['receipts']


def _selection(records, start, limit):
    if type(start) is not int or start < 0 or (limit is not None and (type(limit) is not int or limit < 1)):
        raise ValueError('Batch start/limit must be non-negative/positive integers')
    return records[start:None if limit is None else start + limit]


def _deduplicate_receipts(receipts):
    unique = {}
    for receipt in receipts:
        unique[(receipt['url'], receipt.get('retrievedAt'), receipt.get('sha256'))] = receipt
    return list(unique.values())


def _evidence(receipt):
    return {k: receipt[k] for k in ('url', 'retrievedAt', 'sha256', 'status') if k in receipt}


def _strings(data, keys):
    return {k: clean_text(data[k]) for k in keys if isinstance(data.get(k), str)}


def _dimension(data):
    if not isinstance(data, dict) or not isinstance(data.get('name'), str):
        raise ValueError('Invalid ONS dimension')
    # Free-form contacts and arbitrary embedded objects are not projected.
    result = _strings(data, ('name', 'label', 'description', 'id'))
    result['name'] = data['name']
    code_list = data.get('links', {}).get('code_list', {})
    if isinstance(code_list, dict) and isinstance(code_list.get('id'), str):
        result['codeListId'] = code_list['id']
    # A dimension ID is not, by itself, evidence of a published code-list link.
    return result


def _latest_url(record):
    href = record.get('links', {}).get('latest_version', {}).get('href')
    if not isinstance(href, str):
        return None
    parsed = urlsplit(href)
    match = VERSION_RE.fullmatch(parsed.path)
    if (parsed.scheme != 'https' or parsed.netloc != 'api.beta.ons.gov.uk'
            or parsed.query or parsed.fragment or not match
            or match.group(1) != record['id']):
        raise ValueError('Latest-version link violates the fixed ONS metadata contract')
    return href, match.group(2), match.group(3)


def _link_is(links, name, href, identifier=None):
    link = links.get(name) if isinstance(links, dict) else None
    return (isinstance(link, dict) and link.get('href') == href
            and (identifier is None or link.get('id') == identifier))


def _metadata_contract(source, data, version_url, edition, version):
    """Validate observed ONS metadata variants without borrowing identity facts.

    Filterable/static metadata carries scalar dataset identity. Census metadata
    instead binds it through dataset_links and a typed Cantabular basis. Absence
    of a static dimension list is legitimate; it is not a time-coverage claim.
    """
    native_version = data.get('version')
    if type(native_version) not in (int, str) or str(native_version) != version:
        raise ValueError('Metadata version differs from advertised version')
    source_type = source.get('type')
    if source_type in CENSUS_TYPES:
        dataset_url = ONS_BASE + '/datasets/' + source['id']
        links, basis = data.get('dataset_links'), data.get('is_based_on')
        if (not _link_is(links, 'self', dataset_url)
                or not _link_is(links, 'editions', dataset_url + '/editions')
                or not _link_is(links, 'latest_version', version_url, version)
                or not isinstance(basis, dict) or basis.get('@type') != source_type
                or not isinstance(basis.get('@id'), str) or not basis['@id']
                or any(key in data and data[key] != expected for key, expected in
                       (('id', source['id']), ('edition', edition), ('type', source_type)))):
            raise ValueError('Census metadata identity contract mismatch')
        variant = 'cantabular-dataset-links'
        identity = {'datasetLinks': {key: {field: links[key][field] for field in ('href', 'id') if field in links[key]}
                                     for key in ('self', 'editions', 'latest_version')},
                    'isBasedOn': {key: basis[key] for key in ('@id', '@type')}}
        dimensions = data.get('dimensions')
    else:
        if data.get('id') != source['id'] or data.get('edition') != edition:
            raise ValueError('Metadata dataset or edition identity mismatch')
        if source_type == 'static':
            if (data.get('type') != 'static'
                    or not _link_is(data.get('links'), 'self', version_url + '/metadata')
                    or not _link_is(data.get('links'), 'version', version_url, version)):
                raise ValueError('Static metadata identity contract mismatch')
            variant = 'static-scalar-identity'
            dimensions = data.get('dimensions', [])
        else:
            if source_type not in (None, 'filterable') or data.get('type') not in (None, 'filterable'):
                raise ValueError('Unsupported metadata type')
            variant = 'filterable-scalar-identity'
            dimensions = data.get('dimensions')
        identity = {'id': data['id'], 'edition': data['edition'], 'version': native_version}
    if not isinstance(dimensions, list):
        raise ValueError('Invalid dimension list for metadata variant')
    return dimensions, {'variant': variant, 'catalogueType': source_type,
                        'identityEvidence': identity, 'dimensionListPresent': 'dimensions' in data}


class CacheOnlyCapture:
    """Reuse checksum-verified successful receipts; never admit a cache miss."""

    def __init__(self, capture):
        self.capture = capture
        self.public = capture.public

    def get(self, url, kind='json'):
        if not any(r.get('url') == url and r.get('status') == 200
                   for r in self.capture.ledger['requests']):
            previous=next((r for r in reversed(self.capture.ledger['requests']) if r.get('url')==url),None)
            if previous is not None:return None,dict(previous)
            return None, {'url': url, 'status': 'not-captured-cache-only'}
        # Capture verifies the retained body digest before returning a cache hit.
        return self.capture.get(url, kind)

    def save(self, *args):
        return self.capture.save(*args)


def _period_key(value):
    """Only compare recognised native period codes; never parse titles/labels."""
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r'([0-9]{4})(?:-([0-9]{2})(?:-([0-9]{2}))?|[- ]Q([1-4]))?', value)
    if not match:
        return None
    year, month, day, quarter = match.groups()
    try:
        if quarter:
            date(int(year), int(quarter) * 3, 1)
            return 'quarter', (int(year), int(quarter))
        date(int(year), int(month or 1), int(day or 1))
        return ('day' if day else 'month' if month else 'year'), (int(year), int(month or 1), int(day or 1))
    except ValueError:
        return None


def native_period_bounds(options, complete):
    """Return extrema only for a complete, uniform, recognised code set."""
    values = [x['option'] for x in options]
    parsed = [_period_key(x) for x in values]
    result = {'minimumNative': None, 'maximumNative': None,
              'basis': 'published time-dimension option codes; no observations',
              'continuityEstablished': False}
    if not complete:
        result['status'] = 'unknown-incomplete-options'
    elif not values:
        result['status'] = 'unknown-no-options'
    elif all(type(value) is int and 1000 <= value <= 9999 for value in values):
        # Nomis SDMX JSON uses native JSON integers for annual codes. Preserve
        # their type and compare only the reviewed four-digit integer variant;
        # a numeric label, decimal, epoch or mixed lexical set is not evidence.
        result.update(status='known-option-extrema', minimumNative=min(values),
                      maximumNative=max(values), granularity='year',
                      comparisonRule='Nomis-native-integer-year.v1')
    elif any(x is None for x in parsed) or len({x[0] for x in parsed}) != 1:
        result['status'] = 'unknown-unrecognised-or-mixed-period-codes'
    else:
        ordered = sorted(zip(parsed, values), key=lambda x: (x[0][1], x[1]))
        result.update(status='known-option-extrema', minimumNative=ordered[0][1],
                      maximumNative=ordered[-1][1], granularity=parsed[0][0],
                      comparisonRule='ONS-native-ISO-period-code.v1')
    return result


def _time_options(cap, version_url, receipts, page_size, max_pages):
    options = []; seen = set(); offset = 0; total = None; stable = True
    duplicate_count = 0; complete = False; reason = 'page-ceiling'
    for _ in range(max_pages):
        url = version_url + '/dimensions/time/options?' + urlencode({'limit': page_size, 'offset': offset})
        data, receipt = cap.get(url); receipts.append(receipt)
        if not isinstance(data, dict):
            reason = 'request-failed'; break
        items = data.get('items'); reported = data.get('total_count')
        if (not isinstance(items, list) or type(reported) is not int or reported < 0
                or data.get('offset') != offset or data.get('count') != len(items)):
            reason = 'invalid-page-contract'; break
        if total is not None and total != reported:
            stable = False
        total = reported
        valid = True
        for item in items:
            if (not isinstance(item, dict) or not isinstance(item.get('option'), str)
                    or item.get('dimension', 'time') != 'time'):
                valid = False; break
            option = _strings(item, ('option', 'label', 'dimension', 'node_id'))
            option['option'] = item['option']
            if option['option'] in seen:
                duplicate_count += 1
            else:
                seen.add(option['option']); options.append(option)
        if not valid:
            reason = 'invalid-option-contract'; break
        offset += len(items)
        if offset >= total:
            complete = stable and len(seen) == total and duplicate_count == 0
            reason = 'exhausted' if complete else 'count-mismatch-or-mutation'
            break
        if not items:
            reason = 'empty-page-before-total'; break
    result = {'options': options, 'reportedTotal': total, 'retrievedUnique': len(seen),
              'complete': complete, 'stableReportedTotal': stable,
              'duplicateCount': duplicate_count, 'stopReason': reason}
    result['bounds'] = native_period_bounds(options, complete)
    return result


def ons_versions(cap, *, start=0, limit=None, page_size=1000, max_time_pages=100):
    """Capture latest metadata and exact native `time` options for an input cohort.

    Completed batches merge only when the input snapshot hash is unchanged.
    No latest-version link, a failed request or unsupported time axis remains an
    explicit record. Network and body bounds are enforced by the shared Capture.
    """
    if type(page_size) is not int or not 1 <= page_size <= 1000 or type(max_time_pages) is not int or not 1 <= max_time_pages <= 100:
        raise ValueError('Invalid metadata pagination bounds')
    sources, source_hash = _source(cap, 'ons-datasets')
    records, receipts = _existing(cap, 'ons-latest-versions', source_hash)
    for source in _selection(sources, start, limit):
        row = {'id': source['id'], 'metadataStatus': 'not-captured',
               'temporal': {'status': 'unknown', 'reason': 'metadata-not-captured'}}
        records[row['id']] = row
        try:
            latest = _latest_url(source)
        except (ValueError, AttributeError):
            row['metadataStatus'] = 'invalid-latest-version-link'; continue
        if latest is None:
            row['metadataStatus'] = 'no-advertised-latest-version'; continue
        version_url, edition, version = latest
        row.update(edition=edition, version=version, versionUrl=version_url)
        data, receipt = cap.get(version_url + '/metadata'); receipts.append(receipt)
        row['metadataEvidence'] = _evidence(receipt)
        if not isinstance(data, dict):
            row['metadataStatus'] = 'request-failed'; continue
        try:
            raw_dimensions, contract = _metadata_contract(source, data, version_url, edition, version)
        except ValueError:
            row['metadataStatus'] = 'invalid-metadata-contract'; continue
        try:
            dimensions = [_dimension(x) for x in raw_dimensions]
        except (ValueError, AttributeError):
            row['metadataStatus'] = 'invalid-dimension-contract'; continue
        row['metadataContract'] = contract
        row['metadata'] = _strings(data, ('title', 'description', 'type', 'state',
            'release_frequency', 'release_date', 'last_updated', 'next_release', 'unit_of_measure'))
        for key in ('release_frequency', 'release_date', 'last_updated', 'next_release'):
            if isinstance(data.get(key), str):
                row['metadata'][key] = data[key]
        row['dimensions'] = dimensions
        row['metadataStatus'] = 'captured'
        if len({x['name'] for x in dimensions}) != len(dimensions):
            row['metadataStatus'] = 'invalid-duplicate-dimensions'; continue
        if 'time' not in {x['name'] for x in dimensions}:
            row['temporal'] = {'status': 'unknown', 'reason': 'no-native-time-dimension',
                               'minimumNative': None, 'maximumNative': None}
            continue
        row['temporal'] = _time_options(cap, version_url, receipts, page_size, max_time_pages)
    ordered = [records[x['id']] for x in sources if x['id'] in records]
    success = sum(x['metadataStatus'] == 'captured' for x in ordered)
    cap.save('ons-latest-versions', ordered, _deduplicate_receipts(receipts), {
        'unit': 'ONS catalogue dataset latest-version metadata', 'inputSha256': source_hash,
        'reportedTotal': len(sources), 'retrievedUnique': success, 'attemptedUnique': len(ordered),
        'catalogueComplete': False, 'latestMetadataComplete': success == len(sources),
        'timeOptionListsComplete': sum(x['temporal'].get('complete') is True for x in ordered),
        'limitations': ['Latest advertised versions only; historical editions and revisions are not traversed.',
            'No observations fetched. Time-option extrema do not establish continuity or populated cells.',
            'Only a native dimension named time is traversed; other temporal axes remain unknown.',
            'Catalogue publication/update dates and frequency are separate from observation periods.',
            'Native dimension IDs are retained; code-list IDs require an explicit code_list link.',
            'Contacts and unreviewed nested metadata are omitted from the public projection.']})


def _many(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _nomis_scalar(value):
    """Retain native text/numbers, excluding booleans and non-finite JSON values."""
    return type(value) in (str, int) or type(value) is float and math.isfinite(value)


def nomis_times(cap, *, start=0, limit=None):
    """Capture Nomis native time codes and selected revision metadata only."""
    sources, source_hash = _source(cap, 'ons-nomis-datasets')
    records, receipts = _existing(cap, 'ons-nomis-time-options', source_hash)
    for source in _selection(sources, start, limit):
        row = {'id': source['id'], 'metadataStatus': 'not-captured', 'codes': [],
               'bounds': native_period_bounds([], False)}
        records[row['id']] = row
        if not NOMIS_ID_RE.fullmatch(row['id']):
            row['metadataStatus'] = 'invalid-dataset-id'; continue
        components = source.get('components', {})
        dimension = components.get('timedimension') if isinstance(components, dict) else None
        if not isinstance(dimension, dict) or dimension.get('conceptref') != 'TIME' or not isinstance(dimension.get('codelist'), str):
            row['metadataStatus'] = 'no-advertised-time-codelist'; continue
        row['codeListId'] = dimension['codelist']
        url = NOMIS_BASE + '/' + row['id'] + '/time.def.sdmx.json'
        data, receipt = cap.get(url); receipts.append(receipt)
        row['metadataEvidence'] = _evidence(receipt)
        if not isinstance(data, dict):
            row['metadataStatus'] = 'request-failed'; continue
        try:
            if isinstance(data.get('structure'),dict) and data['structure'].get('codelists') is None:
                row['metadataStatus']='no-returned-time-codelist';continue
            lists = _many(data['structure']['codelists']['codelist'])
            if len(lists) != 1 or lists[0].get('id') != row['codeListId']:
                raise ValueError('Codelist identity mismatch')
            codes = _many(lists[0].get('code'))
            seen = set()
            for code in codes:
                if not isinstance(code, dict) or not _nomis_scalar(code.get('value')) or code['value'] in seen:
                    raise ValueError('Invalid or duplicate native time code')
                seen.add(code['value'])
                native = {'value': code['value']}
                description = code.get('description', {})
                if isinstance(description, dict):
                    if 'value' in description and not _nomis_scalar(description['value']):
                        raise ValueError('Invalid native time-code description')
                    native['description'] = {**({'value': description['value']} if 'value' in description else {}),
                                             **({'lang': description['lang']} if isinstance(description.get('lang'), str) else {})}
                annotations = code.get('annotations', {})
                entries = _many(annotations.get('annotation')) if isinstance(annotations, dict) else []
                native['revisionMetadata'] = [
                    {'title': x['annotationtitle'], 'value': x['annotationtext']}
                    for x in entries if isinstance(x, dict)
                    and x.get('annotationtitle') in {'CurrentRevisionReleased', 'CurrentRevisionStatus',
                        'CurrentRevisionVersion', 'NextRevisionReleased', 'taken on', 'period start', 'period end'}
                    and _nomis_scalar(x.get('annotationtext'))
                ]
                row['codes'].append(native)
        except (KeyError, TypeError, AttributeError, ValueError):
            row['metadataStatus'] = 'invalid-time-codelist-contract'; continue
        row['metadataStatus'] = 'captured'
        row['returnedCodeCount'] = len(codes)
        row['bounds'] = native_period_bounds([{'option': x['value']} for x in row['codes']], True)
        row['bounds']['basis'] = 'Nomis returned TIME codelist native codes; no observations'
    ordered = [records[x['id']] for x in sources if x['id'] in records]
    success = sum(x['metadataStatus'] == 'captured' for x in ordered)
    cap.save('ons-nomis-time-options', ordered, _deduplicate_receipts(receipts), {
        'unit': 'Nomis key-family native TIME codelist', 'inputSha256': source_hash,
        'reportedTotal': len(sources), 'retrievedUnique': success, 'attemptedUnique': len(ordered),
        'catalogueComplete': False, 'timeCodelistsComplete': success == len(sources),
        'temporalBoundsKnown': sum(x['bounds']['status'] == 'known-option-extrema' for x in ordered),
        'limitations': ['Complete returned metadata documents, not observation coverage or continuity.',
            'Exact native period codes/labels are retained; mixed/unrecognised syntax has unknown bounds.',
            'Native numeric types are preserved; only uniform four-digit integer codes establish numeric year extrema.',
            'Frequency is not inferred from gaps, code ordering or date-label precision.',
            'Selected date/revision annotations only; contacts and arbitrary metadata are omitted.']})


def nomis_overviews(cap, *, start=0, limit=None):
    """Capture compact dataset/release/dimension metadata, explicitly sans Contact.

    Overview does not promise period bounds or frequency values. Native TIME/FREQ
    codelist references are retained from the cohort and remain untraversed here.
    """
    sources, source_hash = _source(cap, 'ons-nomis-datasets')
    records, receipts = _existing(cap, 'ons-nomis-overviews', source_hash)
    for source in _selection(sources, start, limit):
        row = {'id': source['id'], 'metadataStatus': 'not-captured',
               'temporal': {'minimumNative': None, 'maximumNative': None, 'status': 'unknown',
                            'reason': 'compact-overview-does-not-establish-observation-period-bounds'},
               'frequency': {'status': 'unknown', 'nativeValues': []}}
        records[row['id']] = row
        if not NOMIS_ID_RE.fullmatch(row['id']):
            row['metadataStatus'] = 'invalid-dataset-id'; continue
        components = source.get('components', {})
        time_dimension = components.get('timedimension', {})
        if isinstance(time_dimension, dict):
            row['temporal']['nativeDimension'] = _strings(time_dimension, ('conceptref', 'codelist'))
        frequency_dimensions = [x for x in _many(components.get('dimension'))
                                if isinstance(x, dict) and (x.get('isfrequencydimension') in (True, 'true') or x.get('conceptref') == 'FREQ')]
        row['frequency']['nativeDimensions'] = [_strings(x, ('conceptref', 'codelist')) for x in frequency_dimensions]
        declared = source.get('annotations', {}).get('Frequency')
        if isinstance(declared, str) and declared:
            row['frequency'].update(status='declared-in-definition', nativeValues=[declared])
        url = NOMIS_BASE + '/' + row['id'] + '.overview.json?' + urlencode({'select': NOMIS_SELECT})
        data, receipt = cap.get(url); receipts.append(receipt)
        row['metadataEvidence'] = _evidence(receipt)
        if not isinstance(data, dict):
            row['metadataStatus'] = 'request-failed'; continue
        overview = data.get('overview')
        if not isinstance(overview, dict) or overview.get('id') != row['id']:
            row['metadataStatus'] = 'invalid-overview-contract'; continue
        row['metadata'] = _strings(overview, ('name', 'description', 'subdescription',
            'mnemonic', 'coverage', 'restricted', 'status', 'analysisname'))
        # Preserve these native strings exactly: no timezone or period inference.
        row['releaseDates'] = {k: overview[k] for k in ('firstreleased', 'lastrevised', 'lastupdated', 'nextupdate')
                               if isinstance(overview.get(k), str)}
        dimensions = overview.get('dimensions', {})
        raw_dimensions = _many(dimensions.get('dimension')) if isinstance(dimensions, dict) else []
        if any(not isinstance(x, dict) or not isinstance(x.get('concept'), str) for x in raw_dimensions):
            row['metadataStatus'] = 'invalid-overview-dimensions'; continue
        row['dimensions'] = [_strings(x, ('concept', 'name')) for x in raw_dimensions]
        row['metadataStatus'] = 'captured'
    ordered = [records[x['id']] for x in sources if x['id'] in records]
    success = sum(x['metadataStatus'] == 'captured' for x in ordered)
    cap.save('ons-nomis-overviews', ordered, _deduplicate_receipts(receipts), {
        'unit': 'Nomis key-family compact overview', 'inputSha256': source_hash,
        'reportedTotal': len(sources), 'retrievedUnique': success, 'attemptedUnique': len(ordered),
        'catalogueComplete': False, 'overviewComplete': success == len(sources),
        'temporalBoundsKnown': 0,
        'limitations': ['Compact overviews complement the definition catalogue; no observations or full codelists fetched.',
            'Release dates do not establish the first/last observation period.',
            'Frequency values remain unknown unless explicitly declared in the captured definition.',
            'Contact is excluded from the request and public projection.']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family', choices=['ons-versions', 'nomis-overviews', 'nomis-times'])
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--cache-only', action='store_true',
                        help='Reprocess retained successful responses; admit no new network request')
    parser.add_argument('--max-requests', type=int, required=True,
                        help='Explicit cumulative request ceiling for the shared ledger')
    args = parser.parse_args()
    if args.max_requests < 1:
        parser.error('max-requests must be positive')
    cap = Capture(ROOT, max_requests=args.max_requests)
    if args.cache_only:
        cap = CacheOnlyCapture(cap)
    function = {'ons-versions': ons_versions, 'nomis-overviews': nomis_overviews, 'nomis-times': nomis_times}[args.family]
    function(cap, start=args.start, limit=args.limit)


if __name__ == '__main__':
    main()
