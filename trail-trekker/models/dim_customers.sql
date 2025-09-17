MODEL (
    name dim_customers,
    kind VIEW
);

SELECT
    customer_id,
    username,
    email,
    first_name,
    last_name,
    location_city,
    location_state,
    profile_created_date
FROM staging_customers