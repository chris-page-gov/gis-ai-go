"""Offline OKF+ source model. JSON front matter is a strict YAML 1.2 subset."""
from __future__ import annotations
import hashlib
import json
import re
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, urlparse, parse_qsl, unquote

BASE='https://chris-page-gov.github.io/gis-ai-go/okf-plus/'
CONTEXT=BASE+'context.jsonld'
PROFILE=BASE+'profile/v1'
PREFIXES={
    'okf':'https://w3id.org/okf/','okfp':BASE+'vocab/',
    'dcat':'http://www.w3.org/ns/dcat#','dcterms':'http://purl.org/dc/terms/',
    'prov':'http://www.w3.org/ns/prov#','skos':'http://www.w3.org/2004/02/skos/core#',
    'geo':'http://www.opengis.net/ont/geosparql#','qb':'http://purl.org/linked-data/cube#',
    'sdmx':'http://purl.org/linked-data/sdmx#','sdmx-code':'http://purl.org/linked-data/sdmx/2009/code#',
    'time':'http://www.w3.org/2006/time#','dqv':'http://www.w3.org/ns/dqv#',
    'adms':'http://www.w3.org/ns/adms#','odrl':'http://www.w3.org/ns/odrl/2/',
    'spdx':'http://spdx.org/rdf/terms#','schema':'https://schema.org/',
    'csvw':'http://www.w3.org/ns/csvw#','sosa':'http://www.w3.org/ns/sosa/',
    'ssn':'http://www.w3.org/ns/ssn/','qudt':'http://qudt.org/schema/qudt/',
    'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs':'http://www.w3.org/2000/01/rdf-schema#',
    'owl':'http://www.w3.org/2002/07/owl#','xsd':'http://www.w3.org/2001/XMLSchema#',
}
JSON_KEYS=['sources','temporal','update','details','rights','coverage','assertions','limitations','provenance','schemaEvidence']
CTX={'@version':1.1,**PREFIXES,
 'title':'dcterms:title','description':'dcterms:description','type':'okfp:recordType',
 'tags':'dcat:keyword','resource':{'@id':'dcat:landingPage','@type':'@id'},
 'nativeIdentifier':'dcterms:identifier','sourceFamily':'okfp:sourceFamily',
 'status':'okfp:lifecycleStatus','generated':{'@id':'okfp:generated','@type':'@json'},'assertionStatus':'okfp:assertionStatus',
 'reviewStatus':'okfp:reviewStatus','okf_version':'okfp:coreVersion',
 **{k:{'@id':'okfp:'+k,'@type':'@json'} for k in JSON_KEYS}}

def canonical(value):return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def duplicate_guard(pairs):
    obj={}
    for key,val in pairs:
        if key in obj:raise ValueError('Duplicate JSON/YAML key: '+key)
        obj[key]=val
    return obj

def load_json(text):
    def reject(value):raise ValueError('Non-finite number: '+value)
    return json.loads(text,object_pairs_hook=duplicate_guard,parse_constant=reject)

def read_markdown(path):
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):raise ValueError('Missing front matter: '+str(path))
    parts=text.split('\n---\n',1)
    if len(parts)!=2:raise ValueError('Unterminated front matter')
    return load_json(parts[0][4:]),parts[1]

def markdown_text(record,body):
    return '---\n'+json.dumps(record,ensure_ascii=False,indent=2,allow_nan=False)+'\n---\n\n'+body.rstrip()+'\n'

def write_markdown(path,record,body):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(markdown_text(record,body),encoding='utf-8')

def identifier(family,native):return BASE+'id/'+family+'/'+quote(str(native),safe='')
def file_key(native):
    slug=re.sub('[^a-z0-9]+','-',str(native).lower()).strip('-')[:80]
    return (slug or 'record')+'-'+hashlib.sha256(str(native).encode()).hexdigest()[:12]

def ref(url):return {'@id':url}
def literal(value,datatype):return {'@value':value,'@type':datatype}
FREQUENCIES={'annual':'A','annually':'A','yearly':'A','quarterly':'Q','monthly':'M','weekly':'W','daily':'D'}

