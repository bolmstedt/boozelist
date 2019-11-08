"""Provides service HTTP routes."""
import threading
from dataclasses import asdict, dataclass
from typing import Dict, List

from confluent_kafka.admin import AdminClient
from redis import Redis

from app.configuration import ConfigDefinition
from simple_server import Route


@dataclass
class DebugConfig:
    """Config class for DebugRoute."""

    redis_prefix: str
    topics: List[str]
    config: ConfigDefinition


class DebugRoute(Route):
    """Debug endpoint."""

    def __init__(
            self,
            redis_client: Redis,
            kafka_admin: AdminClient,
            debug_config: DebugConfig
    ):
        self.redis_client = redis_client
        self.kafka_admin = kafka_admin
        self.redis_prefix = debug_config.redis_prefix
        self.topics = debug_config.topics
        self.config = debug_config.config

    def exec(self) -> Dict:
        """Return debug information."""
        keys = self.redis_client.keys(self.redis_prefix + '*')
        cached_products = format(len(keys))
        configs = asdict(self.config)
        threads = [thread.name for thread in threading.enumerate()]

        return {
            'status': 'ok',
            'redis': {
                'cached_products': cached_products,
            },
            'topics': self.topics,
            'config': configs,
            'threads': threads
        }
