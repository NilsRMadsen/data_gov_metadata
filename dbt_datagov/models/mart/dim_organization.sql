with organizations as (

    select *
    from {{ ref('stg_datagov__organization') }}

)

, dim_organization as (

    select
        organization_id
        , "name"
        , title
        , organization_type
        , "description"
        , organization_status
        , approval_status
        , created_at
    from organizations

)

select *
from dim_organization