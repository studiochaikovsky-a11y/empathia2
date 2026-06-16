-- Empathia CRM — schema v2: Clients + Sales Plans (payment milestones)
-- Run: npx wrangler d1 execute empathia-crm --file schema_v2.sql --remote

-- A client is created once a lead converts into a buyer. It can optionally
-- reference the original lead it came from.
CREATE TABLE IF NOT EXISTS clients (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT    DEFAULT (datetime('now')),
  lead_id       INTEGER REFERENCES leads(id) ON DELETE SET NULL,
  name          TEXT    NOT NULL,
  phone         TEXT,
  email         TEXT,
  villa         TEXT,                          -- 'Villa Jane' / 'Villa Anna' / 'Villa Georgette' / custom
  plot          TEXT,                          -- plot number / identifier
  price         REAL    DEFAULT 0,
  currency      TEXT    DEFAULT 'USD',
  contract_date TEXT,
  agent         TEXT,                          -- referring agent, optional
  status        TEXT    DEFAULT 'active'        -- active / completed / cancelled
);

-- Each row is one milestone in a client's staged payment plan
-- (Reservation, Contract, Foundation, Frame, Completion, or custom).
CREATE TABLE IF NOT EXISTS payments (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id   INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  milestone   TEXT    NOT NULL,
  amount      REAL    NOT NULL DEFAULT 0,
  currency    TEXT    DEFAULT 'USD',
  due_date    TEXT,
  paid_date   TEXT,
  status      TEXT    DEFAULT 'pending',        -- pending / paid / overdue
  sort_order  INTEGER DEFAULT 0
);

-- Notes attached to a client (separate table from leads.notes — a client may
-- exist without ever having had a lead note thread, and vice versa).
CREATE TABLE IF NOT EXISTS client_notes (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id   INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  created_at  TEXT    DEFAULT (datetime('now')),
  text        TEXT    NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_clients_status      ON clients(status);
CREATE INDEX IF NOT EXISTS idx_clients_villa        ON clients(villa);
CREATE INDEX IF NOT EXISTS idx_clients_lead_id       ON clients(lead_id);
CREATE INDEX IF NOT EXISTS idx_payments_client_id    ON payments(client_id);
CREATE INDEX IF NOT EXISTS idx_payments_due_date     ON payments(due_date);
CREATE INDEX IF NOT EXISTS idx_payments_status        ON payments(status);
CREATE INDEX IF NOT EXISTS idx_client_notes_client_id ON client_notes(client_id);
