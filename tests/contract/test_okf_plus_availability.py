"""Synthetic uncertainty, rights and native property presence contracts."""
import copy
import hashlib
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError
from scripts.okf_plus.availability import assess_availability, from_ngd_receipt, from_query_plan


class AvailabilityTests(unittest.TestCase):
    def fixture(self, **kwargs):
        return {'source':{'id':'synthetic-source','version':'5'},
            'selector':{'id':'synthetic-selection','spatial':'synthetic-area','time':'synthetic-window'},
            'field':{'id':'urn:synthetic:width','path':['properties','width']},
            'evidence':[{'reference':'urn:synthetic:receipt','receipt_sha256':'a'*64}], **kwargs}

    def bound_fixture(self):
        spec=self.fixture()
        selection={'collection':spec['source']['id'],'bbox':[0,0,1,1]}
        spec['selector']['id']=hashlib.sha256(json.dumps(selection,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        return spec,selection

    def test_allowed_expected_not_attempted_does_not_mean_available(self):
        result=assess_availability(self.fixture(access='allowed',expected_presence='expected'))
        self.assertEqual(result['observed_presence'],'unknown')
        self.assertEqual(result['status'],'unknown')
        self.assertFalse(result['expectation_gap'])

    def test_missing_null_and_zero_are_distinct(self):
        statuses=[]
        for observation in ['property_missing','null','zero','value']:
            result=assess_availability(self.fixture(observation=observation,retrieval='complete',expected_presence='expected'))
            statuses.append(result['status'])
            self.assertEqual(result['expectation_gap'],observation=='property_missing')
            self.assertEqual(result['observed_presence'],'absent' if observation=='property_missing' else 'present')
        self.assertEqual(statuses,['property_missing','present_null','present_zero','present_value'])

    def test_incomplete_paging_and_unknown_denominator_never_infer_absence(self):
        for observation in ['property_missing','empty']:
            result=assess_availability(self.fixture(observation=observation,retrieval='incomplete',denominator_known=True,empty_reason='filtered_empty'))
            self.assertEqual(result['status'],'retrieval_incomplete')
            self.assertEqual(result['observed_presence'],'unknown')
        result=assess_availability(self.fixture(observation='empty',retrieval='complete',empty_reason='filtered_empty'))
        self.assertEqual(result['observed_presence'],'unknown')

    def test_complete_empty_contexts_are_explicit_not_conflated(self):
        for reason in ['outside_coverage','filtered_empty','not_collected','unavailable_product']:
            result=assess_availability(self.fixture(observation='empty',retrieval='complete',denominator_known=True,empty_reason=reason))
            self.assertEqual(result['status'],reason)
            self.assertEqual(result['access'],'unknown')
            self.assertEqual(result['observed_presence'],'absent')

    def test_permission_and_transient_failure_do_not_establish_absence(self):
        denied=assess_availability(self.fixture(access='denied',retrieval='failed'))
        failed=assess_availability(self.fixture(access='allowed',retrieval='failed',failure_reason='transient_failure'))
        self.assertEqual(denied['status'],'permission_denied')
        self.assertEqual(failed['status'],'transient_failure')
        self.assertEqual(failed['observed_presence'],'unknown')
        self.assertEqual(failed['access'],'allowed')

    def test_receipt_adapter_preserves_scope_and_disposal_is_not_retrievable(self):
        spec,selection=self.bound_fixture()
        for receipt,state in [({'complete':True,'selection':selection},'complete'),
            ({'complete':True,'payloadDiscarded':True},'incomplete'),
            ({'complete':False,'reason':'request-budget'},'incomplete'),
            ({'complete':False,'reason':'rate-limited'},'failed')]:
            result=from_ngd_receipt({**receipt,'selection':selection},source=spec['source'],selector=spec['selector'],field=spec['field'],evidence_reference='urn:synthetic:receipt',observation='empty')
            self.assertEqual(result['retrieval'],state)
            self.assertEqual(result['source'],spec['source'])
            self.assertEqual(result['selector'],spec['selector'])
            self.assertEqual(result['observed_presence'],'unknown')
            self.assertEqual(len(result['evidence'][0]['receipt_sha256']),64)

    def test_complete_receipt_for_a_different_selector_never_establishes_absence(self):
        spec=self.fixture()
        with self.assertRaisesRegex(ValueError,'bind the requested'):
            from_ngd_receipt({'complete':True,'selection':{'collection':spec['source']['id']}},
                source=spec['source'],selector=spec['selector'],field=spec['field'],
                evidence_reference='urn:synthetic:receipt',observation='property_missing')

    def test_every_receipt_state_rejects_unrelated_collection_or_selector_before_claims(self):
        spec,selection=self.bound_fixture()
        for state in ({'complete':True},{'complete':True,'payloadDiscarded':True},
                      {'complete':False,'reason':'http-failed','lastHttpStatus':403},
                      {'complete':False,'reason':'rate-limited'},
                      {'complete':False,'reason':'request-budget'}):
            for mismatch in ('collection','selector','missing-selection'):
                for observation in ('unknown','null','zero','value','property_missing'):
                    receipt={**state,'selection':selection}
                    source=copy.deepcopy(spec['source']);selector=copy.deepcopy(spec['selector'])
                    if mismatch=='collection':source['id']='other-collection'
                    elif mismatch=='selector':selector['id']='other-selector'
                    else:del receipt['selection']
                    with self.subTest(state=state,mismatch=mismatch,observation=observation),self.assertRaisesRegex(ValueError,'bind the requested'):
                        from_ngd_receipt(receipt,source=source,selector=selector,field=spec['field'],
                            evidence_reference='urn:synthetic:receipt',observation=observation,access='allowed')

    def test_bound_failure_does_not_override_explicit_owner_access_claim(self):
        spec,selection=self.bound_fixture()
        spec['selector']['id']='urn:sha256:'+spec['selector']['id']
        result=from_ngd_receipt({'selection':selection,'complete':False,'reason':'http-failed','lastHttpStatus':403},
            source=spec['source'],selector=spec['selector'],field=spec['field'],
            evidence_reference='urn:synthetic:receipt',access='allowed',expected_presence='expected')
        self.assertEqual(result['access'],'allowed')
        self.assertEqual(result['expected_presence'],'expected')
        self.assertEqual(result['observed_presence'],'unknown')
        self.assertEqual(result['status'],'permission_denied')

        self.assertEqual(result['failure_reason'],'permission_denial')

    def test_planner_missing_candidates_are_not_missing_data(self):
        spec=self.fixture()
        for selected in [None, {'recipes':[]}]:
            plan={'profile':'okf-plus-offline-query-plan.v1','execution':False,
                  'selected':selected,'missing_fields':[spec['field']]}
            result=from_query_plan(plan,source=spec['source'],selector=spec['selector'],
                field=spec['field'],evidence_reference='urn:synthetic:plan',access='allowed')
            self.assertEqual(result['retrieval'],'not_attempted')
            self.assertEqual(result['observed_presence'],'unknown')
            self.assertEqual(result['expected_presence'],'unknown')
            self.assertEqual(result['access'],'allowed')
            self.assertFalse(result['expectation_gap'])
            self.assertIn('data presence remains unknown',result['summary'])

    def test_bounded_secret_free_input_and_no_mutation(self):
        spec=self.fixture();before=copy.deepcopy(spec)
        assess_availability(spec);self.assertEqual(spec,before)
        for update in [{'access':'yes'},{'denominator_known':1},{'evidence':[]},
                       {'field':{'id':'x','path':[]}}, {'unexpected':True},
                       {'selector':{'id':'https://example.invalid/?key=secret','spatial':None,'time':None}}]:
            with self.subTest(update=update),self.assertRaises(ValueError):
                assess_availability(self.fixture(**update))

    def test_output_schema_and_false_completeness_authority_rejection(self):
        schema=json.loads((Path(__file__).resolve().parents[2]/'okf-plus/schemas/data-availability.schema.json').read_text())
        Draft202012Validator.check_schema(schema);validator=Draft202012Validator(schema)
        result=assess_availability(self.fixture(observation='property_missing',retrieval='complete',expected_presence='expected'))
        validator.validate(result)
        for key,value in [('execution',True),('distribution','public'),('retrieval','incomplete')]:
            changed={**result,key:value}
            with self.subTest(key=key),self.assertRaises(ValidationError):validator.validate(changed)

    def test_request_denial_is_distinct_from_server_error_and_licence_rights(self):
        spec,selection=self.bound_fixture()
        def outcome(status):
            return from_ngd_receipt({'selection':selection,'complete':False,'reason':'http-failed','lastHttpStatus':status},
                source=spec['source'],selector=spec['selector'],field=spec['field'],
                evidence_reference='urn:synthetic:receipt')
        denied=outcome(403);failed=outcome(500)
        self.assertEqual(denied['access'],'denied')
        self.assertEqual(denied['status'],'permission_denied')
        self.assertEqual(failed['access'],'unknown')
        self.assertEqual(failed['status'],'retrieval_failed')
        self.assertEqual(denied['observed_presence'],'unknown')
