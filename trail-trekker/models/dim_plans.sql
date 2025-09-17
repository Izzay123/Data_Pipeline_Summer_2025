MODEL (
    name dim_plans,
    kind SCD_TYPE_1
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
    created_at,
    CURRENT_TIMESTAMP AS last_updated
FROM staging_plans
ORDER BY plan_id