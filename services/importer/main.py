"""Imports products from api.systembolaget.se (and registers them)."""
import sys
from datetime import datetime

# pylint: disable=no-name-in-module
import sentry_sdk
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import Consumer, KafkaError, Producer
from redis import Redis

from app.configuration import (CONFIG, KAFKA_TOPIC, REDIS_PREFIX,
                               SENTRY_DISABLED)
from app.importer import Importer
from app.register import Register
from app.routes import DebugConfig, DebugRoute
from app.systembolaget import Systembolaget
from simple_server import SimpleServer
from thread_runner import ThreadRunner


def _main() -> None:
    if CONFIG.sentry_dsn != SENTRY_DISABLED:
        sentry_sdk.init(CONFIG.sentry_dsn)

    redis_client = Redis(host=CONFIG.redis_host)
    producer = Producer({
        'bootstrap.servers': CONFIG.kafka_host,
        'error_cb': _error_cb
    })
    consumer = Consumer({
        'bootstrap.servers': CONFIG.kafka_host,
        'group.id': CONFIG.kafka_group_id,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])
    admin_client = AdminClient({'bootstrap.servers': CONFIG.kafka_host})

    routes = {
        r'^debug$': DebugRoute(
            redis_client, admin_client, DebugConfig(
                REDIS_PREFIX, [KAFKA_TOPIC], CONFIG
            )
        )
    }

    services = [
        Importer(
            producer,
            redis_client,
            Systembolaget(CONFIG.systembolaget_api_key)
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
