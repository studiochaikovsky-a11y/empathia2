-- Empathia CRM — fix: leads.utm_source/utm_medium/utm_campaign were referenced
-- by functions/api/lead.js and functions/api/crm/stats.js but never existed in
-- schema.sql, so every website lead insert has been silently failing the UTM
-- bind and (depending on D1 strictness) may have failed the whole insert.
-- Run: npx wrangler d1 execute empathia-crm --file schema_fix_utm.sql --remote
--
-- If you see "duplicate column name" errors below, the columns already exist —
-- that's fine, ignore those specific errors and proceed to schema_v2.sql.

ALTER TABLE leads ADD COLUMN utm_source TEXT;
ALTER TABLE leads ADD COLUMN utm_medium TEXT;
ALTER TABLE leads ADD COLUMN utm_campaign TEXT;
