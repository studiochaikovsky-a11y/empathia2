-- Additive: existing forms continue working until the new site is deployed.
ALTER TABLE leads ADD COLUMN attribution_json TEXT NOT NULL DEFAULT '{}';
