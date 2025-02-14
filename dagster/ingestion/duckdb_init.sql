-- landing tables need to be created before the initial backfill
CREATE SCHEMA IF NOT EXISTS landing;

CREATE TABLE IF NOT EXISTS landing.datagov_group
(
    id UUID
    , approval_status VARCHAR
    , created VARCHAR
    , description VARCHAR
    , display_name VARCHAR
    , image_display_url VARCHAR
    , image_url VARCHAR
    , is_organization BOOLEAN
    , "name" VARCHAR
    , num_followers BIGINT
    , package_count BIGINT
    , state VARCHAR
    , title VARCHAR
    , "type" VARCHAR
    , inserted_at TIMESTAMP
)
;

CREATE TABLE IF NOT EXISTS landing.datagov_license
(
    id VARCHAR
    , domain_content VARCHAR
    , domain_data VARCHAR
    , domain_software VARCHAR
    , "family" VARCHAR
    , is_generic VARCHAR
    , od_conformance VARCHAR
    , osd_conformance VARCHAR
    , maintainer VARCHAR
    , status VARCHAR
    , url VARCHAR
    , title VARCHAR
    , inserted_at TIMESTAMP
)
;

CREATE TABLE IF NOT EXISTS landing.datagov_organization
(
    id UUID
    , approval_status VARCHAR
    , created VARCHAR
    , description VARCHAR
    , display_name VARCHAR
    , image_display_url VARCHAR
    , image_url VARCHAR
    , is_organization BOOLEAN
    , "name" VARCHAR
    , num_followers BIGINT
    , package_count BIGINT
    , state VARCHAR
    , title VARCHAR
    , "type" VARCHAR
    , organization_type VARCHAR
    , inserted_at TIMESTAMPTZ
)
;

CREATE TABLE IF NOT EXISTS landing.datagov_package
(
    id UUID
    , author JSON
    , author_email JSON
    , creator_user_id UUID
    , isopen BOOLEAN
    , license_id VARCHAR
    , license_title VARCHAR
    , maintainer VARCHAR
    , maintainer_email VARCHAR
    , metadata_created VARCHAR
    , metadata_modified VARCHAR
    , "name" VARCHAR
    , notes VARCHAR
    , num_resources BIGINT
    , num_tags BIGINT
    , organization STRUCT(
        id UUID
        , "name" VARCHAR
        , title VARCHAR
        , "type" VARCHAR
        , description VARCHAR
        , image_url VARCHAR
        , created VARCHAR
        , is_organization BOOLEAN
        , approval_status VARCHAR
        , state VARCHAR
    )
    , owner_org UUID
    , private BOOLEAN
    , state VARCHAR
    , title VARCHAR
    , "type" VARCHAR
    , url JSON
    , "version" JSON
    , extras STRUCT(
        "key" VARCHAR
        , "value" JSON
    )[]
    , resources STRUCT(
        cache_last_updated JSON
        , cache_url JSON
        , created VARCHAR
        , description VARCHAR
        , format VARCHAR
        , hash VARCHAR
        , id UUID
        , last_modified JSON
        , metadata_modified VARCHAR
        , mimetype VARCHAR
        , mimetype_inner JSON
        , "name" VARCHAR
        , package_id UUID
        , "position" BIGINT
        , resource_type JSON
        , SIZE JSON
        , state VARCHAR
        , url VARCHAR
        , url_type JSON
        , conformsTo VARCHAR
        , describedBy VARCHAR
        , describedByType VARCHAR
        , no_real_name BOOLEAN
        , resource_locator_function VARCHAR
        , resource_locator_protocol VARCHAR
    )[]
    , tags STRUCT(
        display_name VARCHAR
        , id UUID
        , "name" VARCHAR
        , state VARCHAR
        , vocabulary_id JSON
    )[]
    , "groups" STRUCT(
        description VARCHAR
        , display_name VARCHAR
        , id UUID
        , image_display_url VARCHAR
        , "name" VARCHAR
        , title VARCHAR
    )[]
    , relationships_as_subject JSON[]
    , relationships_as_object JSON[]
    , license_url VARCHAR
    , inserted_at TIMESTAMP
)
;

CREATE TABLE IF NOT EXISTS landing.date_spine
(
    calendar_date DATE
)
;