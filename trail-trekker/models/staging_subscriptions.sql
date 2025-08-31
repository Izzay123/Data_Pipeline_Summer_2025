Model (
    name staging_subscriptions,
    kind view,
    audits (
        not_null(columns := (subscription_id, customer_id, plan_id))
    )
);

select 
    subscription_id,
    customer_id,
    plan_id,
    billing_cycle,
    subscription_start_date,
    coalesce(
        TRY_CAST(subscription_end_date AS DATE),
        DATE '1900-01-01'
    ) as subscription_end_date,
    status,
    coalesce(
        TRY_CAST(next_billing_date AS DATE),
        DATE '1900-01-01'
    ) as next_billing_date,
    payment_method
from raw_subscriptions