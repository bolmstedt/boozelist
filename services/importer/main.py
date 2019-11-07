"""Imports products from api.systembolaget.se (and registers them)."""
import sys
from datetime import datetime

# pylint: disable=no-name-in-module
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import Consumer, KafkaError, Producer
from redis import Redis

from app.configuration import CONFIG, KAFKA_TOPIC, REDIS_PREFIX
from app.importer import Importer
from app.register import Register
from app.routes import DebugConfig, DebugRoute
from app.systembolaget import Systembolaget
from simple_server import SimpleServer
from thread_runner import ThreadRunner


def _main() -> None:
    redis_client = Redis(host=CONFIG.REDIS_HOST)
    producer = Producer({
        'bootstrap.servers': CONFIG.KAFKA_HOST,
        'error_cb': _error_cb
    })
    consumer = Consumer({
        'bootstrap.servers': CONFIG.KAFKA_HOST,
        'group.id': CONFIG.KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])
    admin_client = AdminClient({'bootstrap.servers': CONFIG.KAFKA_HOST})

    routes = {r'^debug$': DebugRoute(
        redis_client, admin_client, DebugConfig(
            REDIS_PREFIX, [KAFKA_TOPIC], CONFIG
        )
    )}

    services = [
        Importer(
            producer,
            redis_client,
            Systembolaget(CONFIG.SYSTEMBOLAGET_API_KEY)
        ),
        Register(consumer, redis_client),
        SimpleServer(8000, routes),
    ]

    ThreadRunner(services).run()


def _error_cb(err: KafkaError) -> None:
    print('[{}] Message delivery failed: {}'.format(str(datetime.now()), err),
          file=sys.stderr)


if __name__ == "__main__":
    _main()
