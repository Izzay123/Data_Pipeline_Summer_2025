MODEL (
    name dim_subscriptions,
    kind view
);

SELECT
    subscription_id,
    customer_id,
    plan_id,
    billing_cycle,
    subscription_start_date,
    status
FROM staging_subscriptions;