import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from jsonschema import Draft202012Validator,ValidationError
from scripts.okf_plus.label_origin import validate_label_origin,label_assertions,title_origin,pointed_state,qualify_title_form
from scripts.okf_plus import classification_release as release
from scripts.okf_plus.model import read_markdown
from tests.test_okf_plus_classification_release import payload
HERE=Path(__file__).resolve().parents[1]/'okf-plus/schemas'
def origin_schema():
 return json.loads((HERE/'classification-browser.schema.json').read_text())['properties']['schemes']['items']['properties']['entries']['items']['properties']['labelOrigin']
SOURCE={'synthetic-source':{'id':'synthetic-source','title':'Fictional source','url':'https://example.invalid/list','sha256':'1'*64}}

def entry(native=None,pointer='/native/description/value',state='absent',kind='project-display-fallback',label='Label not supplied · X1'):
    return {'id':'fictional-row','code':'X1','label':label,'definition':None,'level':None,'parentCode':None,
            'aliases':[],'nativeSearchForms':[],'labelLanguage':None,'sourceId':'synthetic-source','sourceLocator':'/codes/0',
            'native':{'description':{}}if native is None else native,'labelOrigin':{'kind':kind,'sourceId':'synthetic-source','sourceLocator':'/codes/0','nativePointer':pointer,'nativeState':state,'languagePointer':None,'displayLanguage':'en-GB'if kind=='project-display-fallback'else None}}

