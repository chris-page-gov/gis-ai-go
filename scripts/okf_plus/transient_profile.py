"""Offline bounded feature profiling; feature contents are not retained.

Supports UTF-8 NDJSON (streaming) and bounded GeoJSON FeatureCollection only.
Input deletion is opt-in, restricted to ignored artefacts, after complete success.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import math
import os
import shutil
import tempfile
from pathlib import Path

try:
    from .model import canonical, load_json, safe_reference, PREFIXES
    from .passages import no_symlinks
except ImportError:
    from model import canonical, load_json, safe_reference, PREFIXES
    from passages import no_symlinks

ROOT = Path(__file__).resolve().parents[2]


def checked_metadata(value):
    """Recipes/schema are metadata, never credentials or executable instructions."""
    if isinstance(value, dict):
        for key, item in value.items():
            if ''.join(c for c in key.lower() if c.isalnum()) in {
                'key', 'apikey', 'token', 'authorization', 'password', 'secret', 'clientsecret'}:
                raise ValueError('Credential metadata is forbidden')
            checked_metadata(item)
    elif isinstance(value, list):
        for item in value: checked_metadata(item)
    elif isinstance(value, str) and '://' in value:
        safe_reference(value)
    return value


def kind(value):
    if value is None: return 'null'
    if isinstance(value, bool): return 'boolean'
    if isinstance(value, int): return 'integer'
    if isinstance(value, float): return 'number'
    if isinstance(value, str): return 'string'
    if isinstance(value, list): return 'array'
    if isinstance(value, dict): return 'object'
    raise ValueError('Unsupported JSON value')


def depth_check(value, depth, limit):
    if depth > limit: raise ValueError('Depth budget exceeded')
    if isinstance(value, float) and not math.isfinite(value): raise ValueError('Non-finite number')
    if isinstance(value, (dict, list)):
        for child in (value.values() if isinstance(value, dict) else value):
            depth_check(child, depth + 1, limit)


def schema_fields(schema, path=()):
    result = {}
    if not isinstance(schema, dict): return result
    for name, definition in schema.get('properties', {}).items():
        key = path + (name,)
        result[key] = definition
        result.update(schema_fields(definition, key))
    items = schema.get('items')
    if isinstance(items, dict):
        result[path + ('*',)] = items
        result.update(schema_fields(items, path + ('*',)))
    return result


def sensitive_path(path):
    return path[0] == 'geometry' or any(name.lower().endswith(('_id', '_ids', 'identifier', 'identifiers')) or name.lower() in {
        'id','ids','toid','osid','uprn','usrn','latitude','longitude','lat','lon','lng',
        'easting','northing','coordinates','x','y','z'} for name in path)


def profile(source, output, *, format='ndjson', schema=None, recipe=None,
            controlled_fields=(), max_bytes=32*1024*1024, max_records=100000,
            max_depth=32, cardinality_cap=10000, discard_after_success=False):
    source, output = no_symlinks(source), no_symlinks(output)
    for budget in (max_bytes, max_records, max_depth, cardinality_cap):
        if type(budget) is not int or budget < 1: raise ValueError('Budgets must be positive integers')
    if format not in {'ndjson', 'geojson'}: raise ValueError('Unsupported format')
    if not source.is_file(): raise ValueError('Input must be a regular file')
    if output.exists() or source == output: raise ValueError('Output already exists or replaces input')
    private = ROOT / 'artifacts'
    if not output.is_relative_to(private): raise ValueError('Profile must remain in ignored artifacts/')
    if discard_after_success and not source.is_relative_to(private):
        raise ValueError('Deletion is restricted to ignored artifacts/')
    schema = checked_metadata(schema or {})
    recipe = checked_metadata(recipe or {})
    definitions = schema_fields(schema)
    controlled = {tuple(x.split('/')) for x in controlled_fields}
    fields, unique, observed = {}, {}, {}
    containers, array_items, record_presence = {}, {}, {}
    geometry_summary = {'types': {}, 'coordinateDimensions': {}}
    count = total_bytes = 0
    digest = hashlib.sha256()
    initial = source.stat()

    def consume(record):
        nonlocal count
        if count >= max_records: raise ValueError('Record budget exceeded')
        depth_check(record, 0, max_depth)
        if not isinstance(record, dict) or record.get('type') != 'Feature':
            raise ValueError('Expected GeoJSON Feature')
        count += 1
        seen = set()
        geometry = record.get('geometry')
        if isinstance(geometry, dict):
            geometry_type = geometry.get('type')
            if geometry_type in {'Point','MultiPoint','LineString','MultiLineString','Polygon','MultiPolygon','GeometryCollection'}:
                counts = geometry_summary['types']
                counts[geometry_type] = counts.get(geometry_type, 0) + 1
        def walk_object(obj, parent=()):
            containers[parent] = containers.get(parent, 0) + 1
            for name, value in obj.items():
                if name == '*': raise ValueError('Literal wildcard property is ambiguous')
                observe(value, parent + (name,))
        def observe(value, path):
            sensitive = sensitive_path(path)
            row = fields.setdefault(path, {'present': 0, 'null': 0, 'types': {},
                'maximumStringLength': 0, 'numericMin': None, 'numericMax': None,
                'arrayLengthMin': None, 'arrayLengthMax': None})
            row['present'] += 1
            seen.add(path)
            typ = kind(value)
            row['types'][typ] = row['types'].get(typ, 0) + 1
            row['null'] += value is None
            scalar = not isinstance(value, (dict, list))
            if isinstance(value, str): row['maximumStringLength'] = max(row['maximumStringLength'], len(value))
            if isinstance(value, (int,float)) and not isinstance(value,bool) and not sensitive:
                row['numericMin'] = value if row['numericMin'] is None else min(row['numericMin'], value)
                row['numericMax'] = value if row['numericMax'] is None else max(row['numericMax'], value)
            declared = definitions.get(path, {}).get('enum')
            allowed = not sensitive and (declared is not None or path in controlled)
            if path in controlled and not scalar:
                raise ValueError('Controlled observed enumerations require scalar fields')
            # Only non-sensitive scalar cardinalities are observed. Containers and
            # geometry/identifier values never receive value-derived buckets.
            if not sensitive and scalar:
                bucket = unique.setdefault(path, set())
                fingerprint = hashlib.sha256(canonical(value)).hexdigest()
                if fingerprint not in bucket:
                    if len(bucket) < cardinality_cap: bucket.add(fingerprint)
                    else: row['cardinalityComplete'] = False
            if allowed and scalar:
                enum = observed.setdefault(path, {})
                if path in controlled or any(canonical(value) == canonical(item) for item in declared):
                    key = canonical(value)
                    if key not in enum and len(enum) >= cardinality_cap:
                        raise ValueError('Observed enumeration budget exceeded; preserve input')
                    enum[key] = value
                else: row['outsideDeclaredEnumCount'] = row.get('outsideDeclaredEnumCount', 0) + 1
            if isinstance(value, dict): walk_object(value, path)
            elif isinstance(value, list):
                row['arrayLengthMin'] = len(value) if row['arrayLengthMin'] is None else min(row['arrayLengthMin'],len(value))
                row['arrayLengthMax'] = len(value) if row['arrayLengthMax'] is None else max(row['arrayLengthMax'],len(value))
                array_items[path] = array_items.get(path, 0) + len(value)
                if path[0] == 'geometry' and 'coordinates' in path and value and all(
                    isinstance(item,(int,float)) and not isinstance(item,bool) for item in value):
                    dimensions = geometry_summary['coordinateDimensions']
                    key = str(len(value))
                    dimensions[key] = dimensions.get(key, 0) + 1
                for item in value: observe(item, path + ('*',))
        walk_object(record)
        for path in seen: record_presence[path] = record_presence.get(path, 0) + 1

    with source.open('rb') as stream:
        if format == 'ndjson':
            while True:
                raw = stream.readline(max_bytes - total_bytes + 1)
                if not raw: break
                total_bytes += len(raw)
                if total_bytes > max_bytes: raise ValueError('Input byte budget exceeded')
                digest.update(raw)
                if raw.strip(): consume(load_json(raw.decode('utf-8')))
        else:
            raw = stream.read(max_bytes + 1)
            if len(raw) > max_bytes: raise ValueError('Input byte budget exceeded')
            total_bytes = len(raw); digest.update(raw)
            document = load_json(raw.decode('utf-8'))
            depth_check(document, 0, max_depth)
            if not isinstance(document, dict) or document.get('type') != 'FeatureCollection' or not isinstance(document.get('features'), list):
                raise ValueError('Expected GeoJSON FeatureCollection')
            for record in document['features']: consume(record)
    result_fields = []
    for path in sorted(set(fields) | set(definitions)):
        row = fields.get(path, {'present': 0, 'null': 0, 'types': {},
            'maximumStringLength': 0, 'numericMin': None, 'numericMax': None}).copy()
        denominator = array_items.get(path[:-1], 0) if path[-1] == '*' else containers.get(path[:-1], 0)
        row.update(path=list(path), opportunities=denominator, missing=denominator-row['present'],
            recordPresence=record_presence.get(path, 0), recordAbsence=count-record_presence.get(path, 0))
        if path in unique:
            row['cardinalityLowerBound'] = len(unique[path])
            row['cardinalityScope'] = 'non-sensitive-scalar-occurrences'
        else:
            row['cardinalityLowerBound'] = None
            row['cardinalityScope'] = 'not-observed-sensitive-or-container'
        row.setdefault('cardinalityComplete', True)
        if path in observed:
            row['observedEnumeration'] = [observed[path][key] for key in sorted(observed[path])]
            row['observedEnumerationScope'] = 'allowlisted-field' if path in controlled else 'declared-values-only'
        result_fields.append(row)
    result = {'profile': 'okf-plus-transient-feature-profile.v1', 'scanComplete': True,
        'recordCount': count, 'inputBytes': total_bytes, 'inputSha256': digest.hexdigest(),
        'format': format, 'declaredSchema': schema, 'declaredSchemaSha256': hashlib.sha256(canonical(schema)).hexdigest(),
        'retrievalRecipe': recipe, 'retrievalRecipeSha256': hashlib.sha256(canonical(recipe)).hexdigest(),
        'fields': result_fields, 'geometryStructure': geometry_summary, 'distribution': 'private', 'executionAdmitted': False,
        'limitations': ['Observed values are not provider-wide enumerations.',
            'Geometry coordinates, identifiers and free-text values are not retained.',
            'Cardinality is a lower bound where cardinalityComplete is false.',
            'Wildcard paths identify array items; missing counts use parent-object occurrences, not feature counts.',
            'Schema tuple items and alternative branches remain in the declared schema; they are not flattened.']}
    # Confirm input stability before publishing or deleting any evidence.
    current = no_symlinks(source).stat()
    if (initial.st_dev,initial.st_ino,initial.st_size,initial.st_mtime_ns) != (current.st_dev,current.st_ino,current.st_size,current.st_mtime_ns):
        raise ValueError('Input changed during profiling')
    output.parent.mkdir(parents=True, exist_ok=True)
    no_symlinks(output.parent)
    staged = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix='.'+output.name+'-', delete=False) as handle:
            staged = Path(handle.name)
            handle.write(canonical(result)); handle.flush(); os.fsync(handle.fileno())
        # Hard link publishes an entire regular file atomically without overwrite.
        os.link(staged, output)
        directory_fd = os.open(output.parent, os.O_RDONLY)
        try: os.fsync(directory_fd)
        finally: os.close(directory_fd)
    finally:
        if staged is not None: staged.unlink(missing_ok=True)
    if discard_after_success:
        # Cardinality overflow means the profile is explicitly incomplete; keep source.
        if any(not row['cardinalityComplete'] for row in result_fields):
            raise ValueError('Cardinality budget incomplete; profile published but input preserved')
        no_symlinks(source).unlink()
    return result


def _definition_fragments(definition, path, limit):
    """Lossless canonical JSON text parts; an oversized manifest fails closed."""
    raw = canonical(definition)
    whole_hash = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8')
    files, parts, start = {}, [], 0
    while start < len(text):
        number = len(parts) + 1
        name = 'definition-' + whole_hash + '-part-' + str(number) + '.jsonld'
        def encoded(end):
            return canonical({'@context': {'okfp': PREFIXES['okfp'],
                'text': {'@id': 'okfp:canonicalJsonText', '@type': '@json'}},
                '@id': 'urn:sha256:' + whole_hash + ':part:' + str(number),
                '@type': 'okfp:PrivateSchemaDefinitionPart', 'text': text[start:end]})
        low, high, best = start + 1, len(text), None
        while low <= high:
            middle = (low + high) // 2
            payload = encoded(middle)
            if len(payload) <= limit:
                best = middle, payload
                low = middle + 1
            else: high = middle - 1
        if best is None: raise ValueError('Definition fragment cannot fit byte ceiling')
        end, payload = best
        files[name] = payload
        parts.append({'file': name, 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)})
        start = end
    manifest_name = 'definition-' + whole_hash + '-manifest.json'
    manifest = {'profile': 'okf-plus-lossless-schema-definition.v1',
        'sha256': whole_hash, 'bytes': len(raw), 'encoding': 'UTF-8',
        'reconstruction': 'Concatenate text from ordered parts without a delimiter; parse complete JSON.',
        'parts': parts}
    payload = canonical(manifest)
    if len(payload) > limit: raise ValueError('Definition manifest exceeds byte ceiling; nothing published')
    files[manifest_name] = payload
    return {'manifest': manifest_name, 'manifestSha256': hashlib.sha256(payload).hexdigest(),
            'sha256': whole_hash, 'bytes': len(raw), 'nativePath': list(path)}, files


def export_field_knowledge(profile_path, output_dir, field_identities=None, max_card_bytes=16384):
    """Publish bounded private JSON-LD cards from a complete machine profile.

    Identity mapping keys are exact tuple paths; values are HTTPS field identity
    strings or dictionaries with @id, structuralField and/or collection HTTPS
    identities. No source/native identity is inferred from a property name.
    The index is an ordered navigation manifest, outside the per-card ceiling.
    Linux renameat2 is required for atomic no-overwrite directory publication.
    """
    profile_path, output_dir = no_symlinks(profile_path), no_symlinks(output_dir)
    if type(max_card_bytes) is not int or max_card_bytes < 1:
        raise ValueError('Card byte ceiling must be a positive integer')
    if not output_dir.is_relative_to(ROOT / 'artifacts') or output_dir == ROOT / 'artifacts':
        raise ValueError('Field knowledge must remain beneath ignored artifacts/')
    if output_dir.exists(): raise ValueError('Knowledge output already exists')
    raw = profile_path.read_bytes()
    snapshot = load_json(raw.decode('utf-8'))
    if snapshot.get('profile') != 'okf-plus-transient-feature-profile.v1' or snapshot.get('scanComplete') is not True:
        raise ValueError('A complete supported machine profile is required')
    for key, hash_key in [('declaredSchema','declaredSchemaSha256'),('retrievalRecipe','retrievalRecipeSha256')]:
        checked_metadata(snapshot[key])
        if hashlib.sha256(canonical(snapshot[key])).hexdigest() != snapshot[hash_key]:
            raise ValueError('Profile metadata checksum mismatch')
    for key in ('inputSha256','declaredSchemaSha256','retrievalRecipeSha256'):
        value = snapshot[key]
        if not isinstance(value,str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('Invalid profile digest')
    profile_hash = hashlib.sha256(raw).hexdigest()
    definitions = schema_fields(snapshot['declaredSchema'])
    identities = field_identities or {}
    paths = [tuple(row['path']) for row in snapshot['fields']]
    if len(set(paths)) != len(paths) or not set(identities) <= set(paths):
        raise ValueError('Duplicate profile path or unknown identity mapping')
    if any(not path or any(not isinstance(part,str) for part in path) for path in paths):
        raise ValueError('Invalid native field path')
    context = {**PREFIXES, **{key:{'@id':'okfp:'+key,'@type':'@json'} for key in
        ('nativePath','statistics','declaredFieldDefinition','declaredFieldDefinitionRef','childCards','evidenceHashes','observedScope','rights')}}
    payloads, entries, definition_files = [], [], {}
    for row, path in zip(snapshot['fields'], paths):
        mapping = identities.get(path, {})
        if isinstance(mapping,str): mapping = {'@id':mapping}
        if not isinstance(mapping,dict) or not set(mapping) <= {'@id','structuralField','collection'}:
            raise ValueError('Unrecognised field identity mapping')
        for value in mapping.values(): safe_reference(value)
        path_hash = hashlib.sha256(canonical(list(path))).hexdigest()
        generated_id = 'urn:sha256:' + profile_hash + ':field:' + path_hash
        card = {'@context':context, '@id':mapping.get('@id',generated_id),
            '@type':'okfp:PrivateObservedFieldProfile','nativePath':list(path),
            'statistics':row, 'declaredFieldDefinition':definitions.get(path),
            'evidenceHashes':{'inputSha256':snapshot['inputSha256'],'profileSha256':profile_hash,
                'schemaSha256':snapshot['declaredSchemaSha256'],'recipeSha256':snapshot['retrievalRecipeSha256']},
            'prov:wasDerivedFrom':{'@id':'urn:sha256:'+profile_hash},
            'observedScope':{'recordCount':snapshot['recordCount'],'inputBytes':snapshot['inputBytes'],
                'scanComplete':True,'providerUniverseComplete':False,
                'enumerationScope':row.get('observedEnumerationScope','not-observed'),
                'cardinalityScope':row.get('cardinalityScope'),'cardinalityComplete':row['cardinalityComplete']},
            'rights':{'distribution':'private','executionAdmitted':False}}
        if 'structuralField' in mapping: card['dcterms:references'] = {'@id':mapping['structuralField']}
        if 'collection' in mapping: card['dcterms:isPartOf'] = {'@id':mapping['collection']}
        payload = canonical(card)
        if len(payload) > max_card_bytes and definitions.get(path) is not None:
            reference, fragments = _definition_fragments(definitions[path], path, max_card_bytes)
            card.pop('declaredFieldDefinition')
            card['declaredFieldDefinitionRef'] = reference
            card['childCards'] = [{'nativePath': list(child),
                'file': 'field-' + hashlib.sha256(canonical(list(child))).hexdigest() + '.jsonld'}
                for child in paths if len(child) == len(path) + 1 and child[:len(path)] == path]
            definition_files.update(fragments)
            payload = canonical(card)
        if len(payload) > max_card_bytes:
            raise ValueError('Complete field card exceeds byte ceiling; nothing published')
        filename = 'field-' + path_hash + '.jsonld'
        entries.append({'path':list(path),'file':filename,'sha256':hashlib.sha256(payload).hexdigest(),
            'bytes':len(payload),'fieldIdentity':mapping.get('@id'),
            'structuralField':mapping.get('structuralField'),'collection':mapping.get('collection')})
        payloads.append(payload)
    # The entire cohort is validated and serialised before any output is created.
    index = {'profile':'okf-plus-private-field-knowledge-index.v1','profileSha256':profile_hash,
        'inputSha256':snapshot['inputSha256'],'maxCardBytes':max_card_bytes,'fieldCount':len(entries),
        'distribution':'private','executionAdmitted':False,'fields':entries,
        'definitionFiles':[{'file': name, 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload)}
            for name,payload in sorted(definition_files.items())]}
    output_dir.parent.mkdir(parents=True,exist_ok=True)
    no_symlinks(output_dir.parent)
    staged = Path(tempfile.mkdtemp(dir=output_dir.parent,prefix='.'+output_dir.name+'-staging-'))
    try:
        for entry,payload in zip(entries,payloads):
            with (staged / entry['file']).open('wb') as stream:
                stream.write(payload);stream.flush();os.fsync(stream.fileno())
        for name,payload in definition_files.items():
            with (staged / name).open('wb') as stream:
                stream.write(payload);stream.flush();os.fsync(stream.fileno())
        with (staged / 'index.json').open('wb') as stream:
            stream.write(canonical(index));stream.flush();os.fsync(stream.fileno())
        no_symlinks(output_dir)
        libc = ctypes.CDLL(None,use_errno=True)
        rename = getattr(libc,'renameat2',None)
        if rename is None: raise OSError('Atomic field publication requires Linux renameat2')
        rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]
        rename.restype=ctypes.c_int
        if rename(-100,os.fsencode(staged),-100,os.fsencode(output_dir),1):
            error=ctypes.get_errno();raise OSError(error,os.strerror(error),str(output_dir))
    finally:
        if staged.exists(): shutil.rmtree(staged)
    return index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--format', choices=('ndjson','geojson'), default='ndjson')
    parser.add_argument('--schema', type=Path)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--controlled-field', action='append', default=[])
    parser.add_argument('--max-bytes', type=int, default=32*1024*1024)
    parser.add_argument('--max-records', type=int, default=100000)
    parser.add_argument('--max-depth', type=int, default=32)
    parser.add_argument('--cardinality-cap', type=int, default=10000)
    parser.add_argument('--discard-after-success', action='store_true')
    args=parser.parse_args()
    result=profile(args.source,args.output,format=args.format,
        schema=load_json(no_symlinks(args.schema).read_text()) if args.schema else None,
        recipe=load_json(no_symlinks(args.recipe).read_text()) if args.recipe else None,
        controlled_fields=args.controlled_field,max_bytes=args.max_bytes,max_records=args.max_records,
        max_depth=args.max_depth,cardinality_cap=args.cardinality_cap,discard_after_success=args.discard_after_success)
    print('Complete records:',result['recordCount'],'input SHA256:',result['inputSha256'])


if __name__=='__main__': main()
