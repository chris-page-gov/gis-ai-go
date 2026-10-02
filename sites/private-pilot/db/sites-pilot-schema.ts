import { sql } from 'drizzle-orm';
import { check, integer, primaryKey, sqliteTable, text } from 'drizzle-orm/sqlite-core';

// Metadata for the published additive DDL; no migration or provisioning at request time.
// Table-level keys preserve SQLite's original TEXT PRIMARY KEY nullability.
export const sitesPilotAllowance = sqliteTable('sites_pilot_allowance_v1', {
  provider: text('provider'),
  enabled: integer('enabled').notNull(),
  used: integer('used').notNull(),
  maximum: integer('maximum').notNull(),
  windowStart: integer('window_start').notNull(),
  windowUsed: integer('window_used').notNull(),
}, (table) => [
  primaryKey({ columns: [table.provider] }),
  check('sites_pilot_enabled', sql`${table.enabled} IN (0,1)`),
  check('sites_pilot_used', sql`${table.used} >= 0`),
  check('sites_pilot_maximum', sql`${table.maximum} BETWEEN 1 AND 200`),
  check('sites_pilot_window_used', sql`${table.windowUsed} >= 0`),
]);

export const sitesPilotReceipts = sqliteTable('sites_pilot_receipts_v1', {
  receiptId: text('receipt_id'),
  createdAt: text('created_at').notNull(),
  resultJson: text('result_json').notNull(),
}, (table) => [
  primaryKey({ columns: [table.receiptId] }),
  check('sites_pilot_result_bytes', sql`length(CAST(${table.resultJson} AS BLOB)) <= 65536`),
]);
