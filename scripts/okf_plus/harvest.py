#!/usr/bin/env python3
"""Bounded, credential-free OS/ONS metadata capture; never retrieves observations."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import time
import signal
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode, urlparse, parse_qs, unquote
from urllib.request import HTTPRedirectHandler, Request, build_opener

try:
    from .model import safe_reference
except ImportError:
    from model import safe_reference

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = {'api.os.uk', 'docs.os.uk', 'api.beta.ons.gov.uk', 'www.nomisweb.co.uk', 'www.arcgis.com', 'osmetadata.astuntechnology.com', 'www.ordnancesurvey.co.uk'}
MAX_BYTES = 16 * 1024 * 1024

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():raise ValueError('Capture destination cannot be a symbolic link')
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,prefix='.'+path.name+'-',delete=False) as stream:
            temporary=Path(stream.name)
            json.dump(data,stream,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)
            stream.write('\n');stream.flush();os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary:temporary.unlink(missing_ok=True)

def allowed(url):
    safe_reference(url)
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in ALLOWED or p.username or p.password or p.port not in (None,443):
        raise ValueError('URL is outside the approved metadata hosts')
    path = p.path
    # Check before matching the raw route: downstream servers/proxies can decode
    # percent escapes or normalise separators differently from urllib. A source
    # URL must not use those differences to escape an admitted metadata route.
    decoded_path = path
    for _ in range(16):
        if ('\\' in decoded_path or any(segment in ('.', '..') for segment in decoded_path.split('/'))
                or re.search(r'%(?:2f|5c)', decoded_path, re.I)
                or re.search(r'%(?![0-9a-fA-F]{2})', decoded_path)):
            raise ValueError('Ambiguous or traversing metadata path')
        next_path = unquote(decoded_path, errors='strict')
        if next_path == decoded_path:
            break
        decoded_path = next_path
    else:
        raise ValueError('Excessively nested metadata path encoding')
    if p.params:
        raise ValueError('Path parameters are outside the metadata profile')
    permitted = (
        p.hostname == 'api.os.uk' and (re.fullmatch(r'/downloads/v1/products(?:/[A-Za-z0-9_-]+)?', path) or re.fullmatch(r'/features/ngd/ofa/v1/collections(?:/[a-z0-9-]+/(?:schema|queryables))?', path))
        or p.hostname == 'docs.os.uk' and (path.endswith('/llms.txt') or path.endswith('.md'))
        or p.hostname == 'api.beta.ons.gov.uk' and re.fullmatch(r'/v1/(?:datasets(?:/[A-Za-z0-9_-]+(?:/editions(?:/[A-Za-z0-9_-]+(?:/versions(?:/[0-9]+(?:/(?:metadata|dimensions(?:/[A-Za-z0-9_-]+/options)?))?)?)?)?)?)?|code-lists|population-types|search(?:/releases)?)', path)
        or p.hostname == 'www.nomisweb.co.uk' and re.fullmatch(r'/api/v01/(?:dataset/def.sdmx.json|dataset/NM_[0-9]+_[0-9]+\.overview\.json|dataset/NM_[0-9]+_[0-9]+/time\.def\.sdmx\.json|contenttype/index.json)',path)
        or p.hostname == 'osmetadata.astuntechnology.com' and path in ('/geonetwork/api/collections/main','/geonetwork/api/collections/044fac9d-3bba-4214-b010-eeb9978422b2/items')
        or p.hostname == 'www.ordnancesurvey.co.uk' and path in ('/products/search-for-os-products','/api/delivery/projects/osweb/entries/search')
        or p.hostname == 'www.arcgis.com' and path in ('/sharing/rest/search','/sharing/rest/portals/ESMARspQHYMw9BZ9')
    )
    if p.hostname == 'api.beta.ons.gov.uk' and path == '/v1/population-types':
        q = parse_qs(p.query, keep_blank_values=True)
        if p.query and (set(q) != {'limit', 'offset'} or any(len(v) != 1 for v in q.values())
                        or not all(re.fullmatch(r'[0-9]{1,7}', q[k][0]) for k in ('limit', 'offset'))
                        or not 1 <= int(q['limit'][0]) <= 1000 or not 0 <= int(q['offset'][0]) <= 1000000):
            raise ValueError('Unsupported population-type metadata query')
    if p.hostname == 'www.ordnancesurvey.co.uk' and path == '/api/delivery/projects/osweb/entries/search':
        q=parse_qs(p.query,keep_blank_values=True)
        expected_fields='pageMetaData.pageTitle,pageMetaData.image,sys.properties,pageMetaData.description,pageMetaData.sectors,dataType,access,title'
        expected_where=[{'field':'sys.versionStatus','equalTo':'published'},{'field':'sys.language','in':['en-GB']},{'field':'sys.contentTypeId','in':['product']}]
        if set(q)!={'aggregations','fields','linkDepth','pageIndex','pageSize','where'} or any(len(v)!=1 for v in q.values()) or q['fields']!=[expected_fields] or q['linkDepth']!=['3'] or q['pageSize']!=['60'] or not re.fullmatch(r'[0-9]{1,3}',q['pageIndex'][0]) or int(q['pageIndex'][0])>100 or json.loads(q['where'][0])!=expected_where or json.loads(q['aggregations'][0])!={'sf_dataType.sys.id':{'field':'dataType.sys.id','size':100},'sf_access.sys.id':{'field':'access.sys.id','size':100}}:
            raise ValueError('Unsupported product delivery query')
    if not permitted:
        raise ValueError('Route is outside the closed metadata profile: '+path)
    if any(k in p.query.lower() for k in ('token'+'=', 'key'+'=', 'api_'+'key=', 'api'+'key=')):
        raise ValueError('Credentials are forbidden')
    return url

class Redirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A redirect is a new wire request. Reject it rather than hiding it
        # outside the admitted request count or following source-controlled URLs.
        raise HTTPError(req.full_url, code, 'Redirect requires a separately admitted capture', headers, fp)

@contextmanager
def deadline(seconds=30):
    """POSIX wall deadline for one synchronous request, including DNS and body."""
    previous=signal.getsignal(signal.SIGALRM)
    previous_timer=signal.getitimer(signal.ITIMER_REAL)
    if previous_timer[0]:raise RuntimeError('Cannot replace an existing alarm')
    def expired(_signum,_frame):raise TimeoutError('Metadata request wall deadline exceeded')
    signal.signal(signal.SIGALRM,expired)
    signal.setitimer(signal.ITIMER_REAL,seconds)
    try:yield
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,previous)

def clean_text(value):
    # Catalogue descriptions can contain named contact details and HTML. They are
    # not needed for source selection; raw responses remain in ignored evidence.
    value = html.unescape(re.sub(r'<[^>]+>', ' ', str(value or '')))
    value = re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[contact omitted]', value)
    value = re.sub(r'(?:\+44|\b0\d{2,4})[\s().-]*\d[\d\s().-]{7,}\d', '[contact omitted]',value)
    value = re.split(r'(?i)(?:for (?:more|further) information[,]? (?:please )?contact|contact (?:details|us|name)\s*:)', value, maxsplit=1)[0]
    return re.sub(r'\s+', ' ', value).strip()

class Capture:
    def __init__(self, root, max_requests=900):
        self.root=root
        self.private=root/'artifacts/okf-plus/capture'
        self.public=root/'okf-plus/source'
        self.path=self.private/'ledger.json'
        self.ledger=json.loads(self.path.read_text()) if self.path.exists() else {'profile':'okf-plus-public-metadata.v1','requests':[]}
        if type(max_requests) is not int or not 1 <= max_requests <= 4000:raise ValueError('Request ceiling must be 1..4000')
        self.max_requests=max_requests
        self.opener=build_opener(Redirect())
    def get(self,url,kind='json'):
        allowed(url)
        for prior in self.ledger['requests']:
            if prior['url']==url and prior['status']==200:
                raw=(self.private/prior['rawFile']).read_bytes()
                if hashlib.sha256(raw).hexdigest()!=prior['sha256']: raise ValueError('Raw source checksum mismatch')
                return (json.loads(raw) if kind=='json' else raw.decode()),prior
        if len(self.ledger['requests'])>=self.max_requests: raise RuntimeError('Run request ceiling reached')
        if sum(r.get('bytes',0) for r in self.ledger['requests']) >= 256*1024*1024: raise RuntimeError('Cumulative capture byte ceiling reached')
        receipt={'url':url,'retrievedAt':datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}
        self.ledger['requests'].append(receipt)
        receipt['status']='pending';dump(self.path,self.ledger)
        time.sleep(.75)
        try:
            with deadline(), self.opener.open(Request(url,headers={'User-Agent':'GIS-AI-GO-OKF-Plus/0.1 metadata-inventory','Accept':'application/json,text/plain;q=0.9'}),timeout=25) as response:
                remaining = 256*1024*1024-sum(r.get('bytes',0) for r in self.ledger['requests'])
                raw=response.read(min(MAX_BYTES,remaining)+1)
                receipt['bytes']=len(raw)
                if len(raw)>min(MAX_BYTES,remaining):raise ValueError('Response or cumulative byte ceiling exceeded')
                receipt.update(status=response.status,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),etag=response.headers.get('ETag'),lastModified=response.headers.get('Last-Modified'),finalUrl=response.url)
                receipt['rawFile']=receipt['sha256']+'.body'
                self.private.mkdir(parents=True,exist_ok=True)
                (self.private/receipt['rawFile']).write_bytes(raw)
                dump(self.path,self.ledger)
                return (json.loads(raw) if kind=='json' else raw.decode()),receipt
        except Exception as error:
            receipt.update(status=error.code if isinstance(error,HTTPError) else 'failed',error=type(error).__name__)
            if isinstance(error,HTTPError):receipt['retryAfter']=error.headers.get('Retry-After')
            dump(self.path,self.ledger)
            print('capture failed',url,receipt['status'],flush=True)
            if receipt['status']==429:raise RuntimeError('Provider rate limit: stop without retry; inspect Retry-After before a later run') from error
            return None,receipt
    def save(self,name,data,receipts,coverage):
        safe_receipts=[{k:v for k,v in r.items() if k!='rawFile'} for r in receipts]
        document={'schema':'okf-plus-source-snapshot.v1','family':name,'coverage':coverage,'receipts':safe_receipts,'records':data}
        dump(self.public/(name+'.json'),document)
        print(name,len(data),'records',coverage,flush=True)

def os_products(cap):
    data,receipt=cap.get('https://api.os.uk/downloads/v1/products')
    if data is None:return
    records=[];receipts=[receipt]
    for product in data:
        detail,r=cap.get('https://api.os.uk/downloads/v1/products/'+product['id']);receipts.append(r)
        item=detail or product
        records.append({k:v for k,v in item.items() if k in {'id','name','description','version','url','documentationUrl','supportingInfo','dataStructures','category','categories','formats','areas','downloadsUrl'}})
    cap.save('os-open-products',records,receipts,{'unit':'OS-served OpenData product','reportedTotal':len(data),'retrievedUnique':len({r['id'] for r in records}),'catalogueComplete':True,'detailsCaptured':sum(r['status']==200 for r in receipts)-1,'limitations':['Includes partner products; not the complete commercial or PSGA portfolio.','Product version is a release label, not a data reference period.']})

def ngd(cap):
    data,r=cap.get('https://api.os.uk/features/ngd/ofa/v1/collections')
    if data is None:return
    collections=data['collections'];receipts=[r];records=[]
    for c in collections:
        item={k:v for k,v in c.items() if k in {'id','title','description','crs','storageCrs','extent','links','itemType'}}
        item['schemas']={}
        for suffix in ('schema','queryables'):
            url='https://api.os.uk/features/ngd/ofa/v1/collections/'+c['id']+'/'+suffix
            schema,sr=cap.get(url);receipts.append(sr)
            if schema is None:continue
            # Preserve structural facts and controlled values, not copied prose or feature data.
            props=schema.get('properties',{})
            item['schemas'][suffix]={'id':schema.get('$id'),'dialect':schema.get('$schema'),'type':schema.get('type'),'required':schema.get('required',[]),'additionalProperties':schema.get('additionalProperties'),'properties':{k:{a:b for a,b in v.items() if a in {'type','format','enum','const','$ref','items','oneOf','anyOf','minimum','maximum','nullable'}} for k,v in props.items()},'requiredUndeclared':sorted(set(schema.get('required',[]))-set(props)),'url':url,'sha256':sr['sha256']}
        records.append(item)
    next_links=[l for l in data.get('links',[]) if l.get('rel')=='next']
    cap.save('os-ngd-collections',records,receipts,{'unit':'versioned NGD API collection','reportedTotal':len(collections),'retrievedUnique':len({r['id'] for r in records}),'catalogueComplete':not next_links,'schemasCaptured':sum('schema' in r['schemas'] for r in records),'queryablesCaptured':sum('queryables' in r['schemas'] for r in records),'limitations':['Catalogue completeness is for this returned API collection listing, not all NGD download feature types.','No feature payloads acquired; advertised temporal extent is preserved as source metadata.','Schema defects are retained; fields and queryables have different meanings.']})

def docs(cap):
    for project in ('os-apis','osngd','os-downloads'):
        data,r=cap.get('https://docs.os.uk/'+project+'/llms.txt','text')
        if data is None:continue
        entries={}
        for title,url in re.findall(r'^- \[(.*?)\]\((https://[^)]+)\)',data,re.M):
            entries[url]={'id':url,'title':html.unescape(title),'url':url,'kind':'documentation-reference'}
        cap.save(project+'-documentation',list(entries.values()),[r],{'unit':'distinct documentation URL in published navigation index','reportedTotal':len(entries),'retrievedUnique':len(entries),'catalogueComplete':True,'contentCaptured':False,'limitations':['An index entry is not proof the target is current or successfully fetched.','Includes historical, withdrawn, guide and template pages.','Documentation reference inventory; page contents are a separate capture plane.']})

def ons(cap):
    records=[];receipts=[];offset=0;total=None;stable=True
    while True:
        data,r=cap.get('https://api.beta.ons.gov.uk/v1/datasets?'+urlencode({'limit':100,'offset':offset}));receipts.append(r)
        if data is None:break
        if total is not None and total!=data['total_count']:stable=False
        total=data['total_count']
        for item in data['items']:
            records.append({k:v for k,v in item.items() if k in {'id','title','description','keywords','last_updated','links','methodologies','national_statistic','next_release','qmi','related_datasets','release_frequency','state','unit_of_measure','type'}})
        offset+=len(data['items'])
        if offset>=total or not data['items']:break
    unique={r['id']:r for r in records}
    cap.save('ons-datasets',list(unique.values()),receipts,{'unit':'public ONS dataset API identifier','reportedTotal':total,'retrievedUnique':len(unique),'catalogueComplete':total==len(unique) and stable,'stableReportedTotal':stable,'duplicateCount':len(records)-len(unique),'limitations':['ONS dataset API coverage does not include the entire ONS website or Nomis.','Metadata modification and next release are not statistical reference periods.','Edition/version metadata is separately inventoried.']})

def nomis(cap):
    data,r=cap.get('https://www.nomisweb.co.uk/api/v01/dataset/def.sdmx.json')
    if data is None:return
    families=data['structure']['keyfamilies']['keyfamily'];records=[]
    for x in families:
        ann=x.get('annotations',{}).get('annotation',[])
        item={k:v for k,v in x.items() if k in {'id','agencyid','name','description','components','version','uri'}}
        item['annotations']={a['annotationtitle']:clean_text(a.get('annotationtext','')) for a in ann if a.get('annotationtitle') in {'Status','Keywords','Units','FirstReleased','LastUpdated','NextUpdate','Frequency','Source','SubDescription','Mnemonic'}}
        records.append(item)
    cap.save('ons-nomis-datasets',records,[r],{'unit':'Nomis key family','reportedTotal':len(families),'retrievedUnique':len({x['id'] for x in records}),'catalogueComplete':True,'limitations':['Complete returned key-family document, not proof of all historical Nomis products.','Code-list references are captured; full code values and observation time ranges require separate metadata routes.']})

def geography(cap):
    org,r=cap.get('https://www.arcgis.com/sharing/rest/portals/ESMARspQHYMw9BZ9?f=json')
    receipts=[r];records=[];start=1;total=None;stable=True
    while start!=-1:
        url='https://www.arcgis.com/sharing/rest/search?'+urlencode({'f':'json','q':'orgid:ESMARspQHYMw9BZ9','num':100,'start':start,'sortField':'created','sortOrder':'asc'})
        data,r=cap.get(url);receipts.append(r)
        if data is None or 'error' in data:break
        if total is not None and total!=data['total']:stable=False
        total=data['total']
        for item in data['results']:
            safe={k:v for k,v in item.items() if k in {'id','title','type','typeKeywords','tags','extent','spatialReference','url','created','modified','access','licenseInfo','culture','categories'}}
            for key in ('description','snippet'):
                safe[key]=clean_text(item.get(key,''))
            # Item owners can be personal account handles; org attribution suffices.
            safe['organisationId']='ESMARspQHYMw9BZ9'
            records.append(safe)
        nxt=data['nextStart']
        if nxt!=-1 and nxt<=start:raise ValueError('Non-progressing ArcGIS pagination')
        start=nxt
        if start>10000:break
    unique={r['id']:r for r in records}
    cap.save('ons-geography-items',list(unique.values()),receipts,{'unit':'public ArcGIS item in verified ONS organisation','reportedTotal':total,'retrievedUnique':len(unique),'catalogueComplete':total==len(unique) and stable and start==-1,'stableReportedTotal':stable,'duplicateCount':len(records)-len(unique),'organisation':{k:v for k,v in (org or {}).items() if k in {'id','name','urlKey'}},'limitations':['Items include maps, services, files, documentation and old releases; not all are distinct datasets.','Public organisation search can differ from the curated geography portal group.','Search is not a transactionally frozen snapshot; stable total and unique count cannot exclude equal-count substitutions.','Created/modified timestamps do not establish data temporal extent.','Service-layer schemas and downloads are not yet fetched.']})

def main():
    p=argparse.ArgumentParser();p.add_argument('families',nargs='+',choices=['os-products','ngd','docs','ons','nomis','geography']);p.add_argument('--max-requests',type=int,default=900);args=p.parse_args()
    if not 1<=args.max_requests<=4000:p.error('request ceiling must be 1..4000')
    cap=Capture(ROOT,args.max_requests)
    funcs={'os-products':os_products,'ngd':ngd,'docs':docs,'ons':ons,'nomis':nomis,'geography':geography}
    for family in args.families:funcs[family](cap)
    print('cumulative capture attempts',len(cap.ledger['requests']),flush=True)
if __name__=='__main__':main()
