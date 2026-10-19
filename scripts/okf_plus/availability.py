"""Private, offline evidence-bound data availability assessment.

Owner: GIS AI GO repository owner. Policy: access claims, expected presence and
observations are separate; no execution authority is granted. Threat: provider
claims and receipts are untrusted evidence, never executable instructions. Exact
source/version/selector/field identifiers are retained without semantic inference.

Input requires source {id,version}, selector {id,spatial,time}, field {id,path},
evidence [{reference,receipt_sha256}]. Optional access allowed/denied/unknown,
expected_presence expected/not_expected/unknown, retrieval
complete/incomplete/not_attempted/failed, and observation property_missing/null/
zero/value/empty/unknown. Empty results require denominator_known:true and an
explicit empty_reason to establish absence. An incomplete retrieval cannot
establish missing/absent data. Context reasons are supplied evidence claims.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

MAX_INPUT_BYTES = 65536
ACCESS = {'allowed', 'denied', 'unknown'}
EXPECTED = {'expected', 'not_expected', 'unknown'}
RETRIEVAL = {'complete', 'incomplete', 'not_attempted', 'failed'}
OBSERVATIONS = {'property_missing', 'null', 'zero', 'value', 'empty', 'unknown'}
REASONS = {'outside_coverage', 'filtered_empty', 'not_collected', 'unavailable_product', 'unknown'}


def _safe(value, depth=0):
    if depth > 16: raise ValueError('Metadata depth ceiling')
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str) or ''.join(c for c in key.lower() if c.isalnum()) in {
                'key','apikey','token','authorization','password','secret','accesstoken'}:
                raise ValueError('Credentials are forbidden in availability evidence')
            _safe(item, depth + 1)
    elif isinstance(value, list):
        for item in value: _safe(item, depth + 1)
    elif isinstance(value,str):
        if value.lower().startswith(('bearer ','basic ')): raise ValueError('Credential text forbidden')
        if '://' in value:
            url=urlsplit(value)
            if url.username or url.password or any(''.join(c for c in k.lower() if c.isalnum()) in {'key','apikey','token','accesstoken'} for k,_ in parse_qsl(url.query)):
                raise ValueError('Credential URL forbidden')
    elif isinstance(value, float) and not math.isfinite(value): raise ValueError('Non-finite metadata')


def _text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 2048:
        raise ValueError('Expected bounded non-empty identifier')
    return value


def assess_availability(spec):
    if not isinstance(spec, dict): raise ValueError('Expected availability object')
    _safe(spec)
    if len(json.dumps(spec)) > MAX_INPUT_BYTES: raise ValueError('Availability input byte ceiling')
    allowed = {'source','selector','field','evidence','access','expected_presence','retrieval',
               'observation','denominator_known','empty_reason','failure_reason'}
    if set(spec) - allowed: raise ValueError('Unknown availability fields')
    for name, keys in [('source', {'id','version'}), ('selector', {'id','spatial','time'}), ('field', {'id','path'})]:
        value = spec.get(name)
        if not isinstance(value, dict) or set(value) != keys: raise ValueError('Explicit source, selector and field context required')
        for key in keys:
            if name == 'field' and key == 'path':
                if not isinstance(value[key], list) or not 1 <= len(value[key]) <= 16:
                    raise ValueError('Explicit bounded native property path required')
                for part in value[key]: _text(part)
            elif value[key] is not None: _text(value[key])
            elif key in {'id','path'}: raise ValueError('Stable identity required')
    evidence = spec.get('evidence')
    if not isinstance(evidence, list) or not 1 <= len(evidence) <= 64:
        raise ValueError('Bounded evidence references required')
    for row in evidence:
        if not isinstance(row, dict) or set(row) != {'reference','receipt_sha256'}:
            raise ValueError('Evidence reference and receipt digest required')
        _text(row['reference'])
        digest = row['receipt_sha256']
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in 'abcdef0123456789' for c in digest):
            raise ValueError('Invalid receipt SHA256')
    access, expected, retrieval = (spec.get('access','unknown'), spec.get('expected_presence','unknown'), spec.get('retrieval','not_attempted'))
    observation, reason = spec.get('observation','unknown'), spec.get('empty_reason','unknown')
    for value, options in [(access,ACCESS),(expected,EXPECTED),(retrieval,RETRIEVAL),(observation,OBSERVATIONS),(reason,REASONS)]:
        if not isinstance(value,str) or value not in options: raise ValueError('Unknown availability enum')
    failure_reason=spec.get('failure_reason','unknown')
    if not isinstance(failure_reason, str) or failure_reason not in {'transient_failure','permission_denial','unknown'}: raise ValueError('Unknown failure reason')
    denominator = spec.get('denominator_known',False)
    if type(denominator) is not bool: raise ValueError('Denominator knowledge must be explicit boolean')
    present = observation in {'null','zero','value'}
    absent = (retrieval == 'complete' and
              (observation == 'property_missing' or observation == 'empty' and denominator and reason != 'unknown'))
    observed = 'present' if present else 'absent' if absent else 'unknown'
    detail = observation if present else 'property_missing' if absent and observation == 'property_missing' else reason if absent else 'unknown'
    # Retrieval problems never erase a positive retained observation, nor establish absence.
    if access == 'denied' or retrieval == 'failed' and failure_reason == 'permission_denial':
        status, summary, action = 'permission_denied', 'The provider rejected access for this request.', 'Check authentication and the cited request-level access decision.'
    elif retrieval == 'failed':
        status, summary, action = ('transient_failure' if failure_reason == 'transient_failure' else 'retrieval_failed'), 'Retrieval failed; availability is unresolved.', 'Inspect the receipt and retry within the documented limits.'
    elif present:
        status = 'present_null' if observation == 'null' else 'present_zero' if observation == 'zero' else 'present_value'
        summary = {'null':'The property is present with a null value.','zero':'The property is present with a zero value.','value':'The property has a value.'}[observation]
        action = 'Use the source definition to interpret the observed value.'
    elif retrieval == 'incomplete':
        status, summary, action = 'retrieval_incomplete', 'Retrieval is incomplete; absence is not established.', 'Complete or resume retrieval for the same selector.'
    elif absent:
        status = 'property_missing' if observation == 'property_missing' else reason
        summary = {'property_missing':'The requested property is absent from the inspected complete record.',
            'outside_coverage':'The selector is outside the evidenced coverage.',
            'filtered_empty':'The complete filtered selection returned no matching records.',
            'not_collected':'The source states this data is not collected for the selector.',
            'unavailable_product':'The requested product is unavailable for the selector.'}[status]
        action = ('Check the requested source version and native property path.' if status == 'property_missing' else
                  'Review the selector and the cited coverage or product evidence.')
    else:
        status, summary, action = 'unknown', 'Availability is not established by the supplied evidence.', 'Obtain the missing access, coverage or complete retrieval evidence.'
    return {'profile':'okf-plus-private-data-availability.v1','distribution':'private','execution':False,
        'source':spec['source'],'selector':spec['selector'],'field':spec['field'],'evidence':evidence,
        'access':access,'expected_presence':expected,'observed_presence':observed,'retrieval':retrieval,
        'observation_detail':detail,'status':status,'summary':summary,'next_action':action,
        'expectation_gap': expected == 'expected' and absent,
        'denominator_known':denominator,'failure_reason':failure_reason}


def from_ngd_receipt(receipt, *, source, selector, field, evidence_reference,
                     access='unknown', expected_presence='unknown', observation='unknown',
                     denominator_known=False, empty_reason='unknown'):
    """Read receipt metadata only; never read feature payloads or invoke a provider.

    ``complete`` applies to the exact selection. Disposal/reacquisition state is
    incomplete. Every receipt must match source collection and selector ID
    equal to the canonical native selection SHA256 (or its urn:sha256 form). A
    failed HTTP/transport receipt never proves absent data.
    """
    if isinstance(receipt,(str,Path)):
        path=Path(receipt)
        if path.is_symlink(): raise ValueError('Symlink receipt refused')
        with path.open('rb') as stream: raw=stream.read(MAX_INPUT_BYTES+1)
        if len(raw)>MAX_INPUT_BYTES: raise ValueError('Receipt byte ceiling')
        receipt=json.loads(raw)
    else:
        raw=json.dumps(receipt,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    if not isinstance(receipt,dict): raise ValueError('Receipt must be object')
    _safe(receipt)
    if len(raw)>MAX_INPUT_BYTES: raise ValueError('Receipt byte ceiling')
    selection=receipt.get('selection')
    if not isinstance(selection,dict) or not isinstance(source,dict) or not isinstance(selector,dict):
        raise ValueError('Receipt must bind the requested collection and selector')
    _text(source.get('id')); _text(selector.get('id'))
    selection_digest=hashlib.sha256(json.dumps(selection,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    if (source.get('id') != selection.get('collection')
            or selector.get('id') not in {selection_digest,'urn:sha256:'+selection_digest}):
        raise ValueError('Receipt must bind the requested collection and selector')
    reason=receipt.get('reason')
    if access == 'unknown' and reason == 'http-failed' and receipt.get('lastHttpStatus') in (401, 403):
        access = 'denied'  # Observed request-level rejection, not a claim about PSGA licence rights.
    if receipt.get('payloadDiscarded') or reason=='needs-reacquisition': state='incomplete'
    elif receipt.get('complete') is True: state='complete'
    elif reason in {'http-failed','transport-failed','rate-limited','content-crs-mismatch','invalid-or-inconsistent-page'}: state='failed'
    else: state='incomplete'
    return assess_availability({'source':source,'selector':selector,'field':field,
        'evidence':[{'reference':evidence_reference,'receipt_sha256':hashlib.sha256(raw).hexdigest()}],
        'access':access,'expected_presence':expected_presence,'retrieval':state,'observation':observation,
        'denominator_known':denominator_known,'empty_reason':empty_reason,
        'failure_reason':('permission_denial' if reason == 'http-failed' and receipt.get('lastHttpStatus') in (401,403) else
                          'transient_failure' if reason in {'transport-failed','rate-limited'} else 'unknown')})


def from_query_plan(plan, *, source, selector, field, evidence_reference,
                    access='unknown', expected_presence='unknown'):
    """Candidate-route availability never establishes presence or missing data.

    Planner ``missing_fields`` means no admitted candidate covers those requests,
    not that a source record lacks a property. This adapter does not accept an
    observation override: a plan contains no observed feature data.
    """
    if not isinstance(plan,dict) or plan.get('profile') != 'okf-plus-offline-query-plan.v1' or plan.get('execution') is not False:
        raise ValueError('Supported inert candidate plan required')
    _safe(plan)
    raw=json.dumps(plan,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    if len(raw)>MAX_INPUT_BYTES: raise ValueError('Candidate plan byte ceiling')
    result=assess_availability({'source':source,'selector':selector,'field':field,
        'evidence':[{'reference':evidence_reference,'receipt_sha256':hashlib.sha256(raw).hexdigest()}],
        'access':access,'expected_presence':expected_presence,'retrieval':'not_attempted',
        'observation':'unknown'})
    result['summary']=('No proven retrieval candidate covers the request; data presence remains unknown.'
                       if plan.get('selected') is None else
                       'A candidate retrieval route is planned; data presence remains unknown.')
    result['next_action']='Review the requested output capabilities and route evidence, then retrieve the same selector.'
    return result
