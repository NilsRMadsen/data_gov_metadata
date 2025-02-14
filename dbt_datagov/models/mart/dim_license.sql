with licenses as (

    select *
    from {{ ref('stg_datagov__license') }}

)

, dim_license as (

    select
        license_id
        , title
        , license_status
        , domain_content
        , domain_data
        , domain_software
        , is_generic
        , od_conformance
        , osd_conformance
        , license_url
    from licenses

)

select *
from dim_license