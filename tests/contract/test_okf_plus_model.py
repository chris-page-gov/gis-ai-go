"""Meaningful offline guard tests for metadata capture and source integrity."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/okf_plus'))
from harvest import allowed, clean_text
from model import load_json, read_markdown, record, write_markdown, apply_frequency, apply_temporal

class OkfPlusModelTests(unittest.TestCase):
    def test_metadata_routes_reject_features_observations_credentials_and_redirects(self):
        for url in ('http://api.os.uk/downloads/v1/products',
                    'https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/items',
                    'https://api.beta.ons.gov.uk/v1/datasets/x/editions/a/versions/1/observations',
                    'https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.data.json',
                    'https://api.os.uk/downloads/v1/products?key=synthetic',
                    'https://api.os.uk.evil.invalid/downloads/v1/products',
                    'https://user@api.os.uk/downloads/v1/products',
                    'https://api.os.uk:444/downloads/v1/products',
                    'https://127.0.0.1/private'):
            with self.subTest(url=url),self.assertRaises(ValueError):allowed(url)
        self.assertTrue(allowed('https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-building-4/schema'))
        self.assertTrue(allowed('https://osmetadata.astuntechnology.com/geonetwork/api/collections/044fac9d-3bba-4214-b010-eeb9978422b2/items?f=json&q=&startIndex=0'))
    def test_duplicate_nonfinite_and_executable_yaml_rejected(self):
        for text in ('{"a":1,"a":2}','{"a":NaN}','!!python/object/apply:os.system [echo]','---\na: b\n---\nc: d'):
            with self.subTest(text=text),self.assertRaises(ValueError):load_json(text)
    def test_native_cadence_not_imputed_from_release_or_title(self):
        row=record('test','demo','Monthly data 1991','Synthetic metadata','https://example.org/data',{'resource':'https://example.org/data'})
        self.assertIsNone(row['update']['frequency']['label'])
        self.assertIsNone(row['temporal']['start'])
        apply_frequency(row,'Quarterly','release_frequency')
        self.assertEqual(row['update']['frequency']['iri'],'http://purl.org/linked-data/sdmx/2009/code#freq-Q')
        self.assertEqual(row['temporal']['status'],'not-evidenced')
    def test_open_extent_keeps_open_end_and_role(self):
        row=record('test','demo','Demo','Synthetic','https://example.org/data',{'resource':'https://example.org/data'})
        apply_temporal(row,'2022-07-30T00:00:00Z',None,'advertised-collection-temporal-extent','extent.temporal.interval[0]')
        self.assertIsNone(row['temporal']['end'])
        self.assertNotIn('dcat:endDate',row['dcterms:temporal'])
        self.assertIn('does not prove',row['temporal']['note'])
    def test_markup_and_contact_details_not_published(self):
        text=clean_text('<p>Metadata</p> For further information contact Person <a>a@example.invalid</a> +44 1234 567890')
        self.assertNotIn('example.invalid',text)
        self.assertNotIn('Person',text)
        self.assertNotIn('<',text)
    def test_front_matter_round_trip_is_unicode_safe(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'r.md';row={'title':'Welsh – Cymraeg','temporal':{'start':None}}
            write_markdown(path,row,'# Evidence\n\nPreserve source identifiers.')
            actual,body=read_markdown(path)
            self.assertEqual(actual,row);self.assertIn('Preserve source',body)

if __name__=='__main__':unittest.main()
