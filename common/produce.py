import logging
from typing import Protocol

from kafka import KafkaProducer

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, service_uri: str, ca_path: str, cert_path: str,
                 key_path: str):
        self.producer = KafkaProducer(bootstrap_servers=service_uri,
                                      security_protocol="SSL",
                                      ssl_cafile=ca_path,
                                      ssl_certfile=cert_path,
                                      ssl_keyfile=key_path)

    def publish(self, topic: str, data):

        if (data != None):
            message = "Sending message {}".format(data)
            logger.info(message)
            self.producer.send(topic, message.encode("utf-8"))

        self.producer.flush()
