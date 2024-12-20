import pandas as pd
import psycopg2


def create_connection(username: str,
                      password: str,
                      host: str,
                      port: str,
                      database: str,
                      schema: str) -> psycopg2.extensions.connection:
    """
    Create a connection to Postgres
    :param username: Postgres username
    :param password: Postgres password
    :param host: Postgres host
    :param port: Postgres port
    :param database: Postgres database
    :param schema: Postgres schema
    :return: Postgres connection
    """
    # Define the connection string
    conn_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    # Create the connection
    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    # Set the schema
    conn.cursor().execute(f'SET search_path TO {schema}')
    # Return the connection
    return conn


def query(conn: psycopg2.extensions.connection, query: str) -> pd.DataFrame:
    """
    Query Postgres.
    :param conn: Postgres connection
    :param query: SQL query
    :return: Pandas DataFrame with the data
    """
    # Fetch the data
    df = pd.read_sql(query, conn)
    # Return the DataFrame
    return df


def use_schema(conn: psycopg2.extensions.connection, schema: str) -> None:
    """
    Set the schema for the connection
    :param conn: Postgres connection
    :param schema: Postgres schema
    """
    # Set the schema
    conn.cursor().execute(f'SET search_path TO {schema}')
    # Commit the transaction
    conn.commit()
