export async function onRequestGet({ env }) {
  await env.DB.prepare(
    `CREATE TABLE IF NOT EXISTS analytics_events (
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
    )`
  ).run();

  const [
    byStatus, byVilla, bySource, last30, byUtmSource, byUtmCampaign,
    clientTotals, clientsByVilla, upcomingPayments, overduePayments, eventTotals,
  ] = await Promise.all([
    env.DB.prepare(
      'SELECT status, COUNT(*) AS count FROM leads GROUP BY status ORDER BY count DESC'
    ).all(),
    env.DB.prepare(
      `SELECT interest, COUNT(*) AS count FROM leads
       WHERE interest != '' AND interest IS NOT NULL
       GROUP BY interest ORDER BY count DESC`
    ).all(),
    env.DB.prepare(
      'SELECT source, COUNT(*) AS count FROM leads GROUP BY source ORDER BY count DESC'
    ).all(),
    env.DB.prepare(
      "SELECT COUNT(*) AS count FROM leads WHERE created_at >= datetime('now', '-30 days')"
    ).first(),
    env.DB.prepare(
      `SELECT utm_source, COUNT(*) AS count FROM leads
       WHERE utm_source != '' AND utm_source IS NOT NULL
       GROUP BY utm_source ORDER BY count DESC LIMIT 10`
    ).all(),
    env.DB.prepare(
      `SELECT utm_campaign, COUNT(*) AS count FROM leads
       WHERE utm_campaign != '' AND utm_campaign IS NOT NULL
       GROUP BY utm_campaign ORDER BY count DESC LIMIT 10`
    ).all(),
    env.DB.prepare(
      `SELECT
         COUNT(*) AS clients,
         COALESCE(SUM(price), 0) AS contracted,
         COALESCE((SELECT SUM(amount) FROM payments WHERE status = 'paid'), 0) AS collected
       FROM clients WHERE status != 'cancelled'`
    ).first(),
    env.DB.prepare(
      `SELECT villa, COUNT(*) AS count, COALESCE(SUM(price), 0) AS value
       FROM clients WHERE status != 'cancelled' AND villa != '' AND villa IS NOT NULL
       GROUP BY villa ORDER BY count DESC`
    ).all(),
    env.DB.prepare(
      `SELECT p.id, p.milestone, p.amount, p.currency, p.due_date, c.id AS client_id, c.name AS client_name, c.villa
       FROM payments p JOIN clients c ON c.id = p.client_id
       WHERE p.status = 'pending' AND p.due_date IS NOT NULL
         AND p.due_date <= date('now', '+30 days')
       ORDER BY p.due_date ASC LIMIT 10`
    ).all(),
    env.DB.prepare(
      `SELECT COUNT(*) AS count FROM payments
       WHERE status = 'pending' AND due_date IS NOT NULL AND due_date < date('now')`
    ).first(),
    env.DB.prepare(
      `SELECT event, COUNT(*) AS count FROM analytics_events
       WHERE created_at >= datetime('now', '-30 days')
       GROUP BY event ORDER BY count DESC`
    ).all(),
  ]);

  const contracted = clientTotals?.contracted ?? 0;
  const collected  = clientTotals?.collected ?? 0;

  return new Response(
    JSON.stringify({
      ok: true,
      by_status: byStatus.results,
      by_villa:  byVilla.results,
      by_source: bySource.results,
      last_30_days: last30?.count ?? 0,
      by_utm_source:   byUtmSource.results,
      by_utm_campaign: byUtmCampaign.results,
      events_30_days: eventTotals.results,
      sales: {
        clients: clientTotals?.clients ?? 0,
        contracted,
        collected,
        outstanding: Math.max(0, contracted - collected),
        by_villa: clientsByVilla.results,
        upcoming_payments: upcomingPayments.results,
        overdue_count: overduePayments?.count ?? 0,
      },
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
