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


class DatagovCkanApiPipeline():

    def __init__(self, endpoint_name, backfill=False):

        self.endpoint_name = endpoint_name
        self.backfill = backfill

        # build query parameters from config
        self.endpoint_config = config.ENDPOINTS.get(self.endpoint_name)

        if not self.endpoint_config:
            raise ValueError(f'No endpoint named "{self.endpoint_name}" was found in config.ENDPOINTS')

        self.url = config.BASE_URL + self.endpoint_config['endpoint']

        if self.backfill and self.endpoint_config.get('backfill_params'):
            self.params = self.endpoint_config['backfill_params']
        else:
            self.params = self.endpoint_config.get('params', dict())
        
        self.limit_parameter = self.endpoint_config['pagination']['limit_parameter']
        self.params[self.limit_parameter] = self.endpoint_config['pagination']['limit_value']

        self.offset_parameter = self.endpoint_config['pagination']['offset_parameter']
        self.params[self.offset_parameter] = 0

        self.max_pages = self.endpoint_config['pagination'].get('max_pages')

        # build database write/update parameters from config
        self.db_path = config.DB_PATH
        self.dest_table = f'{config.LANDING_SCHEMA}.{self.endpoint_config['destination_table']}'
        self.primary_key = self.endpoint_config.get('primary_key')
        self.update_mode = self.endpoint_config['update_mode']
        self.write_mode = self.endpoint_config['write_mode']

    
    def get_with_retries(self, max_retries=5):
        '''
        Make a GET request to an API, with retries if necessary
        '''
        for retry_num in range(1, max_retries+1):
            r = requests.get(self.url, params=self.params, stream=True)
            
            if r.ok:
                return r
            
            else:
                # server errors should lead to retries
                if r.status_code >= 500:
                    print(f'API returned status code {r.status_code} with reason "{r.reason}". Retrying.')
                    
                # bad request errors should throw an exception
                elif r.status_code >= 400:
                    raise RuntimeError(f'API returned status code {r.status_code} with reason "{r.reason}".')
            
            sleep(3)
        
        raise RuntimeError('Max retries exhausted when making GET request to API.')


    def write_to_duckdb(self, records):
        '''
        Write API records to the DuckDB data warehouse.
        '''
        with StringIO() as f:
            json.dump(records, f)
            f.seek(0)

            data = self.conn.read_json(f)
        
            # for small tables of mutable data, full reloads are simple and self-healing
            if self.update_mode == 'full_reload':
                self.conn.sql(f'''
                            
                    BEGIN TRANSACTION;

                    DELETE FROM {self.dest_table}
                    ;

                    INSERT INTO {self.dest_table}
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
            elif self.update_mode == 'upsert_replace':
                self.conn.sql(f'''
                    
                    BEGIN TRANSACTION;
                    
                    DELETE FROM {self.dest_table}
                    WHERE
                        {self.primary_key} IN (SELECT {self.primary_key} FROM data)
                    ;

                    INSERT INTO {self.dest_table}
                    BY NAME
                    SELECT
                        *
                        , CURRENT_LOCALTIMESTAMP() as inserted_at
                    FROM data
                    ;

                    COMMIT;

                ''')

            # for development purposes only - do not use in production due to risk of schema drift
            elif self.update_mode == 'create_table':
                self.conn.sql(f'''
                            
                    CREATE OR REPLACE TABLE {self.dest_table} AS
                    SELECT
                        *
                        , CURRENT_LOCALTIMESTAMP() as inserted_at
                    FROM data

                ''')
            
        print(f'    Wrote {len(records)} records to DuckDB')


    def run(self):

        start_time = time.time()
        print(f'\nStarting pipeline for endpoint "{self.endpoint_name}"\n')

        # get records from API
        records = list()
        page_num = 1

        with duckdb.connect(self.db_path) as self.conn:

            # loop through API pages
            while True:

                with self.get_with_retries() as r:
                    page_records = utilities.find(json.load(r.raw), self.endpoint_config['path_to_records'])

                num_records = len(page_records)
                print(f'Collected {num_records} records from page {page_num}')

                # if there are no records on this page, we have gone past the last page
                if num_records == 0:
                    print('Pagination terminated')
                    break

                # select fields, if needed
                field_list = self.endpoint_config.get('fields')

                if field_list:
                    for i, record in enumerate(page_records):
                        page_records[i] = {field: record[field] for field in field_list}

                if self.write_mode == 'page_chunks':
                    self.write_to_duckdb(page_records)
                else:
                    records.extend(page_records)

                # keep paging until max_pages is reached or no records are returned
                if self.max_pages and page_num >= self.max_pages:
                    print('Pagination terminated')
                    break
                else:
                    page_num += 1
                    self.params[self.offset_parameter] += num_records

            if self.write_mode == 'single_batch':
                self.write_to_duckdb(records)

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

    # build and run pipeline
    pipeline = DatagovCkanApiPipeline(args.target, args.backfill)
    pipeline.run()