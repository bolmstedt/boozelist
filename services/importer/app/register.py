"""Provides the Register class."""
import json
from datetime import datetime

from confluent_kafka.cimpl import Consumer
from redis import Redis

from app.configuration import REDIS_PREFIX
from app.utils import hash_product
from thread_runner import Runnable, Runner


class Register(Runnable):
    """Class to register produced products to Redis."""

    def __init__(
            self,
            consumer: Consumer,
            redis_cli: Redis
    ) -> None:
        self.consumer = consumer
        self.redis = redis_cli

    def _register(self, raw: bytes) -> None:
        digest = hash_product(raw)
        date = str(datetime.now())

        self.redis.set(REDIS_PREFIX + digest, date)

        product = json.loads(raw.decode('utf-8'))

        print('[{}] {} added with hash {}'.
              format(date, product.get('ProductNameBold'), digest))

    def run(self, runner: Runner) -> None:
        """Register produced products to Redis."""
        while runner.run:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print('Consumer error: {}'.format(msg.error()))
                continue

            self._register(msg.value())

        self.consumer.close()
        print('[{}] Received SIGTERM, shutting down consumer.'.
              format(str(datetime.now())))
