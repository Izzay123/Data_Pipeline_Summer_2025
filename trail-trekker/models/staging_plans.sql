MODEL (
  name staging_plans,
  kind VIEW
);

SELECT
  plan_id,
  plan_name,
  COALESCE(TRY_CAST(plan_level AS INT), 0) AS plan_level,
  COALESCE(TRY_CAST(price AS DOUBLE), 0.0) AS price,
  COALESCE(TRY_CAST(max_hikes_per_month AS INT), 0) AS max_hikes_per_month,
  COALESCE(TRY_CAST(photo_storage_gb AS INT), 0) AS photo_storage_gb,
  description,
  COALESCE(TRY_CAST(created_at AS DATE), '1900-01-01'::DATE) AS created_at
FROM raw_plans