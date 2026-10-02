#!/usr/bin/env python3
"""Import frozen factual metadata as reviewable Markdown/YAML-LD sources."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
from model import BASE, CONTEXT, CTX, apply_frequency, apply_temporal, compact_time_metadata, digest, file_key, markdown_text, record, ref, write_markdown, load_json, safe_reference
from harvest import clean_text
ROOT=Path(__file__).resolve().parents[2]
RELEASE_CALENDAR='https://www.ons.gov.uk/releasecalendar'
RELEASE_RSS=RELEASE_CALENDAR+'?rss&highlight=true&limit=10&page=1&release-type=type-published&sort=date-newest'

def text_value(value):
    if isinstance(value,str):return clean_text(value)
    if isinstance(value,list):return '; '.join(text_value(v) for v in value)
    if isinstance(value,dict):return text_value(value.get('value',value.get('#text',value.get('text',''))))
    return str(value or '')

def receipt_match(snapshot,evidence,successful=True):
    """Bind one observation by its full tuple, never by an unrelated fallback."""
    fields=('url','retrievedAt','status')+(('sha256',) if successful else ())
    if not isinstance(evidence,dict) or any(k not in evidence for k in fields):
        raise ValueError('Incomplete explicit capture evidence')
    if successful and evidence['status']!=200:raise ValueError('Successful capture required')
    matches=[r for r in snapshot['receipts'] if all(r.get(k)==evidence[k] for k in fields)]
    if not matches:raise ValueError('Explicit evidence does not match a capture receipt')
    safe_reference(evidence['url'])
    return matches[0]


def captured_bytes(root,receipt):
    checksum=receipt.get('sha256','')
    if receipt.get('status')!=200 or not re.fullmatch('[0-9a-f]{64}',checksum):
        raise ValueError('Successful receipt requires a SHA-256 digest')
    safe_reference(receipt['url'])
    directory=root/'artifacts/okf-plus/capture'
    path=directory/(checksum+'.body')
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Capture evidence escapes the checkout')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=checksum:raise ValueError('Raw source integrity mismatch')
    if 'bytes' in receipt and receipt['bytes']!=len(raw):raise ValueError('Raw source byte count mismatch')
    return raw


def pointer_value(document,pointer):
    if not isinstance(pointer,str) or (pointer and not pointer.startswith('/')):
        raise ValueError('Invalid JSON pointer')
    value=document
    for part in pointer.split('/')[1:]:
        if re.search(r'~(?![01])',part):raise ValueError('Invalid JSON pointer escape')
        part=part.replace('~1','/').replace('~0','~')
        if isinstance(value,list):
            if not re.fullmatch('0|[1-9][0-9]*',part):raise ValueError('Invalid JSON pointer index')
            index=int(part)
            if index>=len(value):raise ValueError('JSON pointer is outside the response')
            value=value[index]
        elif isinstance(value,dict) and part in value:value=value[part]
        else:raise ValueError('JSON pointer does not resolve')
    return value


def original_locators(root,snapshot):
    """Verify captured bytes and locate each retained native record or document.

    Whole-document bindings need an explicit response digest/receipt or a
    reviewed parser that proves the native identifier occurs in that document.
    Failed requests and browser observations never inherit successful receipts.
    """
    responses=[];discovered={};result={}
    for receipt in snapshot['receipts']:
        if receipt['status']!=200:continue
        raw=captured_bytes(root,receipt)
        try:data=load_json(raw.decode('utf-8'))
        except (ValueError,UnicodeError):data=None
        responses.append((receipt,raw,data))
        prefix='';rows=[]
        if isinstance(data,list):rows=data
        elif isinstance(data,dict):
            if isinstance(data.get('hits'),dict):rows=data['hits'].get('hits',[]);prefix='/hits/hits'
            elif 'structure' in data:
                rows=data['structure'].get('keyfamilies',{}).get('keyfamily',[]);prefix='/structure/keyfamilies/keyfamily'
            else:
                key=next((k for k in ('items','collections','results') if isinstance(data.get(k),list)),None)
                if key:rows=data[key];prefix='/'+key
                elif 'id' in data:rows=[data];prefix=None
        if isinstance(rows,dict):rows=[rows]
        for i,item in enumerate(rows):
            if not isinstance(item,dict):continue
            nid=item.get('id');sub=''
            if isinstance(item.get('_source'),dict):
                nid=item['_source'].get('uuid') or item['_source'].get('metadataIdentifier')
                if nid is None:nid=item.get('_id')
                else:sub='/_source'
            if nid is not None:
                pointer=(prefix+'/'+str(i)+sub) if prefix is not None else ''
                # A singleton SDMX object has no array position.
                if isinstance(data,dict) and prefix=='/structure/keyfamilies/keyfamily' and isinstance(data['structure']['keyfamilies']['keyfamily'],dict):pointer=prefix
                pointer_value(data,pointer)
                discovered.setdefault(str(nid),[]).append((receipt,pointer))
        if snapshot['family'].endswith('-documentation') and data is None:
            for url in re.findall(r'^- \[.*?\]\((https://[^)]+)\)',raw.decode('utf-8'),re.M):
                discovered.setdefault(url,[]).append((receipt,None))
        if snapshot['family']=='os-product-search' and data is None:
            from os_enrichment import product_state
            for item in product_state(raw.decode('utf-8'))['results']:
                discovered.setdefault(str(item['id']),[]).append((receipt,None))
    seen=set()
    for item in snapshot['records']:
        nid=native(item)
        if not nid or nid in seen:raise ValueError('Missing or duplicate native source identity')
        seen.add(nid)
        if item.get('sourceObservation',{}).get('status')=='browser-observed':continue
        explicit=item.get('sourceEvidence')
        metadata=item.get('metadataEvidence')
        if explicit is not None:
            receipt=receipt_match(snapshot,explicit)
            data=next(data for r,_,data in responses if r is receipt)
            pointed=pointer_value(data,explicit.get('pointer'))
            field=item.get('nativeIdentityField','id')
            if field not in ('id','uri','name','/links/self/id') or not isinstance(pointed,dict):
                raise ValueError('Unadmitted source native identity field')
            identity=pointer_value(pointed,field) if field.startswith('/') else pointed.get(field,'')
            if str(identity)!=nid:
                raise ValueError('Explicit source pointer native identity mismatch')
            result[nid]=(receipt,explicit['pointer'])
        elif metadata is not None:
            receipt=receipt_match(snapshot,metadata,successful=metadata.get('status')==200)
            if metadata.get('status')!=200:continue
            result[nid]=(receipt,None)
        elif item.get('sourceSha256') is not None:
            matches=[r for r,_,_ in responses if r['sha256']==item['sourceSha256'] and r['url']==item.get('url')]
            if len(matches)!=1:raise ValueError('Document digest requires one matching source URL')
            result[nid]=(matches[0],None)
        else:
            matches=discovered.get(nid,[])
            if not matches:raise ValueError('No captured response proves this native source identity')
            # Prefer a detail response to the catalogue entry; both must have
            # demonstrated the same exact native identity before selection.
            result[nid]=next((m for m in reversed(matches) if m[1]==''),matches[0])
    return result

def native(record):return str(record.get('id',record.get('url','')))
def source_evidence(snapshot,path,index,item,locators):
    common={'normalisedSource':path.as_posix(),'normalisedPointer':'/records/'+str(index),'normalisedRecordSha256':digest(item)}
    if item.get('sourceObservation',{}).get('status')=='browser-observed':
        obs=item['sourceObservation']
        safe_reference(obs['sourceUrl'])
        return {'resource':obs['sourceUrl'],'evidenceKind':'rendered-public-catalogue','observedOn':obs['observedOn'],'observation':obs,**common,'sourcePointerStatus':'rendered-reference-no-http-binding'}
    metadata=item.get('metadataEvidence')
    if metadata is not None and metadata.get('status')!=200:
        receipt=receipt_match(snapshot,metadata,successful=False)
        return {'resource':receipt['url'],'retrievedAt':receipt['retrievedAt'],'requestStatus':receipt['status'],'evidenceKind':'failed-metadata-request',**common,'sourcePointerStatus':'request-failed-no-response-binding'}
    locator=locators.get(native(item))
    if not locator:raise ValueError('Missing frozen source locator; run the explicit locator-freeze stage')
    match=next((r for r in snapshot['receipts'] if r.get('sha256')==locator['sha256'] and r['url']==locator['url'] and r['retrievedAt']==locator['retrievedAt'] and r['status']==200),None)
    if not match:raise ValueError('Frozen source locator does not match a capture receipt')
    safe_reference(locator['url'])
    return {'resource':locator['url'],'retrievedAt':locator['retrievedAt'],'responseSha256':locator['sha256'],'sourcePointer':locator['pointer'],**common,'evidenceKind':'captured-public-metadata','sourcePointerStatus':locator['status']}

def apply_native_bounds(row,bounds,source_field):
    if bounds.get('status')!='known-option-extrema':return
    row['temporal']={'status':'normalised-source-options','kind':'available-native-period-options','start':bounds['minimumNative'],'end':bounds['maximumNative'],'sourceField':source_field,'note':'Extrema of the complete published native period-code list; no continuity or populated observation cells are inferred.','precision':bounds.get('granularity'),'derivation':bounds['comparisonRule']}
    row['okfp:nativeTemporalBounds']={'@value':bounds,'@type':'@json'}


def map_record(family,item,source):
    nid=native(item)
    title=text_value(item.get('title',item.get('label',item.get('name',nid)))) or nid
    description=text_value(item.get('description',item.get('snippet','')))
    if family=='os-open-products':
        url=item['url'];row=record(family,nid,title,description,url,source,details=item)
        row['update']['releaseVersion']=item.get('version')
        row['update']['releaseCatalogue']=[url,item.get('documentationUrl','')]
        row['tags']=item.get('categories',[])+item.get('dataStructures',[])
        row['rights']['describedData']='OpenData catalogue entry; consult product attribution and licence, including partner rights.'
    elif family=='os-ngd-collections':
        url='https://api.os.uk/features/ngd/ofa/v1/collections/'+nid
        row=record(family,nid,title,description,url,source,'Collection',item)
        row['tags']=['OS NGD',nid.split('-')[0],'schema','queryables']
        interval=item.get('extent',{}).get('temporal',{}).get('interval',[])
        if interval:apply_temporal(row,interval[0][0],interval[0][1],'advertised-collection-temporal-extent','extent.temporal.interval[0]')
        row['update']['releaseCatalogue']=['https://docs.os.uk/osngd/getting-started/os-ngd-release-notes']
        row['schemaEvidence']={k:{'resource':v['url'],'responseSha256':v['sha256'],'requiredUndeclared':v['requiredUndeclared']} for k,v in item['schemas'].items()}
        row['dcterms:conformsTo']=[ref('http://www.opengis.net/spec/ogcapi-features-1/1.0'),ref(item.get('storageCrs','http://www.opengis.net/def/crs/EPSG/0/27700'))]
        # Field definitions are addressable nodes; controlled enum values stay native.
        fields=[]
        for name,definition in item['schemas'].get('schema',{}).get('properties',{}).items():
            f={'@id':row['@id']+'/field/'+quote(name,safe=''),'@type':'rdf:Property','dcterms:identifier':name,'rdfs:label':name,'okfp:schemaDefinition':{'@value':definition,'@type':'@json'},'okfp:queryable':name in item['schemas'].get('queryables',{}).get('properties',{}),'prov:wasDerivedFrom':ref(item['schemas']['schema']['url'])}
            fields.append(f)
        row['okfp:field']=fields
        row['rights']['describedData']='OS NGD protected data: licence and entitlement required; public schemas do not grant feature access or AI-hosting rights.'
    elif family.endswith('-documentation'):
        url=item['url'];row=record(family,nid,title,'Documentation reference listed by the official navigation index.',url,source,'Documentation',item)
        row['tags']=['documentation']
        for tag,pattern in [('release-notes','release'),('controlled-vocabulary','code-list'),('schema','data-structure'),('FAQ','faq'),('specification','technical-specification'),('retirement','withdraw')]:
            if pattern in url.lower():row['tags'].append(tag)
        row['limitations']=['The navigation index was captured; target-page availability and full content are separate checks.']
    elif family=='ons-datasets':
        url=item.get('links',{}).get('self',{}).get('href','https://api.beta.ons.gov.uk/v1/datasets/'+nid)
        row=record(family,nid,title,description,url,source,details=item)
        row['tags']=item.get('keywords',[])
        apply_frequency(row,item.get('release_frequency'),'release_frequency')
        row['update'].update(releaseCatalogue=[RELEASE_CALENDAR],releaseFeed=[RELEASE_RSS],nextRelease=item.get('next_release'),metadataModified=item.get('last_updated'))
        row['rights']['describedData']='ONS published-data terms apply; dataset-specific notices and third-party rights must be checked.'
        row['qb:structure']=ref(url+'/editions')
    elif family=='ons-nomis-datasets':
        url='https://www.nomisweb.co.uk/api/v01/dataset/'+nid+'/def.sdmx.json'
        row=record(family,nid,title,description or 'Nomis dataset definition with native SDMX components.',url,source,details=item)
        ann=item.get('annotations',{})
        row['tags']=[v.strip() for v in ann.get('Keywords','').split(',') if v.strip()]
        row['update'].update(releaseCatalogue=['https://www.nomisweb.co.uk/releasecalendar.asp'],metadataModified=ann.get('LastUpdated'))
        row['limitations']=['FREQ denotes statistical observation frequency; it does not establish release cadence.','FirstReleased and LastUpdated describe publication history, not the observation date range.']
        dims=item.get('components',{}).get('dimension',[])
        row['qb:structure']={'@id':row['@id']+'/structure','@type':'qb:DataStructureDefinition','qb:component':[{'@type':'qb:ComponentSpecification','qb:dimension':{'@id':row['@id']+'/dimension/'+quote(d['conceptref'],safe=''),'@type':'qb:DimensionProperty','rdfs:label':d['conceptref'],'qb:codeList':ref('https://www.nomisweb.co.uk/api/v01/codelist/'+d['codelist']+'/def.sdmx.json')} } for d in dims if 'conceptref' in d and 'codelist' in d]}
    elif family=='ons-geography-items':
        url='https://geoportal.statistics.gov.uk/items/'+nid
        row=record(family,nid,title,description,url,source,details=item)
        row['tags']=item.get('tags',[])+[item['type']]
        row['update']['releaseCatalogue']=['https://geoportal.statistics.gov.uk/']
        row['update']['metadataModified']=datetime.fromtimestamp(item['modified']/1000,timezone.utc).isoformat().replace('+00:00','Z') if item.get('modified') else None
        row['rights']['describedData']=clean_text(item.get('licenseInfo')) or 'Consult the portal item licence; no licence inferred.'
        row['limitations']=['A date in an item title is not automatically the observation/reference range.','Portal items can be different representations or vintages of one product.']
        row['dcterms:publisher']=ref('https://www.ons.gov.uk/')
    elif family in ('os-api-contracts','os-lifecycle-guides','osngd-documentation-pages','os-download-guide-pages'):
        url=item['url'];row=record(family,nid,title,'Captured official documentation '+('with extracted API contract fragments.' if family=='os-api-contracts' else 'with structural metadata for schema, vocabulary, lifecycle and update discovery.'),url,source,'Specification' if item.get('contracts') else 'Documentation',item)
        row['tags']=['specification','documentation']
        if 'structure' in item:row['limitations']=['The public projection retains headings, references and recognised table structure. Original prose, examples and instructions are not republished; extraction omissions are counted explicitly.','A captured guide does not establish complete vocabulary coverage or API conformance.']
    elif family=='ons-latest-versions':
        meta=item.get('metadata',{});url=item.get('versionUrl',source['resource'])
        title=meta.get('title') or ('ONS version metadata: '+nid)
        row=record(family,nid,title,meta.get('description') or 'Current advertised ONS edition/version metadata and native time options.',url,source,'Dataset',item)
        row['update'].update(releaseCatalogue=[RELEASE_CALENDAR],releaseFeed=[RELEASE_RSS],releaseVersion=item.get('version'),metadataModified=meta.get('last_updated'),nextRelease=meta.get('next_release'))
        apply_frequency(row,meta.get('release_frequency'),'release_frequency')
        apply_native_bounds(row,item.get('temporal',{}).get('bounds',{}),'temporal.options')
    elif family=='ons-nomis-time-options':
        url=item.get('metadataEvidence',{}).get('url',source['resource']);row=record(family,nid,'Nomis time options: '+nid,'Native time code list and selected revision metadata; no observations.',url,source,'Dataset',compact_time_metadata(item))
        apply_native_bounds(row,item.get('bounds',{}),'codes')
        row['update']['releaseCatalogue']=['https://www.nomisweb.co.uk/releasecalendar.asp']
    elif family.startswith('ons-website-') or family.startswith('ons-releases-'):
        url=item['resource'];is_release=family.startswith('ons-releases-')
        row=record(family,nid,title,text_value(item.get('meta_description',item.get('summary',''))) or ('Official release catalogue entry.' if is_release else 'ONS website catalogue metadata.'),url,source,'Documentation' if is_release else 'Dataset',item)
        row['tags']=item.get('keywords',[])+[item.get('type','release')]
        row['update'].update(releaseCatalogue=[RELEASE_CALENDAR],releaseFeed=[RELEASE_RSS],releaseVersion=item.get('edition'))
        row['limitations']=['Website and API representations are retained separately; matching titles do not prove equivalence.','Release dates do not establish the period covered by statistical observations.']
    elif family in ('ons-population-types','ons-code-lists'):
        row=record(family,nid,title,description or 'Native ONS '+family.removeprefix('ons-')+' catalogue entry.',item['resource'],source,'Concept',item)
        row['okfp:machineImported']=True
        row['skos:prefLabel']={'@value':title,'@language':'en'}
        row['limitations']=['A catalogue entry does not enumerate all subordinate variables, categories or code-list editions.']
    elif family in ('os-product-search','os-gemini-metadata'):
        url=item.get('url',source['resource']);row=record(family,nid,title,description or 'Official product or metadata catalogue entry.',url,source,'Dataset',item)
        row['limitations']=['Catalogue representations are not deduplicated into assumed identical datasets.','Product availability does not establish licensed data access or downstream hosting rights.']
    else:
        url=item.get('url',source['resource']);row=record(family,nid,title,description or 'Official source metadata.',url,source,details=item)
    row['update']['releaseCatalogue']=[u for u in row['update']['releaseCatalogue'] if u]
    # Record body avoids raw HTML and executable links; source structure stays JSON.
    row['description']=row['description'][:3000]
    return row

def body_for(row):
    temporal=row['temporal'];freq=row['update']['frequency']
    lines=['# '+row['title'],'',row['description'],'',f"Native identifier: `{row['nativeIdentifier']}`.",'',f"Source family: `{row['sourceFamily']}`. Assertion: normalised metadata; independent human review is not recorded.",'',f"[Official source]({row['resource']})",'',f"Update cadence: {freq['label'] or 'not evidenced in captured metadata'}.",f"Temporal evidence: {temporal['status']} ({temporal['kind']}); start {temporal['start'] or 'not stated'}, end {temporal['end'] or 'not stated'}.",temporal['note'],'']
    for url in row['update']['releaseCatalogue']:lines.append('[Release catalogue or change-discovery route]('+url+')')
    for url in row['update']['releaseFeed']:lines.append('[Recent release feed]('+url+')')
    if row['limitations']:lines.extend(['','## Evidence limits','']+['- '+s for s in row['limitations']])
    lines+=['','The front matter retains source receipts, rights, native metadata and schema facts. Discovery does not authorise data access.']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--families',nargs='*');parser.add_argument('--check',action='store_true',help='Verify imported sources without changing any file');args=parser.parse_args()
    count=0;drift=[]
    supplements={}
    for family in ('ons-latest-versions','ons-nomis-time-options'):
        path=ROOT/'okf-plus/source'/(family+'.json')
        if path.exists():
            snapshot=json.loads(path.read_text());locators=json.loads((ROOT/'okf-plus/source/locator-index.json').read_text())['families'].get(family,{})
            supplements[family]={native(item):(item,source_evidence(snapshot,path.relative_to(ROOT),i,item,locators)) for i,item in enumerate(snapshot['records'])}
    for path in sorted((ROOT/'okf-plus/source').glob('*.json')):
        snapshot=json.loads(path.read_text())
        if snapshot.get('schema')!='okf-plus-source-snapshot.v1':continue
        family=snapshot['family']
        if args.families and family not in args.families:continue
        locators=json.loads((ROOT/'okf-plus/source/locator-index.json').read_text())['families'].get(family,{})
        target=ROOT/'okf-plus/records'/family;expected=set()
        for index,item in enumerate(snapshot['records']):
            source=source_evidence(snapshot,path.relative_to(ROOT),index,item,locators)
            row=map_record(family,item,source)
            extra_family={'ons-datasets':'ons-latest-versions','ons-nomis-datasets':'ons-nomis-time-options'}.get(family)
            if extra_family and row['nativeIdentifier'] in supplements.get(extra_family,{}):
                extra,evidence=supplements[extra_family][row['nativeIdentifier']]
                row['sources'].append(evidence)
                row['details']['timeMetadata']=compact_time_metadata(extra) if extra_family=='ons-nomis-time-options' else extra
                bounds=extra.get('temporal',{}).get('bounds',{}) if extra_family=='ons-latest-versions' else extra.get('bounds',{})
                apply_native_bounds(row,bounds,'timeMetadata.temporal.options' if extra_family=='ons-latest-versions' else 'timeMetadata.codes')
                row['limitations'].append('Time-option extrema describe available native codes; continuity and populated observation cells have not been established.')
            output=target/(file_key(row['nativeIdentifier'])+'.md');expected.add(output)
            if args.check:
                if not output.is_file() or output.read_text()!=markdown_text(row,body_for(row)):drift.append(output.relative_to(ROOT).as_posix())
            else:write_markdown(output,row,body_for(row))
            count+=1
        # Explicit importer owns only this family directory, never authored concepts.
        if target.exists():
            for stale in target.glob('*.md'):
                if stale not in expected:
                    if args.check:drift.append(stale.relative_to(ROOT).as_posix())
                    else:stale.unlink()
    context=ROOT/'okf-plus/context.jsonld';expected_context=json.dumps({'@context':CTX},indent=2,sort_keys=True)+'\n'
    if args.check:
        if not context.is_file() or context.read_text()!=expected_context:drift.append('okf-plus/context.jsonld')
        if drift:raise SystemExit('Imported source drift ('+str(len(drift))+'): '+', '.join(drift[:20]))
    else:context.write_text(expected_context)
    print('Verified' if args.check else 'Imported',count,'Markdown/YAML-LD metadata sources.')
if __name__=='__main__':main()
