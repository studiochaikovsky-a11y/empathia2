-- Empathia CRM — Cloudflare D1 schema
-- Run: npx wrangler d1 execute empathia-crm --file schema.sql --remote

CREATE TABLE IF NOT EXISTS leads (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  TEXT    DEFAULT (datetime('now')),
  source      TEXT    DEFAULT 'empathia-seychelles.com',
  country     TEXT,
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
CREATE TABLE IF NOT EXISTS analytics_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event TEXT NOT NULL,
  page TEXT DEFAULT '',
  page_title TEXT DEFAULT '',
  label TEXT DEFAULT '',
  href TEXT DEFAULT '',
  interest TEXT DEFAULT '',
  utm_source TEXT DEFAULT '',
  utm_medium TEXT DEFAULT '',
  utm_campaign TEXT DEFAULT '',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
