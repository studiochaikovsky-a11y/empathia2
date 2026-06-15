export async function onRequestGet({ env }) {
  const [byStatus, byVilla, bySource, last30, byUtmSource, byUtmCampaign] = await Promise.all([
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
  ]);

  return new Response(
    JSON.stringify({
      ok: true,
      by_status: byStatus.results,
      by_villa:  byVilla.results,
      by_source: bySource.results,
      last_30_days: last30?.count ?? 0,
      by_utm_source:   byUtmSource.results,
      by_utm_campaign: byUtmCampaign.results,
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}
