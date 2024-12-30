import logging

import redis

from box import Box
from src.util.postgres import create_connection, create_sqlalchemy_connection


class AppConfig:
    def __init__(self, path_to_config_file: str, verbose: bool = False):
        self.path_to_config_file = path_to_config_file

        # Initialize connection app_config
        self.config = Box.from_yaml(filename=self.path_to_config_file)
        self.redis_client = redis.StrictRedis.from_url(self.config.DASHBOARD.REDIS_URL)
        self.pg_connection = create_sqlalchemy_connection(
            username=self.config.POSTGRES.USERNAME,
            password=self.config.POSTGRES.PASSWORD,
            host=self.config.POSTGRES.HOST,
            port=self.config.POSTGRES.PORT,
            database=self.config.POSTGRES.DATABASE,
            schema=self.config.POSTGRES.SCHEMA
        )

        self.verbose = verbose
        self.logger = logging.Logger('root')


app_config = AppConfig(path_to_config_file='src/config.yaml')
