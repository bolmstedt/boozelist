"""Contains configuration for this application."""
from typing import NamedTuple

import config

KAFKA_TOPIC: str = 'streaming.products.raw'
REDIS_PREFIX: str = 'product:imported:'


class ConfigDefinition(NamedTuple):
    """Definition of config parameters.

    Should have entries like this:
    VARIABLE: type
    OTHER_VAR: type = 'default_value'
    """

    SYSTEMBOLAGET_API_KEY: str  # Needs to be defined in .env of ENV
    KAFKA_HOST: str = 'localhost:9092'
    KAFKA_GROUP_ID: str = 'test'
    REDIS_HOST: str = 'localhost'


CONFIG = ConfigDefinition(*config.load(ConfigDefinition))
