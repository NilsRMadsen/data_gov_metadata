with packages as (

    select *
    from {{ ref('stg_datagov__package') }}

)

, fact_dataset as (

    select
        package_id
        , "name"
        , title
        , notes
        , organization_id
        , maintainer
        , maintainer_email
        , dataset_status
        , is_private
        , is_open
        , license_id
        , created_at
        , modified_at
    from packages

)

select *
from fact_dataset