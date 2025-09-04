MODEL (
    name staging_customers,
    kind VIEW,
        audits (
        not_null(columns := (customer_id))

    )
);

SELECT
    customer_id,
    username,
    email,
    COALESCE(phone, '000-0000') AS phone,
    first_name,
    last_name,
    COALESCE(
        TRY_CAST(date_of_birth AS DATE),
        DATE '1900-01-01'
    ) AS date_of_birth,
    preferred_difficulty,
    location_city,
    location_state,
    location_country,
    COALESCE(
        TRY_CAST(profile_created_date AS DATE),
        DATE '1900-01-01'
    ) AS profile_created_date,
    COALESCE(
        TRY_CAST(total_hikes_logged AS INT),
        0
    ) AS total_hikes_logged,
    favorite_trail_type
FROM raw_customers