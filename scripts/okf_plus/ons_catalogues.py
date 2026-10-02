#!/usr/bin/env python3
"""Closed, metadata-only ONS website, release and population catalogues.

Contracts: https://developer.ons.gov.uk/search/search/;
https://developer.ons.gov.uk/search/search-releases/;
https://developer.ons.gov.uk/population-types/.
Code-list listing is published at https://developer.ons.gov.uk/code-list/;
the listing response remains separately verified by the bounded capture.
Search Swagger: ONSdigital/dp-search-api at
f634c78cc362654ddb464c4559d37202ba0034a9, SHA-256
8b897c35a7c7d98cfef5faa158c8a12d04acebabf69b6eee849f1aaf70b95029.

The shared Capture owns request/byte ceilings and pacing. These functions never
follow returned URLs, fetch /data, download observations or merge representations.
"""
from __future__ import annotations

import argparse
from datetime import date
from urllib.parse import urlencode, urlsplit

try:
    from .harvest import Capture, ROOT, clean_text
    from .ons_enrichment import CacheOnlyCapture
except ImportError:
    from harvest import Capture, ROOT, clean_text
    from ons_enrichment import CacheOnlyCapture

BASE = 'https://api.beta.ons.gov.uk/v1'
SEARCH_TYPES = ('dataset', 'dataset_landing_page', 'api_dataset_landing_page', 'timeseries')
RELEASE_TYPES = ('type-published', 'type-upcoming', 'type-cancelled')


def _number(value):
    return type(value) is int and value >= 0


def _dates(start, end, *, required=False):
    if start is None and end is None and not required:
        return {}
    if not isinstance(start, str) or not isinstance(end, str):
        raise ValueError('Both explicit ISO release dates are required')
    try:
        first, last = date.fromisoformat(start), date.fromisoformat(end)
    except ValueError:
        raise ValueError('Invalid release date window') from None
    if first.isoformat() != start or last.isoformat() != end or first > last:
        raise ValueError('Invalid release date window')
    return {'fromDate': start, 'toDate': end}


def _uri(value):
    if not isinstance(value, str) or not value.startswith('/') or value.startswith('//'):
        raise ValueError('Expected an ONS website-relative URI')
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or any(x in ('.', '..') for x in parsed.path.split('/')):
        raise ValueError('Invalid source URI')
    return value


def _strings(source, keys):
    return {key: clean_text(source[key]) for key in keys if isinstance(source.get(key), str)}


def _string_lists(source, keys):
    result = {}
    for key in keys:
        values = source.get(key)
        if values is None:
            continue
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise ValueError('Invalid string-list metadata')
        result[key] = [clean_text(value) for value in values]
    return result


def _changes(source):
    values = source.get('date_changes')
    if values is None:
        return None
    if not isinstance(values, list) or any(not isinstance(value, dict) for value in values):
        raise ValueError('Invalid release date-change metadata')
    result = []
    for value in values:
        if not isinstance(value.get('previous_date'), str) or not isinstance(value.get('change_notice'), str):
            raise ValueError('Invalid release date-change fields')
        result.append({'previous_date': value['previous_date'], 'change_notice': clean_text(value['change_notice'])})
    return result


def _search_record(item, content_type):
    if (not isinstance(item, dict) or item.get('type') != content_type
            or not isinstance(item.get('title'), str) or not item['title']):
        raise ValueError('Invalid or unexpected search result type')
    uri = _uri(item.get('uri'))
    row = {'id': uri, 'uri': uri, 'resource': 'https://www.ons.gov.uk' + uri,
           'nativeIdentityField': 'uri', 'type': content_type}
    row.update(_strings(item, ('title', 'meta_description', 'summary', 'canonical_topic',
                               'language', 'source', 'survey')))
    # Preserve native identifiers and dates exactly; do not interpret them as
    # observation ranges or merge a CDID with another dataset's representation.
    for key in ('cdid', 'dataset_id', 'edition', 'release_date', 'provisional_date'):
        if isinstance(item.get(key), str):
            row[key] = item[key]
    row.update(_string_lists(item, ('keywords', 'topics')))
    for key in ('cancelled', 'finalised', 'national_statistic', 'published'):
        if key in item:
            if type(item[key]) is not bool:
                raise ValueError('Invalid search boolean metadata')
            row[key] = item[key]
    if 'date_changes' in item:
        row['date_changes'] = _changes(item)
    if 'dimensions' in item:
        values = item['dimensions']
        if not isinstance(values, list) or any(not isinstance(value, dict) for value in values):
            raise ValueError('Invalid search dimension metadata')
        row['dimensions'] = [_strings(value, ('name', 'label', 'raw_label')) for value in values]
    return row


