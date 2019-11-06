"""Provides the Importer class."""
import json
import sys
import time
from datetime import datetime
from http.client import HTTPException
from typing import List, Optional

import requests
import schedule
from confluent_kafka.cimpl import KafkaError, Message, Producer
from redis import Redis

from app.configuration import ConfigDefinition
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
              format(str(datetime.now()), err))
    elif msg is Message:
        print('[{}] Message delivered to {} [{}]'.
              format(str(datetime.now()), msg.topic(), msg.partition()))


class Importer:
    """Class to import new products from Systembolaget."""

    def __init__(
            self,
            producer: Producer,
            redis_cli: Redis,
            config: ConfigDefinition
    ) -> None:
        self.producer = producer
        self.redis = redis_cli
        self.config = config

    def _get_data(self) -> List[str]:
        headers = {
            'Ocp-Apim-Subscription-Key': self.config.SYSTEMBOLAGET_API_KEY,
        }

        data: List[str] = []

        try:
            response = requests.get(
                self.config.SYSTEMBOLAGET_API_HOST +
                self.config.SYSTEMBOLAGET_API_PRODUCTS_URL,
                headers=headers
            )
            data = json.loads(response.content.decode('utf-8'))
            response.close()
        except HTTPException as err:
            print(err, file=sys.stderr)

        return data

    def _import(self) -> None:
        data = self._get_data()
        imported = 0

        for product in data:
            raw = json.dumps(product).encode('utf-8')
            digest = hash_product(raw)

            if self.redis.exists(self.config.REDIS_PREFIX + digest) == 1:
                continue

            # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below,
            # when the message has been successfully delivered or failed
            # permanently.
            self.producer.produce(
                self.config.KAFKA_TOPIC,
                raw,
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
