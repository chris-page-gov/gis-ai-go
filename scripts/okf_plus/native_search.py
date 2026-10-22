"""Validate exact source-native lexical forms in already reviewed JSON inputs.

Structural checks do not independently establish source meaning or authority.
Input/source review and hash admission remain the caller's responsibility.
"""
import hashlib
import json
import re

FORM_KEYS = {'text', 'kind', 'authority', 'sourceId', 'sourceLocator', 'nativePointer', 'language'}
CODE_ROLES = {'unknown', 'source-code-retained', 'explicit-empty-code',
              'unresolved-native-value', 'no-separate-code-assertion'}


def require(condition, message):
    if not condition:
        raise ValueError('Native search: ' + message)


def resolve_native(entry, pointer):
    require(type(pointer) is str and pointer.startswith('/native/') and len(pointer) <= 512,
            'invalid pointer')
    parts = pointer.split('/')[1:]
    require(len(parts) <= 16 and not re.search(r'~(?![01])', pointer), 'invalid pointer')
    value = entry
    for token in parts:
        key = token.replace('~1', '/').replace('~0', '~')
        if type(value) is dict:
            require(key in value, 'missing pointer')
            value = value[key]
        elif type(value) is list:
            require(bool(re.fullmatch(r'0|[1-9][0-9]*', key)), 'invalid array pointer')
            require(int(key) < len(value), 'missing array pointer')
            value = value[int(key)]
        else:
            raise ValueError('Native search: non-container pointer')
    return value


def validate_native_search(entry, sources):
    require(type(entry) is dict and type(sources) is dict, 'entry context')
    forms = entry.get('nativeSearchForms', [])
    require(type(forms) is list and len(forms) <= 8, 'form count')
    try:
        form_bytes = json.dumps(forms, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')
        # Native keys and values must survive the same UTF-8 export boundary.
        json.dumps(entry['native'], ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')
    except UnicodeError as error:
        raise ValueError('Native search: unpaired surrogate') from error
    require(len(form_bytes) <= 8192, 'form byte bound')
    seen = set()
    for form in forms:
        require(type(form) is dict and set(form) == FORM_KEYS, 'closed form')
        require(type(form['text']) is str and 0 < len(form['text']) <= 1000, 'text bound')
        require(form['kind'] == 'source-native-value' and form['authority'] == 'source-stated', 'form role')
        require(form['language'] is None, 'language not admitted')
        require(form['sourceId'] == entry['sourceId'] and form['sourceId'] in sources, 'source mismatch')
        require(form['sourceLocator'] == entry['sourceLocator'], 'locator mismatch')
        pointer = form['nativePointer']
        value = resolve_native(entry, pointer)
        require(type(value) is str and value == form['text'], 'native string mismatch')
        require(pointer not in seen, 'duplicate pointer')
        seen.add(pointer)
    role = entry.get('codeRole', 'unknown')
    require(type(role) is str and role in CODE_ROLES, 'unknown code role')
    code = entry['code']
    require(code is None or type(code) is str, 'code type')
    if role == 'source-code-retained':
        require(type(code) is str and bool(code.strip()), 'code role conflict')
    elif role == 'explicit-empty-code':
        require(code == '', 'code role conflict')
    elif role != 'unknown':
        require(code is None, 'code role conflict')
    return forms


def qualified_form(record_id, form, source_url):
    pointer = '/details/entry' + form['nativePointer']
    return {'@id': record_id + '/native-search/' + hashlib.sha256(pointer.encode()).hexdigest(),
            '@type': 'okfp:LexicalForm', 'rdf:value': {'@value': form['text']},
            'okfp:formKind': 'source-native-value', 'okfp:authority': 'source-stated',
            'prov:wasDerivedFrom': [{'@id': source_url}], 'okfp:sourcePointer': pointer}


def validate_qualified_form(row, form):
    """Bind the complete qualified form back to its declared native entry context."""
    try:
        details = row['details']
        entry = details['entry']
        native_sources = details['scheme']['sources']
        sources = {s['id']: s for s in native_sources}
        require(len(sources) == len(native_sources), 'duplicate source context')
        forms = validate_native_search(entry, sources)
        matches = [f for f in forms if '/details/entry' + f['nativePointer'] == form['okfp:sourcePointer']]
        require(len(matches) == 1, 'unresolved qualified pointer')
        expected = qualified_form(row['@id'], matches[0], sources[entry['sourceId']]['url'])
        require(form == expected, 'qualified form differs from native declaration')
        return form['okfp:sourcePointer']
    except (KeyError, TypeError) as error:
        raise ValueError('Native search: incomplete qualified context') from error
