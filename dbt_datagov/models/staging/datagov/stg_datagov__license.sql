with datagov_license as (

    select *
    from {{ source('datagov', 'license') }}

)

, renamed as (

    select
        trim(id) as license_id
        , trim(title) as title
        , trim("status") as license_status
        , domain_content::boolean as domain_content
        , domain_data::boolean as domain_data
        , domain_software::boolean as domain_software
        , is_generic::boolean as is_generic
        , trim(od_conformance) as od_conformance
        , trim(osd_conformance) as osd_conformance
        , "url" as license_url
        -- , maintainer
        -- , family
        -- , inserted_at
    from datagov_license

)

select *
from renamed