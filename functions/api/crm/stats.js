export async function onRequestGet({ env }) {
  const [byStatus, byVilla, bySource, last30] = await Promise.all([
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
  ]);

  return new Response(
    JSON.stringify({
      ok: true,
      by_status: byStatus.results,
      by_villa:  byVilla.results,
      by_source: bySource.results,
      last_30_days: last30?.count ?? 0,
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
