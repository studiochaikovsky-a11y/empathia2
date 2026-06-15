-- Empathia CRM — Cloudflare D1 schema
-- Run: npx wrangler d1 execute empathia-crm --file schema.sql --remote

CREATE TABLE IF NOT EXISTS leads (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  TEXT    DEFAULT (datetime('now')),
  source      TEXT    DEFAULT 'empathia-seychelles.com',
  name        TEXT,
  phone       TEXT,
  email       TEXT,
  interest    TEXT,
  message     TEXT,
  page        TEXT,
  status      TEXT    DEFAULT 'new',
  type        TEXT    DEFAULT 'client'
);

CREATE TABLE IF NOT EXISTS notes (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id     INTEGER NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  created_at  TEXT    DEFAULT (datetime('now')),
  text        TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_leads_status     ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_source     ON leads(source);
CREATE INDEX IF NOT EXISTS idx_leads_created    ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notes_lead_id    ON notes(lead_id);
