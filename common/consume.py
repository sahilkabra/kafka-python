import logging

from kafka import KafkaConsumer

from config import kafkaConfig

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self):
        logging.info(kafkaConfig)
        self.consumer = KafkaConsumer(bootstrap_servers=kafkaConfig["uri"],
                                      security_protocol="SSL",
                                      ssl_cafile=kafkaConfig["ca_path"],
                                      ssl_certfile=kafkaConfig["cert_path"],
                                      ssl_keyfile=kafkaConfig["access_key"])

    def consume(self, topic: str, dataConsumer):

        self.consumer.subscribe([topic])

        for message in self.consumer:
            logger.info(
                "received message {message}".format(message=message.offset))
            dataConsumer.consume(message.value)

    def close(self):
        self.consumer.close()
