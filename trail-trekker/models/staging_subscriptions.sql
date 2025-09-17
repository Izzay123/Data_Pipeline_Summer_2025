MODEL (
  name staging_subscriptions,
  kind VIEW,
  audits (
    NOT_NULL(columns := (subscription_id, customer_id, plan_id))
  )
);

SELECT
  subscription_id,
  customer_id,
  plan_id,
  billing_cycle,
  subscription_start_date,
  COALESCE(TRY_CAST(subscription_end_date AS DATE), '1900-01-01'::DATE) AS subscription_end_date,
  status,
  COALESCE(TRY_CAST(next_billing_date AS DATE), '1900-01-01'::DATE) AS next_billing_date,
  payment_method
FROM subscriptions