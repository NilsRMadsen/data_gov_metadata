from pathlib import Path

# destination database
DB_PATH = Path(__file__).absolute().parent.parent.parent / "dbt_datagov/database/data_gov_metadata.duckdb"
LANDING_SCHEMA = 'landing'

# API
BASE_URL = 'https://catalog.data.gov/api/3/'

ENDPOINTS = {
    'organization': {
        'endpoint': 'action/organization_list'
        , 'docs': 'https://docs.ckan.org/en/latest/api/#ckan.logic.action.get.organization_list'
        , 'pagination': {
            'limit_parameter': 'limit'
            , 'limit_value': 100
            , 'offset_parameter': 'offset'
            , 'max_pages': None
        }
        , 'params': {
            'sort': 'name asc'
            , 'all_fields': True
        }
        , 'path_to_records': ['result']
        , 'destination_table': 'datagov_organization'
        , 'primary_key': 'id'
        , 'update_mode': 'full_reload'
        , 'write_mode': 'single_batch'
    }

    , 'package': {
        'endpoint': 'action/package_search'
        , 'docs': 'https://docs.ckan.org/en/latest/api/#ckan.logic.action.get.package_search'
        , 'pagination': {
            'limit_parameter': 'rows'
            , 'limit_value': 1000
            , 'offset_parameter': 'start'
            , 'max_pages': None
        }
        , 'params': {
            'sort': 'metadata_modified desc'
            , 'fq': 'metadata_modified:[NOW-5DAY/DAY TO NOW]'
        }
        , 'backfill_params': {
            'sort': 'metadata_created asc'
        }
        , 'path_to_records': ['result', 'results']
        , 'fields': [
            'author'
            , 'author_email'
            , 'creator_user_id'
            , 'id'
            , 'isopen'
            , 'license_id'
            , 'license_title'
            , 'maintainer'
            , 'maintainer_email'
            , 'metadata_created'
            , 'metadata_modified'
            , 'name'
            , 'notes'
            , 'organization'
            , 'owner_org'
            , 'private'
            , 'state'
            , 'title'
            , 'type'
            , 'url'
            , 'version'
            , 'tags'
            , 'groups'
        ]
        , 'destination_table': 'datagov_package'
        , 'primary_key': 'id'
        , 'update_mode': 'upsert_replace'
        , 'write_mode': 'page_chunks'
    }

    , 'group': {
        'endpoint': 'action/group_list'
        , 'docs': 'https://docs.ckan.org/en/latest/api/#ckan.logic.action.get.group_list'
        , 'pagination': {
            'limit_parameter': 'limit'
            , 'limit_value': 1000
            , 'offset_parameter': 'offset'
            , 'max_pages': None
        }
        , 'params': {
            'all_fields': True
        }
        , 'path_to_records': ['result']
        , 'destination_table': 'datagov_group'
        , 'primary_key': 'id'
        , 'update_mode': 'full_reload'
        , 'write_mode': 'single_batch'
    }

    , 'license': {
        'endpoint': 'action/license_list'
        , 'docs': 'https://docs.ckan.org/en/latest/api/#ckan.logic.action.get.license_list'
        , 'pagination': {
            'limit_parameter': 'limit'
            , 'limit_value': 1000
            , 'offset_parameter': 'offset'
            , 'max_pages': 1
        }
        , 'params': {
            'all_fields': True
        }
        , 'path_to_records': ['result']
        , 'destination_table': 'datagov_license'
        , 'primary_key': 'id'
        , 'update_mode': 'full_reload'
        , 'write_mode': 'single_batch'
    }
}
