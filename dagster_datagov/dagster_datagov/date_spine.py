try:
    from . import config
except ImportError:
    import config

import duckdb
import json

from datetime import date, datetime, timedelta
from io import StringIO

START_DATE = '2000-01-01'
DEST_TABLE = 'date_spine'


def load_date_spine():
    # establish start and end dates
    start_date = datetime.fromisoformat(START_DATE).date()
    today = datetime.now().date()
    end_date = date(today.year + 10, today.month, today.day)

    print(f'\nGenerating date spine from {start_date.isoformat()} to {end_date.isoformat()}')

    # build list of dates between the start and end dates, inclusive
    range_length = (end_date - start_date).days + 1
    date_range = [
        {'calendar_date': (start_date + timedelta(days=x)).isoformat()} 
        for x in range(range_length)
    ]

    # load the date spine into DuckDB
    with StringIO() as f:
        json.dump(date_range, f)
        f.seek(0)

        with duckdb.connect(config.DB_PATH) as conn:

            target_table = f'{config.LANDING_SCHEMA}.{DEST_TABLE}'
            spine = conn.read_json(f)

            conn.sql(f'''

                BEGIN TRANSACTION;
                    
                DELETE
                FROM {target_table}
                ;

                INSERT INTO {target_table}
                BY NAME
                SELECT *
                FROM spine
                ;

                COMMIT;

            ''')

            print('Wrote date spine to DuckDB\n')


if __name__ == '__main__':
    load_date_spine()