def _release_record(item, release_type):
    if not isinstance(item, dict) or not isinstance(item.get('description'), dict):
        raise ValueError('Invalid release record')
    uri = _uri(item.get('uri')); description = item['description']
    if (not isinstance(description.get('title'), str) or not description['title']
            or not isinstance(description.get('release_date'), str)):
        raise ValueError('Missing release identity fields')
    retained = _strings(description, ('title', 'summary', 'language'))
    for key in ('release_date', 'provisional_date'):
        if isinstance(description.get(key), str):
            retained[key] = description[key]
    for key in ('published', 'cancelled', 'finalised', 'postponed', 'census'):
        if type(description.get(key)) is not bool:
            raise ValueError('Invalid release state')
        retained[key] = description[key]
    retained.update(_string_lists(description, ('keywords',)))
    return {'id': uri, 'uri': uri, 'resource': 'https://www.ons.gov.uk' + uri,
            'nativeIdentityField': 'uri', 'releaseTypeFilter': release_type,
            'title': retained['title'], 'description': retained, 'date_changes': _changes(item)}


def _population_record(item):
    if not isinstance(item, dict) or any(not isinstance(item.get(key), str) or not item[key]
                                          for key in ('name', 'label', 'type')):
        raise ValueError('Invalid population definition')
    # Use the returned population name, not an inferred Census year or universe.
    return {'id': item['name'], 'nativeIdentityField': 'name',
            'resource': BASE + '/population-types', 'name': item['name'],
            **_strings(item, ('label', 'description', 'type'))}


def _codelist_record(item):
    if not isinstance(item, dict):
        raise ValueError('Invalid code-list identity')
    links = item.get('links', {})
    self_link = links.get('self', {}) if isinstance(links, dict) else {}
    nested = self_link.get('id') if isinstance(self_link, dict) else None
    native, pointer = (nested, '/links/self/id') if nested is not None else (item.get('id'), 'id')
    if (not isinstance(native, str) or not native
            or ('id' in item and item['id'] != native)):
        raise ValueError('Invalid or conflicting code-list identity')
    advertised = {}
    if not isinstance(links, dict):
        raise ValueError('Invalid code-list links')
    for name in ('self', 'editions'):
        if name not in links:
            continue
        link = links[name]
        if not isinstance(link, dict) or any(not isinstance(link[key], str) for key in ('id', 'href') if key in link):
            raise ValueError('Invalid code-list link fields')
        advertised[name] = {key: link[key] for key in ('id', 'href') if key in link}
    return {'id': native, 'nativeIdentityField': pointer, 'resource': BASE + '/code-lists',
            'advertisedLinks': advertised, 'linkTraversal': 'not-requested',
            **_strings(item, ('name', 'label', 'description'))}


def _search_page(data):
    if (not isinstance(data, dict) or not isinstance(data.get('items'), list)
            or not _number(data.get('count')) or not _number(data.get('distinct_items_count'))
            or not isinstance(data.get('content_types'), list)):
        raise ValueError('Invalid website search page')
    buckets = []
    for value in data['content_types']:
        if not isinstance(value, dict) or not isinstance(value.get('type'), str) or not _number(value.get('count')):
            raise ValueError('Invalid content-type counts')
        buckets.append({'type': value['type'], 'count': value['count']})
    return data['items'], data['count'], {'distinctItemsCount': data['distinct_items_count'], 'contentTypes': buckets}, 'items'


