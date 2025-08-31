Model (
    name staging_features,
    kind view,
    audits (
        not_null(columns := (feature_id))

    )
);

select 
    feature_id,
    feature_name,
    feature_description,
    feature_category
from raw_features