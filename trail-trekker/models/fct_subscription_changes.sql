Model (
    name fct_subscription_changes,
    kind VIEW,
    audits (
        not_null(columns := (subscription_id, customer_id, plan_id))
    )
);

SELECT
    s.customer_id,
    s.subscription_id,
    s.plan_id,
    s.subscription_start_date,
    s.subscription_end_date,
    s.status,
    s.billing_cycle,

    -- Plan details
    p.plan_name,
    p.price as monthly_revenue,
    p.plan_level,
    p.max_hikes_per_month,

    -- Calculated metrics
    CASE
        WHEN s.subscription_end_date = DATE '1900-01-01'
        THEN DATE_DIFF('day', TRY_CAST(s.subscription_start_date AS DATE), CURRENT_DATE)
        ELSE DATE_DIFF('day', TRY_CAST(s.subscription_start_date AS DATE), s.subscription_end_date)
    END as subscription_duration_days,

    CASE
        WHEN s.status = 'active' AND s.subscription_end_date = DATE '1900-01-01'
        THEN TRUE
        ELSE FALSE
    END as is_active,

    -- Revenue calculation
    CASE
        WHEN s.billing_cycle = 'monthly' THEN p.price
        WHEN s.billing_cycle = 'yearly' THEN p.price * 12
        ELSE p.price
    END as total_subscription_value

FROM staging_subscriptions s
LEFT JOIN staging_plans p ON s.plan_id = p.plan_id
ORDER BY s.customer_id, s.subscription_start_date DESC