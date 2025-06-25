SELECT 
    variation,
    geo,
    SUM(impressions) AS impressions_sum,
    SUM(clicks) AS clicks_sum,
    ROUND(SUM(profit), 2) AS profit_sum,
    ROUND(SUM(clicks) / SUM(impressions) * 100.00, 2) AS ctr,
    SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) AS conversions,
    ROUND(SUM(profit) / SUM(clicks), 2) AS profit_per_click,
    ROUND(SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) * 100.00 / SUM(clicks), 2) AS conv_rate

FROM adperformancedataset.ad_performance_test
GROUP BY variation, geo
--HAVING SUM(impressions) >= 500
  -- AND SUM(clicks) >= 30
ORDER BY geo
