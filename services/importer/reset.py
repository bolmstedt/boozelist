"""Resets all service state."""
import sys

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import KafkaException
from redis import Redis

from app.configuration import CONFIG, KAFKA_TOPIC, REDIS_PREFIX


def _main() -> None:
    print('Clearing Kafka and Redis')
    redis_client = Redis(host=CONFIG.redis_host)
    keys = redis_client.keys(REDIS_PREFIX + '*')
    if len(keys) > 0:
        redis_client.delete(*keys)
    admin = AdminClient({'bootstrap.servers': CONFIG.kafka_host})
    topics = admin.delete_topics([KAFKA_TOPIC], operation_timeout=30)
    for topic, future in topics.items():
        try:
            future.result()  # The result itself is None
            print("Topic {} deleted".format(topic))
        except KafkaException as err:
            print("Failed to delete topic {}: {}".format(topic, err),
                  file=sys.stderr)


if __name__ == "__main__":
    _main()
