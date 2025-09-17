MODEL (
  name dim_features,
  kind VIEW
);

SELECT
  feature_id AS feature_key,
  feature_id,
  feature_name,
  feature_description,
  feature_category
FROM staging_features
ORDER BY
  feature_id