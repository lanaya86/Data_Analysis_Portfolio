With cte AS(
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
    ORDER BY geo
    ),

cteA AS(
    SELECT 
        ctr, conv_rate, profit_per_click, geo
    FROM cte 
    WHERE variation = 'A'
),
cteB AS(
    SELECT 
        ctr, conv_rate, profit_per_click, geo
    FROM cte 
    WHERE variation = 'B')

    SELECT 
        c.variation, 
        c.geo, 
        a.ctr AS a_ctr, 
        b.ctr AS b_ctr,
        a.profit_per_click,
        b.profit_per_click,
        a.conv_rate,
        b.conv_rate
    FROM cte AS c
    JOIN cteA AS a
    USING(geo)
    JOIN cteB AS b
    USING(geo)
    WHERE 
        #a.ctr >= b.ctr
        #a.profit_per_click >= b.profit_per_click
        a.conv_rate >= b.conv_rate
    ORDER by c.geo     
