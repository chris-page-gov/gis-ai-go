"""Optional label-origin checks for offline reviewed classification inputs.

The native pointer binds a projection claim to retained JSON. It cannot establish
that the retained JSON is an authentic source, or that the chosen field is a label.
"""
import json
import re

KEYS={'kind','sourceId','sourceLocator','nativePointer','nativeState','languagePointer','displayLanguage'}
STATES={'absent','null','empty-string','string'}

def require(ok,message):
    if not ok:raise ValueError('Label origin: '+message)

def snapshot(value):
    nodes=0;seen=set()
    def visit(x,depth=0):
        nonlocal nodes
        nodes+=1;require(nodes<=4096 and depth<=16,'JSON bound')
        if x is None or type(x) in (str,int,float,bool):return x
        require(type(x) in (dict,list),'plain JSON required')
        require(id(x) not in seen,'cycle');seen.add(id(x))
        if type(x) is list:result=[visit(v,depth+1)for v in x]
        else:
            require(all(type(k)is str for k in x),'string keys required')
            result={k:visit(v,depth+1)for k,v in x.items()}
        seen.remove(id(x));return result
    result=visit(value)
    try:raw=json.dumps(result,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8')
    except (UnicodeError,ValueError)as e:raise ValueError('Label origin: finite UTF-8 JSON required')from e
    require(len(raw)<=131072,'entry byte bound');return result

def pointed_state(entry,pointer):
    require(type(pointer)is str and pointer.startswith('/native/')and len(pointer)<=512
            and not re.search(r'~(?![01])',pointer),'pointer syntax')
    parts=pointer.split('/')[1:];require(len(parts)<=16,'pointer depth')
    value=entry
    for i,token in enumerate(parts):
        key=token.replace('~1','/').replace('~0','~');last=i==len(parts)-1
        if type(value)is dict:
            if key not in value:
                require(last,'pointer parent absent; point to the actual missing field')
                return {'state':'absent','value':None}
            value=value[key]
        elif type(value)is list:
            require(bool(re.fullmatch(r'0|[1-9][0-9]*',key)),'array index syntax')
            require(int(key)<len(value),'array index absent')
            value=value[int(key)]
        else:raise ValueError('Label origin: pointer parent is not a container')
    if value is None:return {'state':'null','value':None}
    require(type(value)is str,'pointed label/language must be string or null')
    return {'state':'empty-string'if value=='' else'string','value':value}

def validate_label_origin(supplied,sources):
    require(type(supplied)is dict and type(sources)is dict,'entry/source objects')
    if 'labelOrigin' not in supplied:return None  # Existing payload behaviour is unchanged.
    entry=snapshot(supplied);origin=entry['labelOrigin']
    require(type(origin)is dict and set(origin)==KEYS,'closed origin metadata')
    require(len(json.dumps(origin,ensure_ascii=False,separators=(',',':')).encode('utf-8'))<=8192,'origin byte bound')
    require(origin['kind']in ('source-native','project-display-fallback'),'kind')
    require(origin['nativeState']in STATES,'native state')
    require(type(entry.get('label'))is str and len(entry['label'])<=10000,'label string')
    require(origin['sourceId']==entry.get('sourceId')and origin['sourceId']in sources,'source binding')
    require(type(origin['sourceLocator'])is str and 0<len(origin['sourceLocator'])<=10000
            and origin['sourceLocator']==entry.get('sourceLocator'),'locator binding')
    source=sources[origin['sourceId']]
    require(type(source)is dict and source.get('id')==origin['sourceId']
            and type(source.get('sha256'))is str and bool(re.fullmatch(r'[0-9a-f]{64}',source['sha256'])),'source identity/hash')
    native=pointed_state(entry,origin['nativePointer'])
    require(native['state']==origin['nativeState'],'native state differs')
    language=({'state':'not-asserted','value':None}if origin['languagePointer']is None
              else pointed_state(entry,origin['languagePointer']))
    source_language=language['value']if language['state']=='string'else None
    require(source_language is None or len(source_language)<=80,'native language bound')
    display_language=origin['displayLanguage']
    require(display_language is None or (type(display_language)is str and 0<len(display_language)<=80),'display language')
    asserted_language=entry.get('labelLanguage')
    if origin['kind']=='source-native':
        require(native['state']in ('empty-string','string')and entry['label']==native['value'],'native label differs')
        require(asserted_language==source_language and display_language==source_language,'source label language differs')
    else:
        require(native['state']in ('absent','null')and bool(entry['label']),'fallback requires absent/null native label')
        require(asserted_language is None,'fallback must not inherit source label language')
        for alias in entry.get('aliases',[]):
            require(alias.get('text')!=entry['label'],'fallback must not be an alias')
        for form in entry.get('nativeSearchForms',[]):
            require(form.get('text')!=entry['label'],'fallback must not be a source-native search form')
    return {'kind':origin['kind'],'nativeState':native['state'],'nativePointer':origin['nativePointer'],
            'sourceId':origin['sourceId'],'sourceSha256':source['sha256'],'sourceLocator':origin['sourceLocator'],
            'nativeLanguage':language,'displayLanguage':display_language}

def label_assertions(entry,sources,coded):
    """Replacement for the exporter's unconditional label assertion only."""
    entry=snapshot(entry)if 'labelOrigin'in entry else entry
    result=validate_label_origin(entry,sources)
    if result is not None and result['kind']=='project-display-fallback':return {}
    label=({'@value':entry['label'],'@language':entry['labelLanguage']}
           if entry.get('labelLanguage')else entry['label'])
    return {'skos:prefLabel'if coded else'rdfs:label':label}

def title_origin(entry,sources):
    """Optional discovery decoration; record title remains a human display name."""
    result=validate_label_origin(entry,sources)
    return None if result is None else result['kind']

def qualify_title_form(row,form):
    """Decorate only a retained record-title occurrence; never create a lexical alias."""
    entry=row.get('details',{}).get('entry')
    if type(entry)is not dict or 'labelOrigin'not in entry:return form
    sources={s['id']:s for s in row['details']['scheme']['sources']}
    origin=title_origin(entry,sources)
    require(form.get('kind')=='record-title'and form.get('pointer')=='/title'
            and form.get('value')==entry['label']and row.get('title')==entry['label'],
            'title occurrence differs from retained entry')
    return {**form,'labelOrigin':origin}
