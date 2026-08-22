- Add a repository-only QUAL-206 Stage 2 threat record that maps all 30 baseline
  risks to implemented controls and residual gates, plus a non-accepting disposition
  for the three retained unfixed High gateway-image findings and content-addressed
  local receipts for the seven applicable evaluation cases. This records a release
  hold; it does not activate the service, accept risk or claim `v0.2.0` readiness.
- Restrict the approved T04 cache to network failures privately classified by the
  module-owned fixed HTTPS transport or HTTP 500 to 599 responses. Proxies, public
  constructor errors, malformed parser responses, incomplete response bodies and
  unknown resolver failures stay receipt-free; recognised DNS failures and genuine
  pre-response connection resets retain their reviewed network classification.
  Require the exact pristine adapter that performed the current call, bind the outage
  proof to that adapter and consume it once so substituted methods, subclasses and
  captured-fault replays cannot authorise a later cache receipt.
