import logging

from kafka import KafkaConsumer

from config import kafka_config

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        logging.info(kafka_config)
        self.consumer = KafkaConsumer(bootstrap_servers=kafka_config["uri"],
                                      security_protocol="SSL",
                                      ssl_cafile=kafka_config["ca_path"],
                                      ssl_certfile=kafka_config["cert_path"],
                                      ssl_keyfile=kafka_config["access_key"])

    def consume(self, topic: str, dataConsumer):

        self.consumer.subscribe([topic])

        for message in self.consumer:
            logger.info(f"received message {message.offset}")

            dataConsumer.consume(message.value)

    def close(self):
        self.consumer.close()
