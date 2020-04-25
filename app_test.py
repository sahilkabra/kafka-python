import pytest

from common.consume import Consumer
from common.produce import Producer
from random_number import RandomNumberProducer

kafka_url = "kafka-kafkapython-sample-sahil-97de.aivencloud.com:16096"
ca_path = ".env/ca.pem"
cert_path = ".env/service.cert"
access_key = ".env/service.key"
topic = "sample-topic"
"""
def test_producer_consumer_integration():
    kafkaProducer = Producer(kafka_url, ca_path, cert_path, access_key)
    kafkaConsumer = Consumer(kafka_url, ca_path, cert_path, access_key)

    import pdb
    pdb.set_trace()
    producedMessage = ""

    def messageCallback(message: str):
        assert message == producedMessage

    mockDataConsumer = MockConsumer(messageCallback)
    kafkaConsumer.consume(topic, mockDataConsumer)

    for num in range(5):
        producedMessage = RandomNumberProducer.produce()

        print("producing message")
        kafkaProducer.publish(topic, producedMessage)
        print("published message")

    kafkaConsumer.close()


class MockConsumer:
    def __init__(self, callback):
        self.callback = callback

    def consume(self, message: str):
        self.callback(message)
"""
