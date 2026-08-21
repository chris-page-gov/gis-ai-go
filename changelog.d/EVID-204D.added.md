- Added an inactive, ledger-linked idempotency reconciliation index for
  `data.query`, a caller-key request wrapper and `evidence.inspect` v2 lookup.
  Pending, completed and conflicting retries fail closed without another provider
  execution or ledger event, and `QUAL-206-HOST-015` passes a deterministic restart
  test. Mounted data faces require the exact linked inspector and use server-owned
  request identities. Raw keys and result material are not retained; production
  activation remains empty and no live-host or deployment claim is made.
