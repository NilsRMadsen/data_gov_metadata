from . import config

import duckdb


if __name__ == '__main__':

    with open('./duckdb_init.sql') as f:
        init_sql = f.read()

    # connect to or create a new duckdb database file, and run initial sql commands
    with duckdb.connect(config.DB_PATH) as conn:
        conn.sql(init_sql)