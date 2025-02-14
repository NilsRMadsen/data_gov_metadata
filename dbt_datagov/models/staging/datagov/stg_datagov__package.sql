with packages as (

    select *
    from {{ source('datagov', 'package') }}

)

, renamed as (

    select
        id as package_id
        , "name"
        , title
        , notes
        , organization.id as organization_id
        , maintainer
        , maintainer_email
        , "state" as dataset_status
        , "private" as is_private
        , isopen as is_open
        , license_id
        , tags
        , groups
        , strptime(metadata_created, '%xT%X.%f') as created_at
        , strptime(metadata_modified, '%xT%X.%f') as modified_at
    from packages

)

select *
from renamed