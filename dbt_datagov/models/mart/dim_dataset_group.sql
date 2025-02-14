with packages as (

    select *
    from {{ ref('stg_datagov__package') }}

)

, groups as (

    select *
    from {{ ref('stg_datagov__group') }}

)

-- the "groups" field is an array of dictionaries, so we first need to unnest the array...
, unnested as (

    select
        package_id
        , unnest(groups) as package_group
    from packages

)

-- then we can extract the tag name
-- we can also dedupe to ensure a correct many-to-many mapping
, flattened_deduped as (

    select distinct
        package_id
        , package_group.id as group_id
    from unnested

)

, joined as (

    select
        flattened_deduped.package_id
        , flattened_deduped.group_id
        , groups.name as group_name
        , groups.title as group_title
    from flattened_deduped
    left join groups
        on flattened_deduped.group_id = groups.group_id

)

select *
from joined