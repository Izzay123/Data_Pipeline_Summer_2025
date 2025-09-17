MODEL (
    name dim_features,
    kind SCD_TYPE_1
);

SELECT
    feature_id AS feature_key,
    feature_id,
    feature_name,
    feature_description,
    feature_category,
    CURRENT_TIMESTAMP AS last_updated
FROM staging_features
ORDER BY feature_id