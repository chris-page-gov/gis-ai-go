#!/usr/bin/env python3
"""Build the additive OKF+ bundle and coverage from reviewable Markdown, offline."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse
from model import BASE, CONTEXT, CTX, PREFIXES, PROFILE, apply_temporal, canonical, digest, load_json, read_markdown, safe_reference
from vocabulary_usage import vocabulary_usage

ROOT=Path(__file__).resolve().parents[2]
MARKER='gis-ai-go-okf-plus-build.v1\n'

def source_path(root,relative):
    path=root/relative
    if not path.resolve().is_relative_to(root.resolve()):raise ValueError('Source escapes checkout')
    if any(p.is_symlink() for p in [path,*path.parents] if p!=root and p.is_relative_to(root)):raise ValueError('Symlink source forbidden')
    return path

def source_inputs(root):
    """Exact ordered build input inventory, also checked at generated export."""
    root=Path(root).resolve()
    paths=sorted((root/'okf-plus/records').rglob('*.md'))
    paths+=sorted((root/'okf-plus/source').glob('*.json'))
    paths+=sorted(p for p in (root/'okf-plus/profile').glob('*') if p.is_file())
    fixed={root/name for name in ('pyproject.toml','uv.lock','package.json','pnpm-lock.yaml') if (root/name).is_file()}
    fixed|={p for folder in ('schemas','vendor','evaluation') for p in (root/'okf-plus'/folder).rglob('*') if p.is_file()}
    paths+=sorted(set((root/'scripts/okf_plus').glob('*.py'))|set((root/'okf-plus').glob('*.json*'))|fixed)
    return [{'path':p.relative_to(root).as_posix(),
             'sha256':hashlib.sha256(source_path(root,p.relative_to(root)).read_bytes()).hexdigest()}
            for p in paths]

def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n')

def schema_validator(root,name):
    path=root/'okf-plus/schemas'/name
    if not path.exists():return None  # Small synthetic build fixtures have no profile tree.
    from jsonschema import Draft202012Validator
    schema=load_json(source_path(root,path.relative_to(root)).read_text())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)

def validate_record(row,path,source_cache):
    needed={'@context','@id','@type','type','title','description','nativeIdentifier','sourceFamily','resource','status','generated','assertionStatus','reviewStatus','tags','sources','temporal','update','rights','limitations','details'}
    if not needed<=row.keys():raise ValueError(f'Missing record fields in {path}: {needed-row.keys()}')
    if row['@context']!=CONTEXT or 'okf_version' in row:raise ValueError('Unknown context or non-root core version')
    if row['status'] not in ('draft','stable','deprecated') or not isinstance(row['generated'],dict) or not isinstance(row['generated'].get('by'),str):raise ValueError('Invalid OKF lifecycle/generation fields')
    if not row['@id'].startswith(BASE+'id/'):raise ValueError('Record identity outside module')
    if row['assertionStatus'] not in ('official','normalised','inferred','model-derived'):raise ValueError('Unknown assertion status')
    if not row['sources']:raise ValueError('Missing provenance')
    for key in ('@type',):
        if not isinstance(row[key],list) or not row[key]:raise ValueError('Non-empty type array required')
        for typ in row[key]:
            if typ.split(':')[0] not in PREFIXES:raise ValueError('Undefined semantic type prefix')
    for link in [row['resource']]+row['update']['releaseCatalogue']+row['update']['releaseFeed']:
        safe_reference(link)
    temporal=row['temporal']
    if temporal['status']=='not-evidenced' and (temporal['start'] is not None or temporal['end'] is not None):raise ValueError('Unknown temporal extent has invented dates')
    if temporal['status']=='source-stated':apply_temporal({},temporal['start'],temporal['end'],temporal['kind'],temporal['sourceField'])
    if row['rights']['executionAdmitted'] is not False:raise ValueError('Metadata cannot activate execution')
    for source in row['sources']:
        relative=source.get('normalisedSource')
        if not relative:continue
        parts=Path(relative).parts
        if Path(relative).is_absolute() or '..' in parts or parts[:2]!=('okf-plus','source'):raise ValueError('Unsafe source path')
        checked_path=source_path(ROOT,relative)
        if relative not in source_cache:source_cache[relative]=load_json(checked_path.read_text())
        snapshot=source_cache[relative]
        match=re.fullmatch(r'/records/([0-9]+)',source['normalisedPointer'])
        if not match:raise ValueError('Unsupported source pointer')
        item=snapshot['records'][int(match[1])]
        if digest(item)!=source['normalisedRecordSha256']:raise ValueError('Source record checksum mismatch')
        if source is row['sources'][0] and snapshot['family']!=row['sourceFamily']:raise ValueError('Source family mismatch')
        safe_reference(source['resource'])
        if source.get('evidenceKind')=='failed-metadata-request':
            evidence=item.get('metadataEvidence',{})
            if (evidence.get('status')==200 or source.get('requestStatus')!=evidence.get('status') or source['resource']!=evidence.get('url') or source.get('retrievedAt')!=evidence.get('retrievedAt') or str(item.get('id'))!=row['nativeIdentifier']):raise ValueError('Failed request evidence mismatch')
            if not any(r.get('url')==evidence.get('url') and r.get('retrievedAt')==evidence.get('retrievedAt') and r.get('status')==evidence.get('status') for r in snapshot['receipts']):raise ValueError('Failed request lacks a matching receipt')
            if any(k in source for k in ('responseSha256','sourcePointer')):raise ValueError('Failed request cannot claim response binding')
            continue
        if source.get('evidenceKind')=='rendered-public-catalogue':
            obs=item.get('sourceObservation',{})
            if obs.get('status')!='browser-observed' or source.get('observation')!=obs or source['resource']!=obs['sourceUrl'] or source['observedOn']!=obs['observedOn'] or str(item.get('id'))!=row['nativeIdentifier']:raise ValueError('Rendered observation mismatch')
            if any(k in source for k in ('responseSha256','retrievedAt')):raise ValueError('Rendered observation cannot claim HTTP binding')
            continue
        matched=next((r for r in snapshot['receipts'] if r.get('sha256')==source['responseSha256'] and r['url']==source['resource'] and r['retrievedAt']==source['retrievedAt'] and r['status']==200),None)
        if not matched:raise ValueError('Provenance URL, timestamp and checksum must match one capture receipt')
        safe_reference(source['resource'])
        if str(item.get('id',item.get('url','')))!=row['nativeIdentifier']:raise ValueError('Source native identity mismatch')
        locator_path='okf-plus/source/locator-index.json'
        if locator_path not in source_cache:source_cache[locator_path]=load_json(source_path(ROOT,locator_path).read_text())
        locator=source_cache[locator_path]['families'].get(snapshot['family'],{}).get(row['nativeIdentifier'])
        if not locator or any(source[a]!=locator[b] for a,b in [('resource','url'),('retrievedAt','retrievedAt'),('responseSha256','sha256'),('sourcePointer','pointer'),('sourcePointerStatus','status')]):raise ValueError('Source locator mismatch')
    # Validate all prefixed properties rather than permitting silent dropped terms.
    def walk(value):
        if isinstance(value,dict):
            if value.get('@type')=='@json':return
            if value.get('@type')=='xsd:date':date.fromisoformat(value['@value'])
            if value.get('@type')=='xsd:dateTime':
                parsed=datetime.fromisoformat(value['@value'].replace('Z','+00:00'))
                if parsed.tzinfo is None:raise ValueError('Date-time requires timezone')
            for key,child in value.items():
                if ':' in key and not key.startswith(('https:','http:')) and key.split(':')[0] not in PREFIXES:raise ValueError('Undefined predicate prefix '+key)
                if key not in ('details','sources','temporal','update','rights','coverage','assertions','limitations','provenance','schemaEvidence'):walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)
    walk(row)

def build(root,output,revision):
    """Validate a staged build before replacing the previous generated artefact."""
    root=root.resolve();output=output.resolve()
    if output==root or output==root/'okf-plus' or output.is_relative_to(root/'okf-plus'):raise ValueError('Build cannot overwrite sources')
    if output.exists() and (not (output/'.okf-plus-generated').is_file() or (output/'.okf-plus-generated').read_text()!=MARKER):raise ValueError('Refusing to replace an unmarked output')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.okf-plus-build-',dir=output.parent) as directory:
        stage=Path(directory)/'staged';previous=Path(directory)/'previous'
        coverage=_build_into(root,stage,revision)
        if output.exists():output.rename(previous)
        try:stage.rename(output)
        except BaseException:
            if previous.exists():previous.rename(output)
            raise
        return coverage

def _build_into(root,output,revision):
    global ROOT
    ROOT=root
    if not re.fullmatch('[0-9a-f]{40}',revision):raise ValueError('A full Git revision is required')
    output=output.resolve()
    if output==root or output==root/'okf-plus' or output.is_relative_to(root/'okf-plus'):raise ValueError('Build cannot overwrite sources')
    if output.exists():
        marker=output/'.okf-plus-generated'
        if not marker.is_file() or marker.read_text()!=MARKER:raise ValueError('Refusing to replace an unmarked output')
        shutil.rmtree(output)
    output.mkdir(parents=True);(output/'.okf-plus-generated').write_text(MARKER)
    records=[];identities=set();source_cache={};search=[]
    record_check=schema_validator(root,'record.schema.json')
    snapshot_check=schema_validator(root,'source-snapshot.schema.json')
    for path in sorted((root/'okf-plus/records').rglob('*.md')):
        source_path(root,path.relative_to(root))
        row,body=read_markdown(path);validate_record(row,path,source_cache)
        if record_check:record_check.validate(row)
        if row['@id'] in identities:raise ValueError('Duplicate semantic identity')
        identities.add(row['@id']);records.append(row)
        route=path.relative_to(root/'okf-plus').as_posix()
        projected={'id':row['@id'],'title':row['title'],'description':row['description'],'type':row['type'],'sourceFamily':row['sourceFamily'],'nativeIdentifier':row['nativeIdentifier'],'sources':row['sources'],'temporal':row['temporal'],'update':row['update'],'details':row['details'],'tags':row['tags'],'text':body,'resource':row['resource'],'rights':row['rights'],'limitations':row['limitations'],'schemaEvidence':row.get('schemaEvidence',{}),'route':route,'assertionStatus':row['assertionStatus'],'reviewStatus':row['reviewStatus'],'status':row['status']}
        search.append(projected)
    if not records:raise ValueError('No records')
    for path in sorted((root/'okf-plus/source').glob('*.json')):
        source_path(root,path.relative_to(root))
        source_cache.setdefault(path.relative_to(root).as_posix(),load_json(path.read_text()))
    context_path=root/'okf-plus/context.jsonld'
    if context_path.exists() and load_json(context_path.read_text())!={'@context':CTX}:raise ValueError('Authored context differs from producer contract')
    inputs=source_inputs(root)
    input_digest=digest(inputs)
    standards_path=root/'okf-plus/profile/standards.json'
    standards=load_json(source_path(root,standards_path.relative_to(root)).read_text()) if standards_path.exists() else {'standards':[]}
    vocabulary=vocabulary_usage(records,standards,revision,input_digest)
    snapshots=[v for v in source_cache.values() if v.get('schema')=='okf-plus-source-snapshot.v1']
    if snapshot_check:
        for snapshot in snapshots:snapshot_check.validate(snapshot)
    coverage={'schema':'gis-ai-go.okf-plus-coverage.v1','revision':revision,'inputDigest':input_digest,'recordCount':len(records),'globalCompleteness':'not-established','byFamily':dict(sorted(Counter(r['sourceFamily'] for r in records).items())),'byType':dict(sorted(Counter(r['type'] for r in records).items())),'catalogues':[{**s['coverage'],'family':s['family'],'retrievedAt':sorted({r['retrievedAt'] for r in s['receipts']}),'failedRequests':sum(r['status']!=200 for r in s['receipts'])} for s in snapshots],
        'temporalEvidence':dict(Counter(r['temporal']['status'] for r in records)),
        'updateFrequencyEvidence':dict(Counter(r['update']['frequency']['status'] for r in records)),
        'evidenceByRecordType':{kind:{'records':sum(r['type']==kind for r in records),'temporal':dict(Counter(r['temporal']['status'] for r in records if r['type']==kind)),'frequency':dict(Counter(r['update']['frequency']['status'] for r in records if r['type']==kind))} for kind in sorted({r['type'] for r in records})},
        'recordsWithReleaseCatalogue':sum(bool(r['update']['releaseCatalogue']) for r in records),
        'recordsWithReleaseFeed':sum(bool(r['update']['releaseFeed']) for r in records),
        'ngdFieldNodes':sum(len(r.get('okfp:field',[])) for r in records),
        'schemaFindings':[{'record':r['@id'],'kind':kind,'requiredUndeclared':e['requiredUndeclared']} for r in records for kind,e in r.get('schemaEvidence',{}).items() if e['requiredUndeclared']],
        'limits':['Counts are catalogue representations at separate grains, not unique OS/ONS products.','No finite concept inventory proves all geospatial concepts.','Frequency and reference-period evidence have separate denominators; not-evidenced is not non-compliance.','Build validates retained metadata and provenance, not statistical accuracy, dataset rights or live connector admission.']}
    write_json(output/'vocabulary-usage.json',vocabulary)
    write_json(output/'context.jsonld',{'@context':CTX})
    write_json(output/'okf-bundle.jsonld',{'@context':CTX,'@id':BASE+'bundle','@type':'dcat:Catalog','dcterms:title':'OS and ONS geospatial OKF+','@graph':records})
    write_json(output/'okf-bundle.json',{'schema':'gis-ai-go.okf-plus-bundle.v1','okfVersion':'0.2','profile':PROFILE,'profileStatus':'candidate-pending-consumer-acceptance','revision':revision,'inputDigest':input_digest,'recordCount':len(records),'records':records})
    index={'schema':'gis-ai-go.okf-plus-search-index.v1','revision':revision,'inputDigest':input_digest,'records':search}
    index_check=schema_validator(root,'search-index.schema.json')
    if index_check:index_check.validate(index)
    write_json(output/'search-index.json',index)
    write_json(output/'coverage.json',coverage)
    write_json(output/'source-lock.json',{'schema':'gis-ai-go.okf-plus-source-lock.v1','revision':revision,'inputs':inputs,'sha256':input_digest})
    write_json(output/'okf.json',{'okf_version':'0.2','title':'OS and ONS geospatial OKF+','description':'Metadata/schema discovery with provenance, date ranges, update routes and measured gaps.','profile':PROFILE,'profile_status':'candidate','entrypoints':{'bundle':'okf-bundle.json','jsonld':'okf-bundle.jsonld','search':'search-index.json','coverage':'coverage.json','vocabularyUsage':'vocabulary-usage.json'},'limitations':['Installed Ask OKF currently allowlists DWP only; this descriptor does not register the new bundle.']})
    lines=['# OS and ONS OKF+ coverage','',f'Revision: `{revision}`. Input digest: `{input_digest}`.','',f'{len(records):,} Markdown/YAML-LD records. Global completeness is **not established**.','', '| Source family | Unit | Retained | Reported denominator | Catalogue traversal |','| --- | --- | ---: | ---: | --- |']
    for c in coverage['catalogues']:lines.append(f"| {c['family']} | {c['unit']} | {c['retrievedUnique']} | {c.get('reportedTotal','unknown')} | {'complete within stated lane' if c.get('catalogueComplete') else 'partial'} |")
    lines+=['','Actual predicate, class, object and datatype references are counted separately in `vocabulary-usage.json`. Namespace declarations and opaque JSON are excluded; unused terms stay visible. Usage is not semantic certification.']
    lines+=['','Temporal extent and update-cadence evidence are counted independently in `coverage.json`. A release date, metadata change timestamp or date in a title does not establish the period covered by observations.','',f"Schema field nodes: {coverage['ngdFieldNodes']:,}. Schema contradictions: {len(coverage['schemaFindings'])}.",'','## Limits','']+['- '+s for s in coverage['limits']]
    (output/'coverage.md').write_text('\n'.join(lines)+'\n')
    checksums={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.iterdir()) if p.is_file()}
    write_json(output/'checksums.json',checksums)
    return coverage

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'artifacts/okf-plus/bundle');p.add_argument('--revision');args=p.parse_args()
    revision=args.revision or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    coverage=build(ROOT,args.output,revision)
    print('Built',coverage['recordCount'],'OKF+ records;',coverage['ngdFieldNodes'],'NGD field nodes;',len(coverage['schemaFindings']),'schema findings.')
if __name__=='__main__':main()
