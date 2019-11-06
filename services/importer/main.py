"""Imports products from api.systembolaget.se (and registers them)."""
import sys
import threading
from datetime import datetime
from pprint import pprint

# pylint: disable=no-name-in-module
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import (Consumer, KafkaError, KafkaException,
                                   Producer)
from redis import Redis

from app.configuration import CONFIG, KAFKA_TOPIC, REDIS_PREFIX
from app.importer import Importer
from app.register import Register
from app.systembolaget import Systembolaget


def _main() -> None:
    redis_client = _get_redis()

    services = [
        Importer(
            _get_producer(),
            redis_client,
            Systembolaget(CONFIG.SYSTEMBOLAGET_API_KEY)
        ),
        Register(_get_consumer(), redis_client)
    ]
    threads = []

    for service in services:
        threads.append(threading.Thread(target=service.run))

    for thread in threads:
        thread.start()


def _get_consumer() -> Consumer:
    consumer = Consumer({
        'bootstrap.servers': CONFIG.KAFKA_HOST,
        'group.id': CONFIG.KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])

    return consumer


def _get_producer() -> Producer:
    return Producer({
        'bootstrap.servers': CONFIG.KAFKA_HOST,
        'error_cb': _error_cb
    })


def _get_redis() -> Redis:
    return Redis(host=CONFIG.REDIS_HOST)


def _debug() -> None:
    redis_client = _get_redis()
    keys = redis_client.keys(REDIS_PREFIX + '*')
    print('Number of cached products in Redis: {}'.format(len(keys)))
    topics = _get_consumer().list_topics().topics
    topics = filter(lambda topic: '__' not in topic, [*topics])
    print('Kafka topics: {}'.format(', '.join(topics)))
    pprint(CONFIG)
    sys.exit()


def _reset() -> None:
    print('Clearing Kafka and Redis')
    redis_client = _get_redis()
    keys = redis_client.keys(REDIS_PREFIX + '*')
    if len(keys) > 0:
        redis_client.delete(*keys)
    admin = AdminClient({'bootstrap.servers': CONFIG.KAFKA_HOST})
    topics = admin.delete_topics([KAFKA_TOPIC], operation_timeout=30)
    for topic, future in topics.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except KafkaException as err:
            print("Failed to delete topic {}: {}".format(topic, err),
                  file=sys.stderr)
    sys.exit()


def _error_cb(err: KafkaError) -> None:
    print('[{}] Message delivery failed: {}'.format(str(datetime.now()), err),
          file=sys.stderr)


if __name__ == "__main__":
    if 'debug' in sys.argv[1:]:
        _debug()
    if 'reset' in sys.argv[1:]:
        _reset()
    _main()