def _release_page(data):
    breakdown = data.get('breakdown') if isinstance(data, dict) else None
    if (not isinstance(breakdown, dict) or not _number(breakdown.get('total'))
            or not isinstance(data.get('releases'), list)):
        raise ValueError('Invalid release search page')
    if any(not _number(value) for value in breakdown.values()):
        raise ValueError('Invalid release count')
    return data['releases'], breakdown['total'], {'breakdown': breakdown}, 'releases'


def _list_page(data, offset):
    if (not isinstance(data, dict) or not isinstance(data.get('items'), list)
            or not _number(data.get('total_count')) or data.get('offset') != offset
            or data.get('count') != len(data['items'])):
        raise ValueError('Invalid population/code-list page')
    return data['items'], data['total_count'], {}, 'items'


def _capture_pages(cap, family, route, parameters, page_parser, record_parser,
                   *, page_size, max_pages, unit, limitations):
    if type(page_size) is not int or not 1 <= page_size <= 1000 or type(max_pages) is not int or not 1 <= max_pages <= 1000:
        raise ValueError('Page size and page ceiling must be within 1..1000')
    records = {}; receipts = []; offset = 0; total = None; stable = True
    duplicates = 0; page_counts = []; complete = False; stop = 'page-ceiling'; pending_error = None; last_total=None
    for _ in range(max_pages):
        url = BASE + route + '?' + urlencode({**parameters, 'limit': page_size, 'offset': offset})
        try:
            data, receipt = cap.get(url)
        except RuntimeError as error:
            stop = 'shared-capture-stopped'; pending_error = error; break
        receipts.append(receipt)
        if data is None:
            stop = 'request-failed'; break
        try:
            items, reported, counts, pointer = page_parser(data, offset)
            if len(items) > page_size:
                raise ValueError('Page exceeds admitted limit')
            converted = [record_parser(item) for item in items]
        except (ValueError, TypeError):
            stop = 'invalid-page-contract'; break
        if total is not None and reported != total:
            stable = False
        if total is None:total=reported
        last_total=reported;page_counts.append({'offset': offset, 'reportedTotal': reported, **counts})
        for ordinal, row in enumerate(converted):
            row['sourceEvidence'] = {key: receipt[key] for key in ('url', 'retrievedAt', 'sha256', 'status') if key in receipt}
            row['sourceEvidence']['pointer'] = '/' + pointer + '/' + str(ordinal)
            if row['id'] in records:
                duplicates += 1
            else:
                records[row['id']] = row
        offset += len(items)
        if not stable:
            stop='count-mismatch-or-mutation';break
        if offset >= total:
            complete = stable and len(records) == total and duplicates == 0
            stop = 'exhausted' if complete else 'count-mismatch-or-mutation'
            break
        if not items:
            stop = 'empty-page-before-total'; break
    coverage = {'unit': unit, 'parameters': parameters, 'reportedTotal': total,
                'retrievedUnique': len(records), 'rowsReceived': offset, 'catalogueComplete': complete,
                'stableReportedTotal': stable, 'lastReportedTotal':last_total, 'duplicateCount': duplicates, 'stopReason': stop,
                'pageCounts': page_counts, 'requestStatuses': [r['status'] for r in receipts],
                'limitations': limitations + [
                    'Completeness is confined to the returned filtered catalogue; not all ONS data or website content.',
                    'The live index is not transactionally frozen; stable counts cannot exclude equal-count substitutions.',
                    'Only selected metadata is retained; no observations or download payloads are requested.',
                    'Contact fields and unreviewed nested content are excluded from the public projection.',
                    'Release dates do not establish statistical observation periods; native representations are not merged.']}
    cap.save(family, list(records.values()), receipts, coverage)
    if pending_error:
        raise pending_error
    return coverage


