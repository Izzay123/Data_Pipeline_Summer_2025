MODEL (
  name dim_plans,
  kind VIEW
);

SELECT
  plan_id AS plan_key,
  plan_id,
  plan_name,
  plan_level,
  price,
  max_hikes_per_month,
  photo_storage_gb,
  description,
  created_at
FROM staging_plans
ORDER BY
  plan_id