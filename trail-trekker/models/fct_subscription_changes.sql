Model (
    name  fct_subscription_changes,
    kind VIEW,
        audits (
        not_null(columns := (subscription_id, customer_id))
    )
);


Select customer_id ,
        subscription_id,
        plan_id as current_plan_id,
        subscription_start_date,
        subscription_end_date,
    from staging_subscriptions
    order by customer_id, subscription_id, subscription_start_date desc