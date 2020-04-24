from kafka import KafkaProducer
from typing import Protocol
import logging

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self, service_uri: str, ca_path: str, cert_path: str,
                 key_path: str):
        self.producer = KafkaProducer(bootstrap_servers=service_uri,
                                      security_protocol="SSL",
                                      ssl_cafile=ca_path,
                                      ssl_certfile=cert_path,
                                      ssl_keyfile=key_path)

    def produce(self, topic: str, dataProducer):
        data = dataProducer.produce()

        if (data != None):
            message = "Sending message {}".format(data)
            logger.info(message)
            self.producer.send(topic, message.encode("utf-8"))

        self.producer.flush()
