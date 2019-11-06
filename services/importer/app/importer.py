"""Provides the Importer class."""
import sys
import time
from datetime import datetime
from typing import Optional

import schedule
from confluent_kafka.cimpl import KafkaError, Message, Producer
from redis import Redis

from app.configuration import KAFKA_TOPIC, REDIS_PREFIX
from app.systembolaget import Systembolaget
from app.utils import hash_product


def _delivery_report(
        err: Optional[KafkaError],
        msg: Message
) -> None:
    """Print result of last produce() call.

    Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush().
    """
    if err is not None:
        print('[{}] Message delivery failed: {}'.
              format(str(datetime.now()), err), file=sys.stderr)
    elif msg is Message:
        print('[{}] Message delivered to {} [{}]'.
              format(str(datetime.now()), msg.topic(), msg.partition()))


class Importer:
    """Class to import new products from Systembolaget."""

    def __init__(
            self,
            producer: Producer,
            redis_cli: Redis,
            systembolaget: Systembolaget
    ) -> None:
        self.producer = producer
        self.redis = redis_cli
        self.systembolaget = systembolaget

    def _import(self) -> None:
        data = self.systembolaget.get_products()
        imported = 0

        for product in data:
            digest = hash_product(product)

            if self.redis.exists(REDIS_PREFIX + digest) == 1:
                continue

            # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below,
            # when the message has been successfully delivered or failed
            # permanently.
            self.producer.produce(
                KAFKA_TOPIC,
                product,
                callback=_delivery_report
            )
            self.producer.poll(0)
            imported += 1

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        self.producer.flush()
        print('[{}] Imported {} new products out of {}'.
              format(str(datetime.now()), imported, len(data)))

    def run(self) -> None:
        """Import new products to Kafka.

        Imports any new products from Systembolaget not already
        registered in Redis and produces messages to Kafka.
        """
        # Always run once on startup to be fresh
        self._import()

        # Schedule to run again every hour
        schedule.every().hour.do(self._import)

        while True:
            schedule.run_pending()
            time.sleep(1)
