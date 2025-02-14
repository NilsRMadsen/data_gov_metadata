with packages as (

    select *
    from {{ ref('stg_datagov__package') }}

)

-- the "tags" field is an array of dictionaries, so we first need to unnest the array...
, unnested as (

    select
        package_id
        , unnest(tags) as tag
    from packages

)

-- then we can extract the tag name
-- tags can be duplicated, so we need to dedupe to ensure a correct many-to-many mapping
, flattened_deduped as (

    select distinct
        package_id
        , trim(tag.name) as tag_name
    from unnested
    where
        trim(tag.name) != ''

)

select *
from flattened_deduped