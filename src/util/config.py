import redis
from box import Box

from src.util.postgres import create_connection

PATH_TO_CONFIG_FILE = 'config.yml'

# Initialize connection settings
CONFIG = Box.from_yaml(filename=PATH_TO_CONFIG_FILE)
REDIS_CLIENT = redis.StrictRedis.from_url(CONFIG.DASHBOARD.REDIS_URL)
PG_CONNECTION = create_connection(
    username=CONFIG.POSTGRES.USERNAME,
    password=CONFIG.POSTGRES.PASSWORD,
    host=CONFIG.POSTGRES.HOST,
    port=CONFIG.POSTGRES.PORT,
    database=CONFIG.POSTGRES.DATABASE,
    schema=CONFIG.POSTGRES.BQ_SCHEMA
)

# Initialize the settings
GLOBAL_CONFIG = {
    'config': CONFIG,
    'redis_client': REDIS_CLIENT,
    'pg_connection': PG_CONNECTION
}
