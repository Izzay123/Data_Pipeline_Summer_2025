MODEL (
  name staging_features,
  kind VIEW,
  audits (
    NOT_NULL(columns := (
      feature_id
    ))
  )
);

SELECT
  feature_id,
  feature_name,
  feature_description,
  feature_category
FROM raw_features