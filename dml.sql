table customer;
table car;



SELECT *
FROM
    public.service;

SELECT *
FROM
    public.service
WHERE
        car_id IN (
                  SELECT
                      car_id
                  FROM
                      public.purchase );


SELECT
    service_name,
    CASE
        WHEN service_cost < 50 THEN 'Low Cost'
        WHEN service_cost >= 50 AND service_cost <= 100 THEN 'Medium Cost'
        WHEN service_cost > 100 THEN 'High Cost'
        END AS cost_category
FROM
    public.service;

SELECT
    c.first_name,
    c.last_name,
    CASE
        WHEN total_service_cost >= 1000 THEN 'High'
        WHEN total_service_cost >= 500 THEN 'Medium'
        ELSE 'Low'
        END AS service_cost_category
FROM
    customer                                   c
        LEFT JOIN (
                  SELECT
                      cs.customer_id,
                      SUM(s.service_cost) AS total_service_cost
                  FROM
                      customer_service cs
                          JOIN service s ON cs.service_id = s.service_id
                  GROUP BY cs.customer_id ) AS service_costs ON c.customer_id = service_costs.customer_id;

