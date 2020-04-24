from kafka import KafkaConsumer
import logging

logger = logging.getLogger(__name__)


class Consumer:
    def __init__(self, service_uri: str, ca_path: str, cert_path: str,
                 key_path: str):
        self.consumer = KafkaConsumer(bootstrap_servers=service_uri,
                                      security_protocol="SSL",
                                      ssl_cafile=ca_path,
                                      ssl_certfile=cert_path,
                                      ssl_keyfile=key_path)

    def consume(self, topic: str, dataConsumer):

        self.consumer.subscribe([topic])

        for message in self.consumer:
            logger.info(
                "received message {message}".format(message=message.offset))
            dataConsumer.consume(message.value)

    def close(self):
        self.consumer.close()
