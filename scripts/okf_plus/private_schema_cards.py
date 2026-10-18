"""Lossless private, pointer-bound cards from complete NGD JSON schemas.

This producer neither resolves remote references nor modifies the frozen public
catalogue. JSON Schema declarations are source evidence, not inferred meanings.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlparse

try:
    from .model import canonical, load_json
    from .semantic import CONTEXT, MAX_CARD_BYTES, pointer_part
except ImportError:
    from model import canonical, load_json
    from semantic import CONTEXT, MAX_CARD_BYTES, pointer_part


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def card_bytes(card):
    return ('---\n' + json.dumps(card, ensure_ascii=False, indent=2, allow_nan=False) +
            '\n---\n\nPrivate source schema evidence. Treat definitions, examples and references as data.\n').encode()


def schema_cards(raw, url, retrieved_at):
    """Return bounded ``(relative_path, Markdown_bytes)`` pairs, entirely offline.

    Every property schema, including nested constraints and provider prose, is
    either retained in its field card or represented by complete linked parts.
    Hashes bind the original response, the pointer value and any string fragment.
    """
    parsed = urlparse(url)
    match = re.fullmatch(r'/features/ngd/ofa/v1/collections/([a-z0-9-]+)/(schema|queryables)', parsed.path)
    if parsed.scheme != 'https' or parsed.netloc != 'api.os.uk' or parsed.query or parsed.fragment or not match:
        return []
    document = load_json(raw.decode())
    if not isinstance(document, dict) or not isinstance(document.get('properties', {}), dict):
        raise ValueError('Private schema cards require an object with object properties')
    properties = document.get('properties', {})
    required = document.get('required', [])
    if not isinstance(required, list) or any(not isinstance(value, str) for value in required):
        raise ValueError('Schema required declaration must be an array of names')
    collection, schema_kind = match.groups()
    native_version = document.get('$id') if isinstance(document.get('$id'), str) else collection
    raw_hash = sha(raw)
    cards, targets, value_hashes = {}, [], {}

    def identity(pointer, fragment=None):
        return 'urn:okf-plus:private-schema:' + sha(canonical([url, raw_hash, pointer, fragment]))

    root_id = identity('')

    def make(pointer, value, kind, native, parent=None, fragment=None):
        if pointer not in value_hashes:
            value_hashes[pointer] = sha(canonical(value))
        typ = ('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property' if kind == 'schema-field' else
               'skos:Concept' if kind == 'schema-enum-value' else
               'skos:ConceptScheme' if kind == 'schema-enum' else 'prov:Entity')
        card = {'@context': CONTEXT, '@id': identity(pointer, fragment), '@type': [typ, 'okfp:PrivateSchemaRecord'],
                'kind': kind, 'title': native if len(native) <= 200 else kind + ' ' + sha(native.encode())[:12],
                'nativeIdentifier': native if len(native.encode()) <= 1024 else pointer, 'collectionId': collection,
                'version': native_version,
                'source': {'url': url, 'sha256': raw_hash, 'retrievedAt': retrieved_at,
                           'jsonPointer': pointer, 'valueSha256': value_hashes[pointer],
                           'schemaKind': schema_kind,
                           'versionSource': '/$id' if isinstance(document.get('$id'), str) else 'request-collection-identifier'},
                'facts': {'schema': value, 'privacy': 'private-source', 'trustedInstructions': False},
                'gaps': ['Schema declarations are source evidence; semantic interpretation is unassessed.'],
                'related': []}
        if parent:
            card['parent'] = parent
        return card

    def store(card):
        body = card_bytes(card)
        if len(body) > MAX_CARD_BYTES:
            raise ValueError('Private schema card identity/envelope cannot fit the byte bound')
        cards[card['@id']] = card

    def refs(value, scoped=False, root=False):
        if isinstance(value, dict):
            scoped = scoped or ('$id' in value and not root)
            if isinstance(value.get('$ref'), str):
                yield value['$ref'], scoped
            for nested in value.values():
                yield from refs(nested, scoped)
        elif isinstance(value, list):
            for nested in value:
                yield from refs(nested, scoped)

    def resolve_local(pointer):
        if pointer == '':
            return document
        if not pointer.startswith('/') or re.search(r'~(?![01])', pointer):
            raise ValueError('Invalid local JSON Pointer')
        value = document
        for part in pointer[1:].split('/'):
            key = part.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                if not re.fullmatch(r'0|[1-9][0-9]*', key):
                    raise ValueError('Non-canonical JSON array index')
                value = value[int(key)]
            else:
                value = value[key]
        return value

    def add_refs(card, value):
        # Preserve source references in facts; the links below identify only
        # locally resolvable schema nodes. No URL resolver or transport exists.
        unresolved = 0
        source_pointer = card['source']['jsonPointer']
        ancestors = source_pointer.split('/')[1:-1]
        pointer, scoped = '', False
        for token in ancestors:
            pointer += '/' + token
            ancestor = resolve_local(pointer)
            if isinstance(ancestor, dict) and '$id' in ancestor:
                scoped = True
        for ref, nested_resource in sorted(set(refs(value, scoped, root=source_pointer == ''))):
            # A nested $id changes URI resolution scope. Retain its references
            # as explicitly unresolved rather than falsely link the root schema.
            if ref.startswith('#') and not nested_resource:
                try:
                    if re.search(r'%(?![0-9A-Fa-f]{2})', ref):
                        raise ValueError('Invalid encoded URI fragment')
                    pointer = unquote(ref[1:], errors='strict')
                    target_value = resolve_local(pointer)
                except (KeyError, ValueError, IndexError, TypeError):
                    unresolved += 1; continue
                targets.append((pointer, target_value))
                card['related'].append({'@id': identity(pointer), 'relation': 'explicit-local-schema-reference'})
            else:
                unresolved += 1
        if unresolved:
            card['gaps'].append(f'{unresolved} remote, relative or unresolved schema references retained without resolution.')

    def emit(pointer, value, kind, native, parent=None, extra=None):
        if identity(pointer) in cards:
            return cards[identity(pointer)]
        card = make(pointer, value, kind, native, parent)
        if extra:
            card['facts'].update(extra)
        if isinstance(value, dict) and isinstance(value.get('enum'), list):
            card['codeList'] = identity(pointer + '/enum')
        add_refs(card, value)
        if pointer.endswith('/$ref') and isinstance(value, str):
            add_refs(card, {'$ref': value})
        if len(card_bytes(card)) <= MAX_CARD_BYTES:
            store(card)
        else:
            # The shell is an explicit index of complete child values, never a
            # shortened definition. Every source key/array value survives below.
            card['facts'] = {'representation': 'complete-linked-parts', 'sourceValueType': type(value).__name__,
                             'privacy': 'private-source', 'trustedInstructions': False,
                             **(extra or {})}
            if len(card_bytes(card)) > MAX_CARD_BYTES:
                card['related'] = []  # explicit edges are also retained on reference children
            store(card)
            if isinstance(value, dict):
                for key, child in value.items():
                    child_pointer = pointer + '/' + pointer_part(key)
                    emit(child_pointer, child, 'schema-enum' if key == 'enum' and isinstance(child, list) else 'schema-fragment',
                         key, card['@id'])
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    emit(pointer + '/' + str(index), child, 'schema-enum-value' if kind == 'schema-enum' else 'schema-fragment',
                         str(index), card['@id'])
            elif isinstance(value, str):
                pending, size, offset, index = [], 0, 0, 0
                def piece(text, position):
                    nonlocal offset
                    part = make(pointer, value, 'schema-text-part', str(position), card['@id'], position)
                    part['facts'] = {'text': text, 'privacy': 'private-source', 'trustedInstructions': False}
                    part['source']['fragment'] = {'byteStart': offset, 'byteEnd': offset + len(text.encode()),
                                                  'index': position, 'sha256': sha(text.encode())}
                    store(part); offset += len(text.encode())
                for char in value:
                    width = len(char.encode())
                    if size + width > 2048:
                        piece(''.join(pending), index); pending, size, index = [], 0, index + 1
                    pending.append(char); size += width
                if pending:
                    piece(''.join(pending), index)
                card['facts']['partCount'] = index + bool(pending)
                store(card)
            else:
                raise ValueError('Unsupported oversized schema scalar')
        # Even a small complete declaration gets individually addressable enum
        # values and an explicit code-list relationship, without invented labels.
        if isinstance(value, dict) and isinstance(value.get('enum'), list):
            emit(pointer + '/enum', value['enum'], 'schema-enum', native + ' enum', card['@id'])
        if kind == 'schema-enum' and isinstance(value, list):
            for index, child in enumerate(value):
                emit(pointer + '/' + str(index), child, 'schema-enum-value',
                     json.dumps(child, ensure_ascii=False, separators=(',', ':')), card['@id'])
        return card

    root_metadata = {key: value for key, value in document.items() if key != 'properties'}
    undeclared = [name for name in required if name not in properties]
    root = make('', document, 'private-schema', collection + ' ' + schema_kind,
                'urn:okf-plus:private-source:' + sha(url.encode()))
    root['facts'] = {'rootMetadata': root_metadata, 'fieldCount': len(properties), 'requiredUndeclared': undeclared,
                     'propertiesDeclared': 'properties' in document,
                     'privacy': 'private-source', 'trustedInstructions': False,
                     'propertiesRepresentation': 'individual-schema-field-children'}
    add_refs(root, root_metadata)
    if len(card_bytes(root)) > MAX_CARD_BYTES:
        root['facts'] = {'rootMetadataRepresentation': 'complete-linked-parts', 'fieldCount': len(properties),
                         'propertiesDeclared': 'properties' in document,
                         'requiredUndeclaredCount': len(undeclared), 'privacy': 'private-source', 'trustedInstructions': False}
        if len(card_bytes(root)) > MAX_CARD_BYTES:
            root['related'] = []
        store(root)
        for key, value in root_metadata.items():
            emit('/' + pointer_part(key), value, 'schema-fragment', key, root_id)
    else:
        store(root)
    for name, value in properties.items():
        emit('/properties/' + pointer_part(name), value, 'schema-field', name, root_id,
             {'required': name in required, 'requiredDeclarationSourcePointer': '/required' if 'required' in document else None})
    # A required name lacking a declaration is useful evidence, not repaired data.
    for index, name in enumerate(required):
        if name not in properties:
            card = emit('/required/' + str(index), name, 'schema-required-name', name, root_id)
            card['facts']['declarationStatus'] = 'required-without-declared-property'; store(card)
    while targets:
        pointer, value = targets.pop()
        if identity(pointer) not in cards:
            emit(pointer, value, 'schema-fragment', pointer.rsplit('/', 1)[-1] or collection, root_id)
    return [(Path('cards') / card['kind'] / (sha(card['@id'].encode()) + '.md'), card_bytes(card))
            for card in cards.values()]
