-- Additive pilot tables. Never alter the existing captured-CPIH snapshot.
CREATE TABLE IF NOT EXISTS sites_pilot_allowance_v1 (
  provider TEXT PRIMARY KEY,
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1)),
  used INTEGER NOT NULL CHECK(used >= 0),
  maximum INTEGER NOT NULL CHECK(maximum BETWEEN 1 AND 200),
  window_start INTEGER NOT NULL,
  window_used INTEGER NOT NULL CHECK(window_used >= 0)
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS sites_pilot_receipts_v1 (
  receipt_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  result_json TEXT NOT NULL CHECK(length(CAST(result_json AS BLOB)) <= 65536)
);
--> statement-breakpoint
-- Reapplying this migration cannot refill an allowance or re-enable a disabled provider.
INSERT INTO sites_pilot_allowance_v1 (provider, enabled, used, maximum, window_start, window_used)
VALUES ('os-names', 1, 0, 120, 0, 0),
       ('os-open-data', 1, 0, 120, 0, 0),
       ('ons-cpih', 1, 0, 120, 0, 0),
       ('ons-geography', 1, 0, 120, 0, 0)
ON CONFLICT(provider) DO NOTHING;
