import logging
from typing import Protocol

from kafka import KafkaProducer

from config import kafka_config

logger = logging.getLogger(__name__)


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=kafka_config["uri"],
                                      security_protocol="SSL",
                                      ssl_cafile=kafka_config["ca_path"],
                                      ssl_certfile=kafka_config["cert_path"],
                                      ssl_keyfile=kafka_config["access_key"])

    def publish(self, topic: str, data: str):
        if (data != None):
            logger.info(f"Sending {data} to kafka topic {topic}")

            self.producer.send(topic, data.encode("utf-8"))

            self.producer.flush()
