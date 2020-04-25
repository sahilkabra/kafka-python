import argparse
import logging
import signal
import sys

from common.consume import Consumer
from common.produce import Producer
from config import kafkaConfig
from random_number import RandomNumberConsumer, RandomNumberProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    args = getArgs()

    run("produce" if args.producer else "consume")


def run(operation: str):
    topic = kafkaConfig["topic"]

    if operation == "produce":
        producer = Producer()

        logger.info("Producing message on topic {topic}".format(topic=topic))

        producer.publish(topic, RandomNumberProducer.produce())
    elif operation == "consume":
        consumer = Consumer()

        logger.info("Consuming message on topic {topic}".format(topic=topic))
        signal.signal(signal.SIGINT, close(consumer))
        consumer.consume(topic, RandomNumberConsumer)


def close(instance):
    def handler(sig, frame):
        logger.info("SIGINT received")
        instance.close()
        sys.exit(0)

    return handler


def getArgs():
    parser = argparse.ArgumentParser(
        description="Sample project to publish and consume messages with Kafka"
    )

    parser.add_argument("--producer",
                        action="store_true",
                        default=False,
                        help="run the producer")
    parser.add_argument("--consumer",
                        action="store_true",
                        default=False,
                        help="run the consumer")

    return parser.parse_args()


if __name__ == '__main__':
    main()
