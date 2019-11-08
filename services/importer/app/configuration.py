"""Contains configuration for this application."""
from dataclasses import dataclass

import config

KAFKA_TOPIC: str = 'streaming.products.raw'
REDIS_PREFIX: str = 'product:imported:'


@dataclass(frozen=True)
class ConfigDefinition:
    """Definition of config parameters."""

    systembolaget_api_key: str  # Needs to be defined in ENV
    kafka_host: str = 'localhost:9092'
    kafka_group_id: str = 'test'
    redis_host: str = 'localhost'


CONFIG = ConfigDefinition(*config.load(ConfigDefinition))
