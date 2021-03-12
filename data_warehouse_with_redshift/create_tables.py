import configparser

import psycopg2
from run_on_aws import get_redshift_cluster_endpoint
from sql_queries import create_table_queries, drop_table_queries


def connect_db():
    """Connects to the database."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    cluster_config = config['CLUSTER']

    address, port = get_redshift_cluster_endpoint(cluster_config['IDENTIFIER'])
    # connect to default database
    print(f"Connecting to Redshift cluster at {address}:{port} ...")
    conn = psycopg2.connect(
        f"host={address} "
        f"dbname={cluster_config['DB_NAME']} "
        f"user={cluster_config['DB_USER']} "
        f"password={cluster_config['DB_PASSWORD']} "
        f"port={port}")
    print(conn)
    conn.set_session(autocommit=True)
    return conn.cursor(), conn


def drop_tables(cur, conn):
    """Drops each table using the queries in `drop_table_queries` list."""
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Creates each table using the queries in `create_table_queries` list."""
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(repr(e))


if __name__ == "__main__":
    cur, conn = connect_db()

    # drop_tables(cur, conn)
    # create_tables(cur, conn)

    conn.close()
