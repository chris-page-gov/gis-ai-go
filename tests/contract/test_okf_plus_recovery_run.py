"""Bounded supervisor tests using fake time and synthetic local evidence only."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from scripts.okf_plus import recovery_run as recovery
from scripts.okf_plus.model import canonical
from scripts.okf_plus.passages import split_document


class RecoveryRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.now=0
        self.private=self.root/recovery.sync.PRIVATE
        self.private.mkdir(parents=True)
        self.url='https://docs.os.uk/osngd/synthetic.md'
        self.frozen_scope={'targets':[self.url]}
        self.capture=Mock(); self.card_export=Mock(side_effect=self.cards)
        self.passage_export=Mock(side_effect=self.overlays)

    def sleep(self,seconds): self.now+=seconds
    def state(self,rows,targets=None,stop=None):
        value={'scope':{'targets':targets or [self.url]},'records':rows,
               'stopReason':stop,'scopeComplete':False}
        self.frozen_scope=value['scope'].copy()
        recovery.atomic(self.private/'checkpoint.json',value)
        return value
    def captured(self):
        raw=b'# Synthetic\n'; digest=hashlib.sha256(raw).hexdigest()
        (self.private/(digest+'.body')).write_bytes(raw)
        manifest,parts=split_document(raw,self.url)
        directory=self.private/'passages/synthetic';directory.mkdir(parents=True)
        (directory/'manifest.jsonld').write_bytes(canonical(manifest))
        for segment,part in zip(manifest['segments'],parts):
            (directory/segment['file']).write_bytes(part)
        return {'status':'captured','receipt':{'url':self.url,'sha256':digest,'rawFile':digest+'.body'},
                'passageDirectory':'passages/synthetic'}
    def cards(self,root,output):
        output.mkdir();(output/'index.json').write_text('{"cards":[]}')
        return [],{'cards':[]}
    def overlays(self,root,**kwargs):
        self.assertTrue(kwargs['all_collections'])
        output=kwargs['output'];self.assertFalse(output.exists());output.mkdir()
        (output/'index.json').write_text('{"candidateOnly":true,"allCollections":true}')
        return {'candidateOnly':True,'allCollections':True}
    def run_supervisor(self,**kwargs):
        return recovery.run(self.root,clock=lambda:self.now,sleep=self.sleep,
            sync_runner=self.capture,card_export=self.card_export,
            passage_export=self.passage_export,head_reader=lambda _: 'a'*40,
            scope_reader=lambda _:self.frozen_scope,**kwargs)

    def test_existing_writer_is_observed_without_duplicate_capture_until_wall_budget(self):
        self.state({})
        with recovery.sync.writer_lock(self.private):
            result=self.run_supervisor(max_wall_seconds=3,poll_seconds=1)
        self.assertEqual(result['status'],'wall_budget')
        self.assertEqual(self.now,3)
        self.capture.assert_not_called();self.card_export.assert_not_called()
        self.assertTrue((self.private/'writer.lock').exists())

    def test_unknown_capture_then_audit_and_new_immutable_exports(self):
        self.state({})
        def capture(root,**kwargs):
            self.assertEqual(kwargs['max_requests'],3000)
            self.assertEqual(kwargs['max_documents'],2303)
            self.assertLessEqual(kwargs['deadline_seconds'],3600)
            self.assertIs(kwargs['capture_factory'],recovery.NoFailedRetryCapture)
            return self.state({self.url:self.captured()})
        self.capture.side_effect=capture
        result=self.run_supervisor()
        self.assertEqual(result['status'],'finished_complete')
        self.assertEqual(result['counts']['unresolved'],0)
        self.assertEqual([p['phase'] for p in result['phases']],['capture','audit','field_cards','field_passages'])
        self.assertFalse(result['sourceScopeComplete'])
        self.assertFalse(result['workspaceSurvivalGuaranteed'])
        receipt=self.root/result['outputDirectory']/'receipt.json'
        self.assertEqual(json.loads(receipt.read_text())['status'],'finished_complete')

    def test_known_307_failures_are_reported_partial_without_retries(self):
        targets=[self.url]+[f'https://docs.os.uk/osngd/failure-{i}.md' for i in range(307)]
        rows={url:{'status':'failed'} for url in targets[1:]};rows[self.url]=self.captured()
        self.state(rows,targets)
        recovery.atomic(self.private/'ledger.json',{'requests':[{'status':429}]})
        result=self.run_supervisor()
        self.assertEqual(result['status'],'finished_partial')
        self.assertEqual(result['counts'],{'requested':308,'processed':308,'captured':1,'failed':307,'unresolved':0})
        self.capture.assert_not_called()
        self.assertFalse(result['sourceScopeComplete'])
        self.assertEqual(result['phases'][0]['verifiedCaptured'],1)

    def test_audit_failure_preserves_checkpoint_and_prevents_exports(self):
        row=self.captured();self.state({self.url:row})
        (self.private/row['receipt']['rawFile']).write_bytes(b'corrupt')
        before=(self.private/'checkpoint.json').read_bytes()
        result=self.run_supervisor()
        self.assertEqual(result['status'],'failed');self.assertEqual(result['errorType'],'ValueError')
        self.assertEqual((self.private/'checkpoint.json').read_bytes(),before)
        self.card_export.assert_not_called();self.passage_export.assert_not_called()

    def test_no_progress_non_resumable_and_429_never_loop_or_retry(self):
        for mode in ['no-progress','non-resumable','429']:
            with self.subTest(mode=mode):
                self.capture.reset_mock();self.now=0
                state=self.state({},stop='request ceiling' if mode=='non-resumable' else None)
                ledger=self.private/'ledger.json'
                if ledger.exists():ledger.unlink()
                if mode=='429': recovery.atomic(ledger,{'requests':[{'status':429}]})
                self.capture.side_effect=lambda *args,**kwargs:state
                result=self.run_supervisor()
                self.assertEqual(result['status'],'blocked')
                self.assertEqual(self.capture.call_count,1 if mode=='no-progress' else 0)

    def test_known_failure_capture_reuses_receipt_without_parent_provider_call(self):
        capture=object.__new__(recovery.NoFailedRetryCapture)
        failure={'url':self.url,'status':404}
        capture.ledger={'requests':[failure]}
        with patch.object(recovery.sync.PrivateCapture,'get') as parent:
            self.assertEqual(capture.get(self.url,'text'),(None,failure))
            parent.assert_not_called()

    def test_changed_source_scope_refuses_even_a_complete_checkpoint_before_audit(self):
        row=self.captured()
        state=self.state({self.url:row});state['scopeComplete']=True
        recovery.atomic(self.private/'checkpoint.json',state)
        before=(self.private/'checkpoint.json').read_bytes()
        self.frozen_scope={'targets':[self.url,'https://docs.os.uk/osngd/new-source.md']}
        with patch.object(recovery.sync,'verify_passages') as verify:
            result=self.run_supervisor()
            verify.assert_not_called()
        self.assertEqual(result['status'],'failed')
        self.assertEqual(result['errorType'],'ValueError')
        self.assertEqual((self.private/'checkpoint.json').read_bytes(),before)
        self.assertTrue((self.private/row['receipt']['rawFile']).is_file())
        self.capture.assert_not_called();self.card_export.assert_not_called()
        self.passage_export.assert_not_called()

    def test_latest_success_is_not_shadowed_by_an_older_failure(self):
        capture=object.__new__(recovery.NoFailedRetryCapture)
        capture.ledger={'requests':[{'url':self.url,'status':404},{'url':self.url,'status':200}]}
        with patch.object(recovery.sync.PrivateCapture,'get',return_value=('cached',{'status':200})) as parent:
            self.assertEqual(capture.get(self.url,'text')[0],'cached')
            parent.assert_called_once_with(self.url,'text')

    def test_interrupted_receipts_do_not_shadow_a_known_terminal_failure(self):
        for pending in ('pending',None):
            with self.subTest(pending=pending):
                capture=object.__new__(recovery.NoFailedRetryCapture)
                failure={'url':self.url,'status':404}
                capture.ledger={'requests':[failure,{'url':self.url,'status':pending}]}
                with patch.object(recovery.sync.PrivateCapture,'get') as parent:
                    self.assertEqual(capture.get(self.url,'text'),(None,failure))
                    parent.assert_not_called()

    def test_prior_429_stops_even_after_later_terminal_or_interrupted_receipts(self):
        for later in (200,404,'pending',None):
            with self.subTest(later=later):
                capture=object.__new__(recovery.NoFailedRetryCapture)
                capture.ledger={'requests':[{'url':self.url,'status':429},{'url':self.url,'status':later}]}
                with patch.object(recovery.sync.PrivateCapture,'get') as parent:
                    with self.assertRaisesRegex(RuntimeError,'Prior rate-limit stop'):
                        capture.get(self.url,'text')
                    parent.assert_not_called()

    def test_optional_receipt_schema_enforces_private_partial_and_runtime_limits(self):
        from jsonschema import Draft202012Validator, ValidationError
        schema=json.loads((Path(__file__).resolve().parents[2]/'okf-plus/schemas/recovery-supervisor.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
        validator=Draft202012Validator(schema)
        self.state({self.url:{'status':'failed'}})
        result=self.run_supervisor()
        validator.validate(result)
        for key,value in [('distribution','public'),('workspaceSurvivalGuaranteed',True),
                          ('maxWallSeconds',86401),('sourceScopeComplete',True)]:
            with self.subTest(key=key),self.assertRaises(ValidationError):
                validator.validate({**result,key:value})

    def test_supervisor_lock_and_bounded_arguments(self):
        self.state({})
        root=self.root/recovery.PRIVATE;root.mkdir(parents=True)
        import fcntl
        with (root/'supervisor.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            with self.assertRaisesRegex(RuntimeError,'already active'):self.run_supervisor()
        for kwargs in [{'max_wall_seconds':86401},{'max_wall_seconds':True},{'poll_seconds':0}]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):self.run_supervisor(**kwargs)