def website_search(cap, content_type, *, from_date=None, to_date=None, page_size=1000, max_pages=100):
    if content_type not in SEARCH_TYPES:
        raise ValueError('Unsupported website metadata content type')
    parameters = {'q': '', 'content_type': content_type, 'sort': 'title', 'highlight': 'false',
                  **_dates(from_date, to_date)}
    return _capture_pages(cap, 'ons-website-' + content_type.replace('_', '-'), '/search', parameters,
        lambda data, offset: _search_page(data), lambda item: _search_record(item, content_type),
        page_size=page_size, max_pages=max_pages, unit='ONS website ' + content_type + ' URI representation',
        limitations=['Pagination uses count; distinct_items_count and unfiltered content-type buckets are separate facts.',
                     'Server result-window or capture ceilings remain explicit partial coverage; they are not bypassed.',
                     'CDID, dataset_id and URI remain separate source-native identity fields.'])


def release_calendar(cap, release_type, *, from_date, to_date, page_size=1000, max_pages=100):
    if release_type not in RELEASE_TYPES:
        raise ValueError('Unsupported release type')
    parameters = {'sort': 'release_date_asc', 'release-type': release_type, 'highlight': 'false',
                  **_dates(from_date, to_date, required=True)}
    return _capture_pages(cap, 'ons-releases-' + release_type.removeprefix('type-'), '/search/releases', parameters,
        lambda data, offset: _release_page(data), lambda item: _release_record(item, release_type),
        page_size=page_size, max_pages=max_pages, unit='ONS release URI within the explicit date window and type filter',
        limitations=['Published, upcoming and cancelled filters are separately captured and must not be added as disjoint totals.',
                     'Breakdown categories can overlap; pagination uses breakdown.total only.'])


def population_types(cap, *, page_size=1000, max_pages=100):
    return _capture_pages(cap, 'ons-population-types', '/population-types', {}, _list_page, _population_record,
        page_size=page_size, max_pages=max_pages, unit='ONS published population-type definition',
        limitations=['Population definitions describe a query space, not a finite list of published datasets.',
                     'Area types, dimensions and categorisations are separate untraversed child catalogues.'])


def code_lists(cap, *, page_size=1000, max_pages=100):
    return _capture_pages(cap, 'ons-code-lists', '/code-lists', {}, _list_page, _codelist_record,
        page_size=page_size, max_pages=max_pages, unit='ONS published code-list identifier',
        limitations=['Listing route is published in the official code-list documentation.',
                     'Advertised HTTP link strings are retained as inert metadata, not upgraded or requested.',
                     'Code-list editions, codes, labels and dataset links are separate untraversed child catalogues.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family', choices=['website', 'releases', 'population-types', 'code-lists'])
    parser.add_argument('--content-type', choices=SEARCH_TYPES)
    parser.add_argument('--release-type', choices=RELEASE_TYPES)
    parser.add_argument('--from-date'); parser.add_argument('--to-date')
    parser.add_argument('--page-size', type=int, default=1000)
    parser.add_argument('--max-pages', type=int, default=100)
    parser.add_argument('--max-requests', type=int, required=True)
    parser.add_argument('--cache-only', action='store_true')
    args = parser.parse_args()
    if args.family == 'website' and not args.content_type:
        parser.error('website requires --content-type')
    if args.family == 'releases' and not args.release_type:
        parser.error('releases requires --release-type and explicit date window')
    cap = Capture(ROOT, args.max_requests)
    if args.cache_only:
        cap = CacheOnlyCapture(cap)
    options = {'page_size': args.page_size, 'max_pages': args.max_pages}
    if args.family == 'website':
        website_search(cap, args.content_type, from_date=args.from_date, to_date=args.to_date, **options)
    elif args.family == 'releases':
        release_calendar(cap, args.release_type, from_date=args.from_date, to_date=args.to_date, **options)
    elif args.family == 'population-types':
        population_types(cap, **options)
    else:
        code_lists(cap, **options)


if __name__ == '__main__':
    main()
