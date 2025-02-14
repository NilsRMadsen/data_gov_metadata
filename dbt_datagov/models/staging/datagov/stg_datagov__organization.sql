with source as (

    select *
    from {{ source('datagov', 'organization') }}

)

, renamed as (

    select
        id as organization_id
        , "name"
        , title
        , organization_type
        , "description"
        , "state" as organization_status
        , approval_status
        , strptime(created, '%xT%X.%f') as created_at
        -- , display_name
        -- , num_followers
        -- , package_count
        -- , image_display_url
        -- , image_url
        -- , type
        -- , is_organization
        -- , inserted_at
    from source

)

select *
from renamed