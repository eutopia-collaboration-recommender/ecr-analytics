import polars as pl
import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, Engine


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


def create_sqlalchemy_connection(username: str,
                                 password: str,
                                 host: str,
                                 port: str,
                                 database: str,
                                 schema: str) -> sqlalchemy.engine.base.Connection:
    """
    Create a connection to Postgres using SQLAlchemy
    :param username: Postgres username
    :param password: Postgres password
    :param host: Postgres host
    :param port: Postgres port
    :param database: Postgres database
    :param schema: Postgres schema
    :return: SQLAlchemy connection
    """
    # Define the connection string
    conn_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    # Create the connection
    engine = create_engine(
        conn_string,
        connect_args={'options': '-csearch_path={}'.format(schema)})
    conn = engine.connect()
    # Return the connection
    return conn


def create_sqlalchemy_engine(username: str,
                             password: str,
                             host: str,
                             port: str,
                             database: str,
                             schema: str) -> Engine:
    """
    Create a connection to Postgres using SQLAlchemy
    :param username: Postgres username
    :param password: Postgres password
    :param host: Postgres host
    :param port: Postgres port
    :param database: Postgres database
    :param schema: Postgres schema
    :return: SQLAlchemy connection
    """
    # Define the connection string
    conn_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    # Create the connection
    engine = create_engine(
        conn_string,
        connect_args={'options': '-csearch_path={}'.format(schema)})
    # Return the connection
    return engine


def query(conn: psycopg2.extensions.connection | sqlalchemy.engine.base.Connection, query_str: str) -> pd.DataFrame:
    """
    Query Postgres.
    :param conn: Postgres connection
    :param query_str: SQL query
    :return: Pandas DataFrame with the data
    """
    # Fetch the data
    df = pd.read_sql(query_str, conn)
    # Return the DataFrame
    return df


def query_polars(conn: sqlalchemy.engine.base.Connection, query_str: str) -> pl.DataFrame:
    """
    Query Postgres.
    :param conn: Postgres connection
    :param query_str: SQL query
    :return: Polars DataFrame with the data
    """
    # Fetch the data
    df = pl.read_database(query_str, conn)
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
