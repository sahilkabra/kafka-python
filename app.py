import signal
import sys
import argparse
import logging

from common.produce import Producer
from common.consume import Consumer
from random_number import RandomNumberProducer, RandomNumberConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    args = getArgs()
    kwargs = {
        k: v
        for k, v in vars(args).items() if k not in ("producer", "consumer")
    }

    run("produce" if args.producer else "consume", **kwargs)


def run(operation: str, service_uri: str, ca_path: str, cert_path: str,
        key_path: str, topic: str):
    if operation == "produce":
        producer = Producer(service_uri, ca_path, cert_path, key_path)

        logger.info("Producing message on topic {topic}".format(topic=topic))
        producer.publish(topic, RandomNumberProducer.produce())
    elif operation == "consume":
        consumer = Consumer(service_uri, ca_path, cert_path, key_path)

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

    parser.add_argument("--service-uri",
                        required=True,
                        help="URI for the running kafka instance(host:port)")
    parser.add_argument("--ca-path", required=True, help="CA cerfificate path")
    parser.add_argument("--cert-path",
                        required=True,
                        help="The Kafka certificate key path")
    parser.add_argument("--key-path",
                        required=True,
                        help="The Kafka access key")
    parser.add_argument("--topic", required=True, help="The Kafka topic")
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
