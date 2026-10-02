"""Evidence-preserving Nomis table projection, without truncation or type coercion."""
import copy
import unittest
from scripts.okf_plus.model import compact_time_metadata, expand_time_metadata

class NativeTimeTableTests(unittest.TestCase):
    def test_round_trip_preserves_types_absent_empty_and_revision_fields(self):
        original={'id':'synthetic','codes':[
            {'value':1971,'revisionMetadata':[]},
            {'value':'1971','description':{},'revisionMetadata':[]},
            {'value':'1971-01','description':{'lang':'en','value':'January 1971'},
             'revisionMetadata':[{'title':'CurrentRevisionVersion','value':3},
                                 {'title':'period start','value':'1971-01-01'}]}]}
        before=copy.deepcopy(original)
        compact=compact_time_metadata(original)
        self.assertEqual(expand_time_metadata(compact),before)
        self.assertEqual(original,before)
        self.assertIs(type(compact['timeOptionsTable']['rows'][0][0]),int)
        self.assertIs(type(compact['timeOptionsTable']['rows'][1][0]),str)

    def test_unknown_fields_are_rejected_instead_of_dropped(self):
        for code in ({'value':2000,'revisionMetadata':[],'newNativeField':'retain me'},
                     {'value':2000,'revisionMetadata':[{'title':'revision','value':1,'extra':2}]}):
            with self.subTest(code=code),self.assertRaises(ValueError):
                compact_time_metadata({'codes':[code]})
