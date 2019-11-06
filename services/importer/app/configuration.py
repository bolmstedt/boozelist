"""Contains configuration for this application."""
from typing import NamedTuple

import config


class ConfigDefinition(NamedTuple):
    """Definition of config parameters.

    Should have entries like this:
    VARIABLE: type
    OTHER_VAR: type = 'default_value'
    """

    SYSTEMBOLAGET_API_KEY: str  # Needs to be defined in .env of ENV
    KAFKA_HOST: str = 'localhost:9092'
    KAFKA_GROUP_ID: str = 'test'
    KAFKA_TOPIC: str = 'streaming.products.raw'
    SYSTEMBOLAGET_API_HOST: str = 'https://api-extern.systembolaget.se'
    SYSTEMBOLAGET_API_PRODUCTS_URL: str = '/product/v1/product'
    REDIS_HOST: str = 'localhost'
    REDIS_PREFIX: str = 'product:imported:'


CONFIG = ConfigDefinition(*config.load(ConfigDefinition))
