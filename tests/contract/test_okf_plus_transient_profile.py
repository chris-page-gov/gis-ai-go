"""Synthetic bounded, privacy-preserving transient profiling contracts."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/okf_plus'))
import transient_profile as module


class TransientProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.patch=patch.object(module,'ROOT',self.root); self.patch.start();self.addCleanup(self.patch.stop)
        self.source=self.root/'artifacts/private/features.ndjson'
        self.source.parent.mkdir(parents=True)
        self.output=self.root/'artifacts/private/profile.json'
    def feature(self,**props):
        return {'type':'Feature','id':'SECRET-IDENTIFIER','geometry':{'type':'Point','coordinates':[123.456789,43.210987]},'properties':props}
    def write(self,records):
        self.source.write_text(''.join(json.dumps(row)+'\n' for row in records))
    def run_profile(self,**kwargs):return module.profile(self.source,self.output,**kwargs)
    def fields(self,result):return {tuple(row['path']):row for row in result['fields']}
    def test_full_scan_missing_null_declared_and_observed_enums_are_separate(self):
        records=[self.feature(width=2,status='A',note='PRIVATE FREE TEXT'),self.feature(width=None,status='B'),self.feature(status='OTHER')]
        self.write(records)
        schema={'type':'object','properties':{'properties':{'type':'object','required':['status'],
            'properties':{'width':{'type':['number','null']},'status':{'type':'string','enum':['A','B','C']},'absent':{'type':'string'}}}}}
        result=self.run_profile(schema=schema,recipe={'product':'synthetic','url':'https://example.org/data'})
        fields=self.fields(result)
        self.assertEqual(result['recordCount'],3); self.assertTrue(result['scanComplete'])
        self.assertEqual(result['declaredSchema'],schema)
        width=fields[('properties','width')]
        self.assertEqual((width['present'],width['missing'],width['null']),(2,1,1))
        self.assertEqual(width['types'],{'integer':1,'null':1})
        self.assertEqual(width['numericMin'],2)
        self.assertEqual(fields[('properties','absent')]['missing'],3)
        status=fields[('properties','status')]
        self.assertEqual(status['observedEnumeration'],['A','B'])
        self.assertEqual(status['outsideDeclaredEnumCount'],1)
        self.assertNotIn('OTHER',self.output.read_text())
        self.assertTrue(self.source.exists())
    def test_geometry_identifier_text_and_coordinate_properties_not_retained(self):
        self.write([self.feature(note='PRIVATE FREE TEXT',latitude=51.234567,osid=987654321,width=2.5)])
        result=self.run_profile()
        encoded=self.output.read_text()
        for secret in ['PRIVATE FREE TEXT','SECRET-IDENTIFIER','123.456789','43.210987','51.234567','987654321']:
            self.assertNotIn(secret,encoded)
        fields=self.fields(result)
        self.assertEqual(fields[('geometry','coordinates')]['types'],{'array':1})
        self.assertIsNone(fields[('geometry','coordinates','*')]['numericMin'])
        self.assertIsNone(fields[('id',)]['cardinalityLowerBound'])
        self.assertEqual(result['geometryStructure'],{'types':{'Point':1},'coordinateDimensions':{'2':1}})
        self.assertIsNone(fields[('properties','latitude')]['numericMin'])
        self.assertEqual(fields[('properties','note')]['maximumStringLength'],17)
    def test_multiline_featurecollection_and_explicit_controlled_values(self):
        self.source.write_text(json.dumps({'type':'FeatureCollection','features':[
            self.feature(category='rural'),self.feature(category='urban')]},indent=2))
        result=self.run_profile(format='geojson',controlled_fields=['properties/category'])
        self.assertEqual(self.fields(result)[('properties','category')]['observedEnumeration'],['rural','urban'])
        self.assertEqual(result['recordCount'],2)
    def test_nested_array_items_denominators_types_null_and_schema_enums(self):
        self.write([self.feature(parts=[{'code':'A','measure':1},{'code':None},{'measure':2}]),
                    self.feature(parts=[]),self.feature(parts=[{'code':'B'},None,7])])
        schema={'properties':{'properties':{'properties':{'parts':{'type':'array','items':{
            'type':['object','null','integer'],'properties':{'code':{'enum':['A','B','C',None]},
            'never':{'type':'string'}}}}}}}}
        result=self.run_profile(schema=schema)
        rows=self.fields(result)
        parts=rows[('properties','parts')]
        self.assertEqual((parts['arrayLengthMin'],parts['arrayLengthMax']),(0,3))
        items=rows[('properties','parts','*')]
        self.assertEqual(items['types'],{'object':4,'null':1,'integer':1})
        self.assertEqual((items['present'],items['opportunities'],items['missing'],items['recordPresence']),(6,6,0,2))
        code=rows[('properties','parts','*','code')]
        self.assertEqual((code['present'],code['opportunities'],code['missing'],code['null']),(3,4,1,1))
        self.assertEqual(code['observedEnumeration'],['A','B',None])
        self.assertEqual(rows[('properties','parts','*','never')]['missing'],4)
        self.assertIsNone(parts['cardinalityLowerBound'])
    def test_controlled_containers_fail_without_retaining_contents(self):
        self.write([self.feature(parts=[{'private':'DO NOT STORE'}])])
        with self.assertRaisesRegex(ValueError,'scalar'):
            self.run_profile(controlled_fields=['properties/parts'])
        self.assertFalse(self.output.exists());self.assertTrue(self.source.exists())
    def test_nested_geometry_dimensions_and_identifier_array_privacy(self):
        record=self.feature(identifiers=['SECRET-ONE','SECRET-TWO'])
        record['geometry']={'type':'LineString','coordinates':[[123.456789,43.210987,99.876543],[124.456789,44.210987,98.876543]]}
        self.write([record])
        result=self.run_profile()
        self.assertEqual(result['geometryStructure']['coordinateDimensions'],{'3':2})
        encoded=self.output.read_text()
        for value in ['SECRET-ONE','SECRET-TWO','123.456789','99.876543']:
            self.assertNotIn(value,encoded)
        rows=self.fields(result)
        self.assertIsNone(rows[('properties','identifiers','*')]['cardinalityLowerBound'])
        self.assertEqual(rows[('geometry','coordinates','*')]['arrayLengthMin'],3)
        self.assertIsNone(rows[('geometry','coordinates','*','*')]['cardinalityLowerBound'])

    def test_limits_and_malformed_input_preserve_original_without_output(self):
        for kwargs in [{'max_bytes':10},{'max_records':1},{'max_depth':2}]:
            self.write([self.feature(width=1),self.feature(width=2)])
            original=self.source.read_bytes()
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                self.run_profile(discard_after_success=True,**kwargs)
            self.assertEqual(self.source.read_bytes(),original);self.assertFalse(self.output.exists())
        self.source.write_bytes(b'{"type":"Feature"}\nmalformed\n')
        with self.assertRaises(ValueError):self.run_profile(discard_after_success=True)
        self.assertTrue(self.source.exists());self.assertFalse(self.output.exists())
    def test_cardinality_overflow_explicit_incomplete_and_prevents_disposal(self):
        self.write([self.feature(width=1),self.feature(width=2)])
        with self.assertRaisesRegex(ValueError,'Cardinality budget incomplete'):
            self.run_profile(cardinality_cap=1,discard_after_success=True)
        self.assertTrue(self.source.exists())
        rows=self.fields(json.loads(self.output.read_text()))
        self.assertFalse(rows[('properties','width')]['cardinalityComplete'])
        self.assertEqual(rows[('properties','width')]['cardinalityLowerBound'],1)
    def test_observed_enum_overflow_is_failure_and_retains_original(self):
        self.write([self.feature(status='a'),self.feature(status='b')])
        with self.assertRaisesRegex(ValueError,'enumeration budget'):
            self.run_profile(controlled_fields=['properties/status'],cardinality_cap=1,discard_after_success=True)
        self.assertTrue(self.source.exists());self.assertFalse(self.output.exists())
    def test_discard_requires_success_and_ignored_input_path(self):
        self.write([self.feature(width=3)])
        result=self.run_profile(discard_after_success=True)
        self.assertFalse(self.source.exists());self.assertTrue(self.output.exists());self.assertTrue(result['scanComplete'])
        outside=self.root/'original.ndjson';outside.write_text(json.dumps(self.feature()))
        with self.assertRaisesRegex(ValueError,'restricted'):
            module.profile(outside,self.root/'artifacts/other.json',discard_after_success=True)
        self.assertTrue(outside.exists())
    def test_field_knowledge_cards_exact_statistics_hashes_and_explicit_links(self):
        import hashlib
        self.write([self.feature(width=2,status='A',note='PRIVATE FREE TEXT'),self.feature(status='B')])
        schema={'properties':{'properties':{'properties':{'width':{'type':['number','null']},
            'status':{'type':'string','enum':['A','B','C']}}}}}
        snapshot=self.run_profile(schema=schema,recipe={'url':'https://example.org/data'})
        destination=self.root/'artifacts/private/field-cards'
        identities={('properties','width'):{'@id':'https://example.org/native/width',
            'structuralField':'https://example.org/knowledge/width','collection':'https://example.org/collections/roads'},
            ('properties','status'):'https://example.org/native/status'}
        index=module.export_field_knowledge(self.output,destination,identities,max_card_bytes=8000)
        self.assertEqual(index['fieldCount'],len(snapshot['fields']))
        self.assertEqual(index['profileSha256'],hashlib.sha256(self.output.read_bytes()).hexdigest())
        rows=self.fields(snapshot)
        for entry in index['fields']:
            payload=(destination/entry['file']).read_bytes()
            self.assertLessEqual(len(payload),8000)
            self.assertEqual(entry['bytes'],len(payload))
            self.assertEqual(entry['sha256'],hashlib.sha256(payload).hexdigest())
            card=json.loads(payload)
            self.assertEqual(card['statistics'],rows[tuple(entry['path'])])
            self.assertFalse(card['observedScope']['providerUniverseComplete'])
            self.assertNotIn('PRIVATE FREE TEXT',payload.decode())
            self.assertNotIn('SECRET-IDENTIFIER',payload.decode())
            self.assertNotIn(str(self.root),payload.decode())
            if entry['path']==['properties','width']:
                self.assertEqual(card['@id'],identities[('properties','width')]['@id'])
                self.assertEqual(card['dcterms:references']['@id'],'https://example.org/knowledge/width')
                self.assertEqual(card['declaredFieldDefinition'],{'type':['number','null']})
        with self.assertRaises(ValueError):module.export_field_knowledge(self.output,destination)
    def test_field_card_budget_or_bad_identity_publishes_nothing_and_preserves_profile(self):
        self.write([self.feature(width=2)])
        self.run_profile()
        original=self.output.read_bytes()
        destination=self.root/'artifacts/private/field-cards'
        with self.assertRaisesRegex(ValueError,'byte ceiling'):
            module.export_field_knowledge(self.output,destination,max_card_bytes=100)
        self.assertFalse(destination.exists());self.assertEqual(self.output.read_bytes(),original)
        with self.assertRaises(ValueError):
            module.export_field_knowledge(self.output,destination,{('properties','width'):'https://example.org/data?key=synthetic'})
        self.assertFalse(destination.exists())
        with self.assertRaises(ValueError):
            module.export_field_knowledge(self.output,self.root/'public-cards')
        self.assertEqual(self.output.read_bytes(),original)

    def test_public_output_credentials_and_output_failure_preserve_source(self):
        self.write([self.feature()])
        with self.assertRaises(ValueError):module.profile(self.source,self.root/'public.json')
        for recipe in [{'url':'https://example.org/data?key=synthetic'},{'authorization':'synthetic'}]:
            with self.assertRaises(ValueError):self.run_profile(recipe=recipe)
        with patch.object(module.os,'link',side_effect=OSError('disk error')),self.assertRaises(OSError):
            self.run_profile(discard_after_success=True)
        self.assertTrue(self.source.exists());self.assertFalse(self.output.exists())


if __name__=='__main__':unittest.main()
