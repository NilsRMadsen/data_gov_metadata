try:
    from . import config, utilities
except ImportError:
    import config, utilities

import argparse
import duckdb
import json
import requests
import time

from io import StringIO
from time import sleep


def get_with_retries(url, params=None, stream=False, max_retries=5):
    '''
    Make a GET request to an API, with retries if necessary
    '''
    for retry_num in range(1, max_retries+1):
        r = requests.get(url, params=params, stream=stream)
        
        if r.ok:
            return r
        
        else:
            # server errors should lead to retries
            if r.status_code >= 500:
                print(f'API returned status code {r.status_code} with reason "{r.reason}". Retrying.')

            # bad request errors should throw an exception
            elif r.status_code >= 400:
                raise RuntimeError(f'API returned status code {r.status_code} with reason "{r.reason}".')
            
            if retry_num >= max_retries:
                raise RuntimeError('Max retries exhausted when making GET request to API.')

            sleep(3)


def write_to_duckdb(conn, records, dest_table, primary_key, update_mode):
    '''
    Write API records to the DuckDB data warehouse.

    Parameters:
    - conn: The active DuckDB connection
    - records: (list of dicts) The records to write to the database
    - dest_table: (str) The schema.table to write the data into
    - primary_key: (str) The name of the primary key for upserts.
    - update_mode: (str) How to update the destination table with the new data

    '''
    with StringIO() as f:
        json.dump(records, f)
        f.seek(0)

        data = conn.read_json(f)
    
        # for small tables of mutable data, full reloads are simple and self-healing
        if update_mode == 'full_reload':
            conn.sql(f'''
                        
                BEGIN TRANSACTION;

                DELETE FROM {dest_table}
                ;

                INSERT INTO {dest_table}
                BY NAME
                SELECT
                    *
                    , CURRENT_LOCALTIMESTAMP() as inserted_at
                FROM data
                ;

                COMMIT;

            ''')
        
        # for larger datasets that should be updated incrementally, upserting with replacement
        # can yield some self-healing while keeping compute and API usage reasonable
        elif update_mode == 'upsert_replace':
            conn.sql(f'''
                
                BEGIN TRANSACTION;
                
                DELETE FROM {dest_table}
                WHERE
                    {primary_key} IN (SELECT {primary_key} FROM data)
                ;

                INSERT INTO {dest_table}
                BY NAME
                SELECT
                    *
                    , CURRENT_LOCALTIMESTAMP() as inserted_at
                FROM data
                ;

                COMMIT;

            ''')

        # for development purposes only - do not use in production due to risk of schema drift
        elif update_mode == 'create_table':
            conn.sql(f'''
                        
                CREATE OR REPLACE TABLE {dest_table} AS
                SELECT
                    *
                    , CURRENT_LOCALTIMESTAMP() as inserted_at
                FROM data

            ''')
        
    print(f'    Wrote {len(records)} records to DuckDB')


def run_pipeline(target_endpoint, backfill=False):

    start_time = time.time()
    print(f'\nStarting pipeline for endpoint "{target_endpoint}"\n')

    # build query parameters from config
    endpoint_config = config.ENDPOINTS[target_endpoint]

    if backfill and endpoint_config.get('backfill_params'):
        params = endpoint_config['backfill_params']
    else:
        params = endpoint_config.get('params', dict())
    
    limit_parameter = endpoint_config['pagination']['limit_parameter']
    params[limit_parameter] = endpoint_config['pagination']['limit_value']

    offset_parameter = endpoint_config['pagination']['offset_parameter']
    params[offset_parameter] = 0

    # build database write parameters from config
    dest_table = f'{config.LANDING_SCHEMA}.{endpoint_config['destination_table']}'
    primary_key = endpoint_config.get('primary_key')
    update_mode = endpoint_config['update_mode']
    write_mode = endpoint_config['write_mode']

    # get records from API
    url = config.BASE_URL + endpoint_config['endpoint']
    records = list()
    page_num = 1

    with duckdb.connect(config.DB_PATH) as conn:

        # loop through API pages
        max_pages = endpoint_config['pagination'].get('max_pages')

        while True:

            with get_with_retries(url, params=params, stream=True) as r:
                page_records = utilities.find(json.load(r.raw), endpoint_config['path_to_records'])

            num_records = len(page_records)
            print(f'Collected {num_records} records from page {page_num}')

            # if there are no records on this page, we have gone past the last page
            if num_records == 0:
                print('Pagination terminated')
                break

            # select fields, if needed
            field_list = endpoint_config.get('fields')

            if field_list:
                for i, record in enumerate(page_records):
                    page_records[i] = {field: record[field] for field in field_list}

            if write_mode == 'page_chunks':
                write_to_duckdb(conn, page_records, dest_table, primary_key, update_mode)
            else:
                records.extend(page_records)

            # keep paging until max_pages is reached or no records are returned
            if max_pages and page_num >= max_pages:
                print('Pagination terminated')
                break
            else:
                page_num += 1
                params[offset_parameter] += num_records

        if write_mode == 'single_batch':
            write_to_duckdb(conn, records, dest_table, primary_key, update_mode)

    print('\nPipeline run complete.')

    # report time elapsed for pipeline
    end_time = time.time()
    elapsed = end_time - start_time
    print(f'Elapsed time {utilities.format_time(elapsed)}\n')


if __name__ == '__main__':

    # command-line argument parsing
    parser = argparse.ArgumentParser(description='Run an ingestion pipeline from a CKAN API endpoint.')
    parser.add_argument('target', type=str, help='The name of the pipeline to run.')
    parser.add_argument('-bf', '--backfill', help='Run a complete backfill of history.', action='store_true')
    args = parser.parse_args()

    run_pipeline(args.target, args.backfill)