class LabelTests(unittest.TestCase):
 def test_four_missing_shapes_stay_distinct(self):
  cases=[({},'/native/description','absent'),({'description':None},'/native/description','null'),({'description':{}},'/native/description/value','absent'),({'description':{'value':None}},'/native/description/value','null')]
  observed=[]
  for native,pointer,state in cases:
   e=entry(native,pointer,state);before=copy.deepcopy(e);r=validate_label_origin(e,SOURCE)
   self.assertEqual(label_assertions(e,SOURCE,True),{});self.assertEqual(e,before);observed.append((r['nativePointer'],r['nativeState']))
  self.assertEqual(len(set(observed)),4)
 def test_empty_is_source_label_not_fallback(self):
  e=entry({'description':{'value':''}},state='empty-string',kind='source-native',label='')
  self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':''})
 def test_whitespace_preserved(self):
  e=entry({'description':{'value':' '}},state='string',kind='source-native',label=' ')
  self.assertEqual(label_assertions(e,SOURCE,False),{'rdfs:label':' '})
 def test_native_ordinary_and_language(self):
  e=entry({'description':{'value':'Fictional category','lang':'cy'}},state='string',kind='source-native',label='Fictional category')
  e['labelLanguage']='cy';e['labelOrigin'].update(languagePointer='/native/description/lang',displayLanguage='cy')
  self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':{'@value':'Fictional category','@language':'cy'}})
 def test_native_language_and_project_language_separate(self):
  e=entry({'description':{'lang':'cy'}});e['labelOrigin']['languagePointer']='/native/description/lang'
  r=validate_label_origin(e,SOURCE);self.assertEqual(r['nativeLanguage'],{'state':'string','value':'cy'});self.assertEqual(r['displayLanguage'],'en-GB');self.assertEqual(label_assertions(e,SOURCE,True),{})
 def test_legacy_without_metadata_unchanged(self):
  for coded in (True,False):
   for label,language in [('ordinary',None),('',None),('label','cy')]:
    e=entry(label=label);e.pop('labelOrigin');e['labelLanguage']=language
    self.assertIsNone(validate_label_origin(e,SOURCE));self.assertIsNone(title_origin(e,SOURCE))
    self.assertEqual(label_assertions(e,SOURCE,coded),{('skos:prefLabel'if coded else'rdfs:label'):({'@value':label,'@language':language}if language else label)})
 def test_source_mismatch_refused(self):
  e=entry();e['labelOrigin']['sourceId']='other'
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_locator_mismatch_refused(self):
  e=entry();e['labelOrigin']['sourceLocator']='/codes/1'
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_declared_state_must_match(self):
  e=entry();e['labelOrigin']['nativeState']='null'
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_existing_native_value_cannot_be_fallback(self):
  e=entry({'description':{'value':'native'}})
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_source_string_cannot_be_changed(self):
  e=entry({'description':{'value':'native'}},state='string',kind='source-native',label='replacement')
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_native_language_cannot_be_applied_to_fallback(self):
  e=entry();e['labelLanguage']='en'
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_label_alias_promotion_refused(self):
  e=entry();e['aliases']=[{'text':e['label'],'kind':'source-alternative-label','authority':'source-stated','sourceId':'synthetic-source'}]
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_native_form_promotion_refused(self):
  e=entry();e['nativeSearchForms']=[{'text':e['label']}]
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_other_alias_not_removed(self):
  e=entry();e['aliases']=[{'text':'A separate retained label'}];before=copy.deepcopy(e)
  self.assertEqual(label_assertions(e,SOURCE,True),{});self.assertEqual(e,before)
 def test_null_code_and_display_title_remain(self):
  e=entry(label='Label not supplied · source row 1');e['code']=None
  self.assertEqual(label_assertions(e,SOURCE,False),{});self.assertIsNone(e['code']);self.assertEqual(title_origin(e,SOURCE),'project-display-fallback')
 def test_parent_must_resolve(self):
  e=entry({})
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_pointer_escaping_and_empty_key(self):
  for native,pointer in [({'':'x'},'/native/'),({'a/b~':{'':'x'}},'/native/a~1b~0/')]:
   e=entry(native,pointer,'string','source-native','x');self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':'x'})
 def test_bad_escape_and_array_indexes(self):
  for pointer in ['/native/~2','/native/values/01','/native/values/-','/native/values/1']:
   e=entry({'values':['x']},pointer,'string','source-native','x')
   with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_array_exact_native_value(self):
  e=entry({'values':['x']},'/native/values/0','string','source-native','x')
  self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':'x'})
 def test_own_prototype_like_key_is_data(self):
  e=entry({'__proto__':{'constructor':'x'}},'/native/__proto__/constructor','string','source-native','x')
  self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':'x'})
 def test_non_string_native_refused(self):
  for value in (False,0,[],{}):
   e=entry({'description':{'value':value}},state='string',kind='source-native',label='x')
   with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_surrogate_refused(self):
  e=entry({'description':{'value':'\ud800'}},state='string',kind='source-native',label='\ud800')
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_source_hash_required(self):
  with self.assertRaises(ValueError):validate_label_origin(entry(),{'synthetic-source':{'sha256':'not-a-hash'}})
 def test_schema_closed_and_states(self):
  s=origin_schema();Draft202012Validator.check_schema(s);v=Draft202012Validator(s)
  v.validate(entry()['labelOrigin']);bad=entry()['labelOrigin'];bad['unexpected']=True
  with self.assertRaises(ValidationError):v.validate(bad)
  bad=entry()['labelOrigin'];bad['nativeState']='string'
  with self.assertRaises(ValidationError):v.validate(bad)
 def test_shape_cannot_prove_pointer_value(self):
  e=entry();e['labelOrigin']['nativeState']='null'
  Draft202012Validator(origin_schema()).validate(e['labelOrigin'])
  with self.assertRaises(ValueError):validate_label_origin(e,SOURCE)
 def test_full_schema_extension_only(self):
  s=json.loads((HERE/'classification-browser.schema.json').read_text());Draft202012Validator.check_schema(s)
  es=s['properties']['schemes']['items']['properties']['entries']['items'];Draft202012Validator(es).validate(entry())
  e=entry();e.pop('labelOrigin');Draft202012Validator(es).validate(e)
 def test_language_absent_null_empty_remain_distinct(self):
  for fields,state in [({},'absent'),({'lang':None},'null'),({'lang':''},'empty-string')]:
   e=entry({'description':{'value':'x',**fields}},state='string',kind='source-native',label='x')
   e['labelOrigin']['languagePointer']='/native/description/lang'
   self.assertEqual(validate_label_origin(e,SOURCE)['nativeLanguage']['state'],state)
   self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':'x'})
 def test_title_marker_cannot_qualify_a_source_label_form(self):
  e=entry();row={'title':e['label'],'details':{'entry':e,'scheme':{'sources':list(SOURCE.values())}}}
  with self.assertRaises(ValueError):qualify_title_form(row,{'kind':'preferred-label','pointer':'/title','value':e['label']})
 def test_complete_export_preserves_all_native_rows_and_qualified_titles(self):
  data=payload();s=data['schemes'][0];s['sources']=list(SOURCE.values())
  entries=[entry({},'/native/description','absent'),entry({'description':{'value':None}},state='null'),
           entry({'description':{'value':' '}},state='string',kind='source-native',label=' '),
           entry({'description':{'value':'Ordinary'}},state='string',kind='source-native',label='Ordinary')]
  legacy=entry(label='Legacy display');legacy.pop('labelOrigin');entries.append(legacy)
  for i,e in enumerate(entries):e['id']='row-'+str(i)
  s['entries']=entries;s['coverage'].update(expectedEntries=5,retainedEntries=5,definitionsStatus='labels-only')
  before=copy.deepcopy(data)
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'export';receipt=release.export(data,out,'b'*64,source_revision='4'*40)
   self.assertEqual(receipt['labelOrigins'],{'source-native':2,'project-display-fallback':2,'legacy-unqualified':1})
   rows=[read_markdown(f)[0]for f in (out/'cards').glob('*.md')]
   for row in rows:
    e=next(e for e in entries if e['id']==row['details']['entry']['id'])
    Draft202012Validator(json.loads((HERE/'record.schema.json').read_text())).validate(row)
    self.assertEqual(row['details']['entry'],e);self.assertEqual(row['title'],e['label']);self.assertEqual(row['skos:notation'],e['code'])
    if e.get('labelOrigin',{}).get('kind')=='project-display-fallback':self.assertNotIn('skos:prefLabel',row);self.assertNotIn('rdfs:label',row);self.assertNotIn('okfp:lexicalForm',row)
    else:self.assertEqual(row['skos:prefLabel'],e['label'])
   index=json.loads((out/'term-discovery.json').read_text())
   Draft202012Validator(json.loads((HERE/'term-discovery.schema.json').read_text())).validate(index)
   self.assertEqual(index['revision'],'4'*40);self.assertEqual(receipt['producerSourceRevision'],'4'*40)
   title_forms=[f for row in index['records']for f in row['forms']if f['kind']=='record-title']
   self.assertEqual(sum(f.get('labelOrigin')=='project-display-fallback'for f in title_forms),2)
   self.assertEqual(sum('labelOrigin'not in f for f in title_forms),1)
   for binding in receipt['files']:
    raw=(out/binding['path']).read_bytes();self.assertEqual(len(raw),binding['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),binding['sha256'])
  self.assertEqual(data,before)
 def test_invalid_origin_refuses_before_any_export_directory(self):
  data=payload();s=data['schemes'][0];s['sources']=list(SOURCE.values());s['entries']=[entry()]
  s['coverage'].update(expectedEntries=1,retainedEntries=1,definitionsStatus='labels-only');s['entries'][0]['labelOrigin']['nativeState']='null'
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'export'
   with self.assertRaises(ValueError):release.export(data,out,'b'*64,source_revision='4'*40)
   self.assertFalse(out.exists())
 def test_empty_source_label_is_valid_input_but_unrepresentable_export_title(self):
  data=payload();s=data['schemes'][0];s['sources']=list(SOURCE.values())
  e=entry({'description':{'value':''}},state='empty-string',kind='source-native',label='');s['entries']=[e]
  s['coverage'].update(expectedEntries=1,retainedEntries=1,definitionsStatus='labels-only')
  before=copy.deepcopy(data);release.validate(data)
  self.assertEqual(label_assertions(e,SOURCE,True),{'skos:prefLabel':''})
  with tempfile.TemporaryDirectory()as tmp:
   out=Path(tmp)/'export'
   with self.assertRaises(ValidationError):release.export(data,out,'b'*64,source_revision='4'*40)
   self.assertFalse(out.exists())
  self.assertEqual(data,before)
 def test_legacy_manifest_has_no_new_origin_assertion(self):
  with tempfile.TemporaryDirectory()as tmp:
   receipt=release.export(payload(),Path(tmp)/'export','b'*64,source_revision='4'*40)
   self.assertNotIn('labelOrigins',receipt)
if __name__=='__main__':unittest.main()