def record(family,native,title,description,resource,source,kind='Dataset',details=None):
    typ={'Dataset':'dcat:Dataset','Collection':'dcat:Dataset','Documentation':'dcterms:BibliographicResource','Concept':'skos:Concept','SourceFamily':'dcat:Catalog','Specification':'dcterms:Standard','DataService':'dcat:DataService'}[kind]
    return {'@context':CONTEXT,'@id':identifier(family,native),'@type':[typ,'okfp:MetadataRecord'],'type':kind,'title':title,'description':description,'nativeIdentifier':str(native),'sourceFamily':family,'resource':resource,'status':'draft','generated':{'by':'gis-ai-go OKF+ source producer'},'okfp:machineImported':kind not in ('Concept','SourceFamily'),'assertionStatus':'normalised','reviewStatus':'not-human-reviewed','tags':[],'sources':[source],
        'prov:wasDerivedFrom':ref(resource),
        'dcterms:conformsTo':ref(PROFILE),
        'temporal':{'status':'not-evidenced' if kind in ('Dataset','Collection') else 'not-applicable','kind':'dataset-reference-period','start':None,'end':None,'sourceField':None,'note':'No supported reference-period extent in captured metadata; release and catalogue dates are separate.' if kind in ('Dataset','Collection') else 'Dataset reference-period extent is not applicable to this record type.'},
        'update':{'frequency':{'status':'not-evidenced' if kind in ('Dataset','Collection','DataService') else 'not-applicable','label':None,'iri':None,'sourceField':None},'releaseCatalogue':[],'releaseFeed':[],'nextRelease':None,'metadataModified':None,'releaseVersion':None},
        'rights':{'metadata':'Public metadata citation and factual normalisation; source rights retained.','describedData':'Not established by metadata discovery; consult source-specific terms.','retrievalAuthority':'metadata-only','executionAdmitted':False},
        'limitations':[],'details':details or {}}

def apply_frequency(row,label,source_field):
    if not label:return
    code=FREQUENCIES.get(str(label).strip().lower())
    iri=PREFIXES['sdmx-code']+'freq-'+code if code else None
    row['update']['frequency']={'status':'source-stated','label':label,'iri':iri,'sourceField':source_field}
    row['dcterms:accrualPeriodicity']=ref(iri) if iri else {'@type':'dcterms:Frequency','rdfs:label':label}

def apply_temporal(row,start,end,kind,source_field):
    bounds=[]
    for value in (start,end):
        if value is None:bounds.append(None);continue
        if not isinstance(value,str):raise ValueError('Temporal date must be source text')
        parsed=datetime.fromisoformat(value.replace('Z','+00:00')) if 'T' in value else date.fromisoformat(value)
        if isinstance(parsed,datetime) and parsed.tzinfo is None:raise ValueError('Temporal date-time requires timezone')
        bounds.append(parsed)
    if all(v is not None for v in bounds):
        if type(bounds[0]) is not type(bounds[1]):raise ValueError('Mixed temporal bound precision requires explicit review')
        if bounds[0]>bounds[1]:raise ValueError('Reversed temporal extent')
    row['temporal']={'status':'source-stated','kind':kind,'start':start,'end':end,'sourceField':source_field,'note':'An open end means the source supplied no terminal date; it does not prove a complete observation history or as-of API support.'}
    extent={'@type':'dcterms:PeriodOfTime'}
    for key,value in [('dcat:startDate',start),('dcat:endDate',end)]:
        if value:extent[key]=literal(value,'xsd:dateTime' if 'T' in value else 'xsd:date')
    row['dcterms:temporal']=extent


def safe_reference(url):
    if not isinstance(url,str) or any(ord(c)<=32 or ord(c)==127 for c in url):raise ValueError('Invalid URL text')
    p=urlparse(url)
    if p.scheme!='https' or not p.hostname or p.username or p.password or p.port not in (None,443):raise ValueError('Unsafe reference URL')
    forbidden={'key','apikey','token','accesstoken','clientsecret','password','signature','sig','authorization','secret'}
    for key,_ in parse_qsl(p.query,keep_blank_values=True):
        normal=re.sub('[^a-z0-9]','',unquote(unquote(key)).lower())
        if normal in forbidden:raise ValueError('Credential parameter in URL')
    return url

def compact_time_metadata(item):
    """Losslessly tabulate repeated Nomis field names for complete evidence units.

    Original normalised snapshots remain unchanged. A null description cell means
    the description key was absent; an empty object remains an empty object.
    """
    value=deepcopy(item)
    codes=value.pop('codes')
    rows=[]
    for code in codes:
        if not {'value','revisionMetadata'}<=code.keys() or not set(code)<={'value','description','revisionMetadata'}:raise ValueError('Unrecognised native time-code fields')
        if 'description' in code and not isinstance(code['description'],dict):raise ValueError('Invalid native description')
        revisions=code['revisionMetadata']
        if not isinstance(revisions,list) or any(set(r)!={'title','value'} for r in revisions):raise ValueError('Unrecognised revision metadata')
        rows.append([code['value'],code.get('description'),[[r['title'],r['value']] for r in revisions]])
    value['timeOptionsTable']={'encoding':'gis-ai-go.native-time-table.v1','columns':['value','description','revisionMetadata'],'revisionColumns':['title','value'],'absentDescription':None,'rows':rows}
    return value

def expand_time_metadata(item):
    value=deepcopy(item);table=value.pop('timeOptionsTable')
    if table['encoding']!='gis-ai-go.native-time-table.v1' or table['columns']!=['value','description','revisionMetadata'] or table['revisionColumns']!=['title','value'] or table['absentDescription'] is not None:raise ValueError('Unknown native time table encoding')
    codes=[]
    for value_code,description,revisions in table['rows']:
        code={'value':value_code,'revisionMetadata':[{'title':title,'value':val} for title,val in revisions]}
        if description is not None:code['description']=description
        codes.append(code)
    value['codes']=codes
    return value
