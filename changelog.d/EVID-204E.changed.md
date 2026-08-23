- Return every successful `evidence.inspect` lookup as a
  `gis-ai-go.evidence-inspect-result.v3` with a dedicated, verifiable current-call
  receipt. The receipt binds the anonymous-open inspection policy, safe lookup
  digest, inspected evidence identities, software and receipt-free result core but
  remains inline-only, not attested and creates no ledger event. Existing v1 and v2
  request and stored-record bytes remain unchanged; production activation stays
  empty and nothing is deployed or released.
