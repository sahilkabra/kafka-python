import logging
from typing import Protocol

from kafka import KafkaProducer

from config import kafkaConfig

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=kafkaConfig["uri"],
                                      security_protocol="SSL",
                                      ssl_cafile=kafkaConfig["ca_path"],
                                      ssl_certfile=kafkaConfig["cert_path"],
                                      ssl_keyfile=kafkaConfig["access_key"])

    def publish(self, topic: str, data: str):
        if (data != None):
            logger.info("Sending data {data}".format(data=data))
            self.producer.send(topic, data.encode("utf-8"))

            self.producer.flush()
