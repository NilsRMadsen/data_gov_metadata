with source as (

    select *
    from {{ source('datagov', 'group') }}

)

, renamed as (

    select
        id as group_id
        , name
        , title
        , display_name
        , description
        , state as group_status
        , approval_status
        , strptime(created, '%xT%X.%f') as created_at
        -- , is_organization
        -- , num_followers
        -- , type
        -- , image_display_url
        -- , image_url
        -- , package_count
        -- , inserted_at
    from source

)

select *
from renamed