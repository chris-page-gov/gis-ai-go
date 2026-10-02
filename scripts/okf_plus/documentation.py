#!/usr/bin/env python3
"""Bounded OS documentation capture and structural projection, never guide execution.

Full Markdown remains in Capture's ignored raw evidence. Public projections contain
bounded navigation and recognised short schema/code-list/lifecycle cells, not guide
paragraphs, examples, contacts, scripts or instructions. No discovered link is fetched.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

try:
    from .harvest import Capture, ROOT, MAX_BYTES, allowed, clean_text
    from .model import load_json
    from .ons_enrichment import CacheOnlyCapture
except ImportError:
    from harvest import Capture, ROOT, MAX_BYTES, allowed, clean_text
    from model import load_json
    from ons_enrichment import CacheOnlyCapture

PROJECTION = 'os-documentation-structure.v2'
MAX_PUBLIC_BYTES = 128 * 1024
MAX_HEADINGS, MAX_LINKS, MAX_TABLES, MAX_ROWS, MAX_COLUMNS = 96, 256, 64, 512, 32
MAX_CODE_LIST_ROWS = 1024
CODE_LIST_PATH = re.compile(r'^/osngd/code-lists/code-lists-overview/[a-z0-9-]+\.md$')
DOWNLOAD_GUIDES = frozenset({
    'https://docs.os.uk/os-downloads/resources/product-resources/product-refresh-dates.md',
    'https://docs.os.uk/os-downloads/resources/product-resources/end-of-life-product-notices.md',
})
COHORTS = {'ngd': ('osngd-documentation', 'osngd-documentation-pages', '/osngd/'),
           'download-guides': ('os-downloads-documentation', 'os-download-guide-pages', '/os-downloads/')}
ROLES = {
    'attribute': 'identifier', 'attributename': 'identifier', 'field': 'identifier', 'fieldname': 'identifier',
    'code': 'code', 'value': 'code', 'codevalue': 'code', 'name': 'identifier', 'product': 'product', 'productname': 'product',
    'datatype': 'data-type', 'type': 'data-type', 'geometrytype': 'data-type',
    'nullable': 'nullable', 'nullability': 'nullable', 'required': 'required', 'mandatory': 'required',
    'unit': 'unit', 'units': 'unit', 'length': 'length', 'maxlength': 'length', 'maximumlength': 'length',
    'precision': 'precision', 'scale': 'scale', 'schemaversion': 'schema-version',
    'dataschemaversion': 'schema-version', 'dataschemaversions': 'schema-version', 'version': 'schema-version',
    'codelist': 'code-list', 'codelistname': 'code-list', 'featuretype': 'feature-type', 'collection': 'collection',
    'updatefrequency': 'update-frequency', 'publicationmonth': 'publication-month',
    'publicationdate': 'publication-date', 'datacutdate': 'data-cut-date', 'extractiondate': 'extraction-date',
}
LIFECYCLE_ROLES = {'product', 'update-frequency', 'publication-month', 'publication-date', 'data-cut-date', 'extraction-date'}


def document_url(url, prefix=None):
    allowed(url)
    p = urlparse(url)
    if (p.netloc != 'docs.os.uk' or p.query or p.fragment or p.params or len(url) > 2048
            or not p.path.endswith('.md') or not p.path.startswith(prefix or ('/osngd/', '/os-downloads/'))):
        raise ValueError('Documentation capture requires a closed OS Markdown route')
    return url


def label(value, max_chars=160, max_words=20):
    value = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', value)
    value = clean_text(value).replace('\u200b', '').strip(' *_`')
    if (not value or len(value) > max_chars or len(value.split()) > max_words
            or '[contact omitted]' in value or re.search(r'(?i)\b(?:ignore (?:all )?(?:previous|prior)|agent instructions|system prompt)\b', value)
            or re.search(r'\$\(|`|#!', value)
            or re.match(r'(?i)^(?:curl|wget|python\d*|sudo|npm|pnpm|rm|rmdir|bash|sh|zsh|powershell|eval|exec)\s', value)):
        return None
    return value


def heading_role(text):
    text = text.casefold()
    for word, role in [('code list', 'code-list'), ('attribute', 'schema-field'), ('schema', 'schema'),
                       ('release', 'release'), ('refresh', 'update'), ('currency', 'update'),
                       ('end of life', 'withdrawal'), ('withdraw', 'withdrawal')]:
        if word in text:
            return role
    return 'section'


def reference(value, page):
    try:
        url = urljoin(page, html.unescape(value))
        p = urlparse(url)
        # Keep reviewed documentation references only, never media, arbitrary
        # external destinations, query services or source-provided credentials.
        if p.netloc != 'docs.os.uk' or p.query or p.params or len(url) > 2048:
            return None
        path = p.path
        if not path.startswith(('/osngd/', '/os-downloads/', '/os-apis/', '/more-than-maps/')):
            return None
        if not (path.endswith('.md') or not re.search(r'\.[A-Za-z0-9]{1,8}$', path)):
            return None
        allowed(url.split('#', 1)[0] if path.endswith('.md') else url.split('#', 1)[0] + '.md')
    except (ValueError, TypeError):
        return None
    kind = ('code-list-reference' if '/code-lists/' in path else
            'schema-reference' if '/data-structure/' in path else
            'withdrawal-reference' if 'end-of-life' in path else
            'release-reference' if any(s in path for s in ('release', 'change-log', 'refresh', 'currency')) else
            'documentation-reference')
    return {'url': url, 'kind': kind, 'followed': False}


def visible_structure(text):
    """Remove executable/example material and the appended GitBook agent section."""
    counts = {'fencedBlocksOmitted': 0, 'agentInstructionSectionOmitted': False, 'exampleOrContactSectionsOmitted': 0}
    marker = re.search(r'^#{1,6}\s+Agent Instructions\b', text, re.M | re.I)
    if marker:
        text = text[:marker.start()]; counts['agentInstructionSectionOmitted'] = True
    text = re.sub(r'<!--.*?(?:-->|$)', '', text, flags=re.S)
    text = re.sub(r'<(script|style|pre|code)\b[^>]*>.*?</\1\s*>', '', text, flags=re.I | re.S)
    lines, fence, omitted_section = [], None, None
    for line in text.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if match:
            if fence is None:
                fence = (match[1][0], len(match[1])); counts['fencedBlocksOmitted'] += 1
            elif match[1][0] == fence[0] and len(match[1]) >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            level = len(heading[1])
            if omitted_section is not None and level <= omitted_section:
                omitted_section = None
            if re.match(r'(?i)^(?:(?:worked |code )?examples?\b|contact(?: us| details)?\s*$)', heading[2].strip(' *_`')):
                omitted_section = level; counts['exampleOrContactSectionsOmitted'] += 1
        if omitted_section is None:
            lines.append(line)
    return '\n'.join(lines), counts


class StructureHTML(HTMLParser):
    """Read structural HTML only; entities are text and no resources are loaded."""
    def __init__(self, max_rows=MAX_ROWS):
        super().__init__(convert_charrefs=True)
        self.max_rows = max_rows
        self.headings, self.links, self.tables = [], [], []
        self.heading = self.table = self.cell = self.row = None
        self.table_depth = 0
        self.total_headings = self.total_links = self.total_tables = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.heading = [int(tag[1]), []]
        if tag == 'a' and 'href' in attributes:
            self.total_links += 1
            if len(self.links) < MAX_LINKS * 4:
                self.links.append(attributes['href'])
        if tag == 'table':
            self.table_depth += 1
            if self.table_depth == 1:
                self.total_tables += 1
                self.table = {'rows': [], 'rowCount': 0, 'format': 'html', 'complexSpans': False}
        if self.table_depth == 1:
            if tag == 'tr':
                self.row = []
            if tag in {'td', 'th'} and self.row is not None:
                self.cell = [tag, []]
                if any(attributes.get(k, '1') != '1' for k in ('rowspan', 'colspan')):
                    self.table['complexSpans'] = True
        if tag == 'br':
            self.handle_data(' ')

    def handle_data(self, data):
        if self.heading is not None:
            self.heading[1].append(data)
        if self.cell is not None and self.table_depth == 1:
            self.cell[1].append(data)

    def handle_endtag(self, tag):
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'} and self.heading is not None:
            self.total_headings += 1
            if len(self.headings) < MAX_HEADINGS:
                self.headings.append((self.heading[0], ''.join(self.heading[1])))
            self.heading = None
        if self.table_depth == 1:
            if tag in {'td', 'th'} and self.cell is not None and self.row is not None:
                if len(self.row) < MAX_COLUMNS + 1:
                    self.row.append((self.cell[0], ''.join(self.cell[1])))
                self.cell = None
            if tag == 'tr' and self.row is not None:
                self.table['rowCount'] += 1
                if len(self.table['rows']) < self.max_rows + 1:
                    self.table['rows'].append(self.row)
                self.row = None
        if tag == 'table' and self.table_depth:
            self.table_depth -= 1
            if self.table_depth == 0:
                if len(self.tables) < MAX_TABLES:
                    self.tables.append(self.table)
                self.table = self.cell = self.row = None


def markdown_tables(text, max_rows=MAX_ROWS):
    tables = []; lines = text.splitlines(); i = 0; total = 0
    split = lambda line: [x.strip().replace('\\|', '|') for x in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
    while i + 1 < len(lines):
        head, separator = split(lines[i]), split(lines[i + 1])
        if '|' not in lines[i] or not separator or not all(re.fullmatch(r':?-{3,}:?', x.strip()) for x in separator):
            i += 1; continue
        total += 1
        table = {'format': 'markdown', 'complexSpans': False, 'rows': [[('th', x) for x in head[:MAX_COLUMNS + 1]]], 'rowCount': 1}
        i += 2
        while i < len(lines) and '|' in lines[i] and lines[i].strip():
            table['rowCount'] += 1
            if len(table['rows']) < max_rows + 1:
                table['rows'].append([('td', x) for x in split(lines[i])[:MAX_COLUMNS + 1]])
            i += 1
        if len(tables) < MAX_TABLES:
            tables.append(table)
    return tables, total


def native_value_label(value):
    """Admit plain native labels, preserving their exact decoded cell text."""
    # Reviewed source maxima are 147 characters/bytes and 27 words. This narrow
    # bound accommodates those factual labels, not their narrative definitions.
    short = label(value, 160, 32)
    if short is None or len(value.encode('utf-8')) > 640 or short != value.strip():
        return None
    return value


def table_projection(table, lifecycle, code_list=False):
    rows = table['rows']; headers = rows[0] if rows and any(k == 'th' for k, _ in rows[0]) else []
    columns = [{'position': i, 'label': label(value, 80, 12),
                'role': ROLES.get(re.sub(r'[^a-z0-9]', '', clean_text(value).casefold()), 'unprojected')}
               for i, (_, value) in enumerate(headers[:MAX_COLUMNS])]
    for col in columns:
        if col['role'] in LIFECYCLE_ROLES and not lifecycle:
            col['role'] = 'unprojected'
    native_headers = [col['label'] for col in columns]
    label_table = code_list and native_headers in (
        ['Label', 'Definition'], ['Label', 'Description'],
        ['Label', 'Definition', None], ['Label', 'Description', None])
    if label_table:
        columns[0]['role'] = 'native-value-label'
    row_limit = MAX_CODE_LIST_ROWS if label_table else MAX_ROWS
    output = {'format': table['format'], 'columns': columns,
              'sourceRowCount': max(0, table['rowCount'] - bool(headers)),
              'hasExplicitHeader': bool(headers), 'complexSpans': table['complexSpans'],
              'sourceColumnCount': len(headers), 'rows': [], 'omittedCellCount': 0, 'raggedRowsOmitted': 0,
              'structureStatus': 'ambiguous-spans' if table['complexSpans'] else 'bounded-structural-projection'}
    if label_table:
        output['nativeLabelTable'] = {'encoding': 'os-documentation-native-label-table.v1',
            'columns': ['sourceRow', 'nativeText'], 'rows': []}
        output['nativeLabelScope'] = {
            'status': 'source-code-list-labels-not-api-enum-assertions',
            'sourceColumn': 'Label', 'rowLimit': row_limit,
            'sourceLabelRows': output['sourceRowCount'], 'retainedLabelRows': 0,
            'omittedLabelRows': output['sourceRowCount'],
            'identity': 'Source page, table ordinal and source row; duplicate labels are not merged.'}
    if table['complexSpans'] or not headers:
        return output
    for index, row in enumerate(rows[1:row_limit + 1]):
        if len(row) != len(headers):
            output['raggedRowsOmitted'] += 1; output['omittedCellCount'] += len(row); continue
        values = []
        for col, (_, value) in zip(columns, row):
            short = native_value_label(value) if col['role'] == 'native-value-label' else label(value, 120, 16)
            if col['role'] == 'unprojected' or short is None:
                output['omittedCellCount'] += 1; continue
            if col['role'] == 'native-value-label':
                output['nativeLabelTable']['rows'].append([index, short])
                continue
            values.append({'column': col['position'], 'role': col['role'], 'nativeText': short})
        output['omittedCellCount'] += max(0, len(row) - len(columns))
        if values:
            output['rows'].append({'sourceRow': index, 'cells': values})
    if label_table:
        retained = len(output['nativeLabelTable']['rows'])
        output['nativeLabelScope'].update(retainedLabelRows=retained,
            omittedLabelRows=output['sourceRowCount'] - retained)
    return output


def project(text, url, *, max_public_bytes=MAX_PUBLIC_BYTES):
    document_url(url)
    if not isinstance(text, str) or len(text.encode('utf-8')) > MAX_BYTES or not 2048 <= max_public_bytes <= MAX_PUBLIC_BYTES:
        raise ValueError('Documentation input or projection budget exceeded')
    visible, omitted = visible_structure(text)
    code_list = CODE_LIST_PATH.fullmatch(urlparse(url).path) is not None
    parse_rows = MAX_CODE_LIST_ROWS if code_list else MAX_ROWS
    parser = StructureHTML(parse_rows); parser.feed(visible); parser.close()
    md_headings = [(len(m[1]), m[2]) for m in re.finditer(r'^(#{1,6})\s+(.+)$', visible, re.M)]
    headings = []
    for level, value in (md_headings + parser.headings)[:MAX_HEADINGS]:
        short = label(value)
        if short:
            headings.append({'level': level, 'text': short, 'role': heading_role(short)})
    markdown_links = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', visible)
    raw_links = markdown_links + parser.links
    refs = {}; rejected = 0
    for value in raw_links:
        item = reference(value, url)
        if item is None:
            rejected += 1
        else:
            refs.setdefault(item['url'], item)
    markdown, table_count = markdown_tables(visible, parse_rows)
    tables = [table_projection(t, url in DOWNLOAD_GUIDES, code_list) for t in (markdown + parser.tables)[:MAX_TABLES]]
    result = {'projectionVersion': PROJECTION,
        'title': next((h['text'] for h in headings if h['level'] == 1), None),
        'canonicalUrl': url[:-3], 'headings': headings, 'references': list(refs.values())[:MAX_LINKS], 'tables': tables,
        'observed': {'headings': len(md_headings) + parser.total_headings,
                     'referenceLinks': len(markdown_links) + parser.total_links,
                     'referenceCandidatesReviewed': len(raw_links), 'distinctAcceptedReferences': len(refs),
                     'rejectedReferences': rejected, 'tables': table_count + parser.total_tables},
        'omitted': omitted, 'projectionTruncated': False,
        'normalisationRule': 'Visible structural labels only; Markdown/HTML markup, zero-width spaces and contact patterns removed. Native cell text is not a typed schema assertion.',
        'contentCompleteness': 'structure-only-not-full-guide-or-vocabulary-conformance'}
    def encoded_size():
        for table in result['tables']:
            if 'nativeLabelScope' in table:
                retained = len(table['nativeLabelTable']['rows'])
                table['nativeLabelScope'].update(retainedLabelRows=retained,
                    omittedLabelRows=table['sourceRowCount'] - retained)
        return len(json.dumps(result, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode())
    while encoded_size() > max_public_bytes:
        result['projectionTruncated'] = True
        if result['tables']:
            if result['tables'][-1]['rows']:
                rows = result['tables'][-1]['rows']
                del rows[-max(1, len(rows) // 4):]
            elif result['tables'][-1].get('nativeLabelTable', {}).get('rows'):
                rows = result['tables'][-1]['nativeLabelTable']['rows']
                del rows[-max(1, len(rows) // 4):]
            else:
                result['tables'].pop()
        elif result['references']:
            result['references'].pop()
        elif result['headings']:
            result['headings'].pop()
        else:
            raise ValueError('Projection metadata exceeds its byte ceiling')
    result['projectionTruncated'] |= (len(headings) < result['observed']['headings']
        or len(result['references']) < len(refs) or len(result['tables']) < result['observed']['tables']
        or len(raw_links) < result['observed']['referenceLinks']
        or any(t['sourceRowCount'] > t.get('nativeLabelScope', {}).get('rowLimit', MAX_ROWS)
               or t.get('nativeLabelScope', {}).get('omittedLabelRows', 0)
               or t['sourceColumnCount'] > MAX_COLUMNS for t in result['tables']))
    return result


def capture(cap, family='ngd', *, start=0, limit=None, checkpoint_every=10):
    if family not in COHORTS or type(start) is not int or start < 0 or (limit is not None and (type(limit) is not int or limit < 1)):
        raise ValueError('Invalid documentation cohort or batch')
    if type(checkpoint_every) is not int or not 1 <= checkpoint_every <= 100:
        raise ValueError('Checkpoint interval must be 1..100')
    source_name, output_name, prefix = COHORTS[family]
    source_path = cap.public / (source_name + '.json')
    if source_path.is_symlink():
        raise ValueError('Documentation index must not be a symbolic link')
    raw = source_path.read_bytes(); snapshot = load_json(raw.decode()); input_hash = hashlib.sha256(raw).hexdigest()
    cohort = snapshot['records']
    if not isinstance(cohort, list):
        raise ValueError('Documentation index requires a record list')
    for row in cohort:
        if not isinstance(row, dict) or row.get('id') != row.get('url'):
            raise ValueError('Documentation index identity mismatch')
        document_url(row['url'], prefix)
    if len({x['url'] for x in cohort}) != len(cohort):
        raise ValueError('Duplicate documentation index URLs')
    if family == 'download-guides':
        cohort = [r for r in cohort if r['url'] in DOWNLOAD_GUIDES]
        if {r['url'] for r in cohort} != DOWNLOAD_GUIDES:
            raise ValueError('Selected download guide is absent from the source index')
    records, receipts = {}, []
    output_path = cap.public / (output_name + '.json')
    if output_path.is_symlink():
        raise ValueError('Documentation checkpoint must not be a symbolic link')
    if output_path.exists():
        old = load_json(output_path.read_text())
        if (old.get('family') != output_name or old['coverage'].get('inputSha256') != input_hash
                or old['coverage'].get('projectionVersion') != PROJECTION):
            raise ValueError('Input or projection changed; preserve the previous snapshot before rebuilding')
        records = {r['id']: r for r in old['records']}; receipts = old['receipts']
        if len(records) != len(old['records']) or not set(records) <= {r['id'] for r in cohort}:
            raise ValueError('Checkpoint identity mismatch')

    def save(stop=None):
        ordered = [records[x['id']] for x in cohort if x['id'] in records]
        succeeded = sum(r['contentCaptured'] for r in ordered)
        unique = {(r['url'], r.get('retrievedAt'), r.get('sha256'), r.get('status')): r for r in receipts}
        cap.save(output_name, ordered, list(unique.values()), {
            'unit': 'indexed OS Markdown documentation page', 'inputFamily': source_name, 'inputSha256': input_hash,
            'projectionVersion': PROJECTION, 'reportedTotal': len(cohort), 'retrievedUnique': succeeded,
            'attemptedUnique': len(ordered), 'catalogueComplete': succeeded == len(cohort),
            'indexedReferences': len(cohort), 'contentCaptured': succeeded,
            'structuredUnique': sum(r.get('structureStatus') == 'projected' for r in ordered),
            'stopReason': stop, 'globalDocumentationComplete': False,
            'limitations': ['Page capture is distinct from navigation-index references and structural extraction.',
                'Full raw pages remain private; narrative definitions, examples, contacts and instructions are not republished.',
                'Bounded headings, reviewed-origin references and recognised table cells only; omissions and unsupported structures remain explicit.',
                'Captured code-list/schema text is not complete vocabulary coverage or API/feature conformance.',
                'No discovered link is followed, and no publication or provider operation is admitted.']})
    for number, source in enumerate(cohort[start:None if limit is None else start + limit], 1):
        url = source['url']
        try:
            text, receipt = cap.get(url, 'text')
        except RuntimeError:
            save('shared-capture-stopped'); raise
        receipts.append(receipt)
        row = {'id': url, 'url': url, 'title': label(source.get('title', '')) or 'OS documentation reference',
               'kind': 'documentation-page', 'callable': False, 'contentCaptured': isinstance(text, str),
               'metadataEvidence': {k: receipt[k] for k in ('url', 'retrievedAt', 'sha256', 'status') if k in receipt},
               'metadataStatus': 'captured' if isinstance(text, str) else 'request-failed'}
        if isinstance(text, str):
            row['sourceSha256'] = receipt.get('sha256')
            try:
                row['structure'] = project(text, url); row['structureStatus'] = 'projected'
            except (ValueError, TypeError, RecursionError):
                row['structureStatus'] = 'invalid-page-structure'
        records[url] = row
        if number % checkpoint_every == 0:
            save('batch-in-progress')
    save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('family', nargs='?', choices=COHORTS, default='ngd')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--checkpoint-every', type=int, default=10)
    parser.add_argument('--cache-only', action='store_true')
    parser.add_argument('--max-requests', type=int, required=True, help='Shared cumulative ledger ceiling, at most 4000')
    args = parser.parse_args()
    cap = Capture(ROOT, args.max_requests)
    if args.cache_only:
        cap = CacheOnlyCapture(cap)
    capture(cap, args.family, start=args.start, limit=args.limit, checkpoint_every=args.checkpoint_every)


if __name__ == '__main__':
    main()
