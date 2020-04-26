import argparse
import logging
import signal
import sys

from common.consume import Consumer
from common.produce import Producer
from config import kafka_config, sites_config
from random_number import RandomNumberConsumer, RandomNumberProducer
from site_status import check, check_process
from site_status.metrics import log_metrics
from site_status.model import Site

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    args = getArgs()

    run(args.operation)


def run(operation: str):
    topic = kafka_config["topic"]

    logger.info("running {operation}".format(operation=operation))

    if operation == "produce":
        producer = Producer()

        logger.info("Producing message on topic {topic}".format(topic=topic))

        producer.publish(topic, str(RandomNumberProducer.produce()))
    elif operation == "consume":
        consumer = Consumer()

        logger.info("Consuming message on topic {topic}".format(topic=topic))
        signal.signal(signal.SIGINT, close(consumer))
        consumer.consume(topic, RandomNumberConsumer)
    elif operation == "check_site":
        producer = Producer()

        logger.info("checking site availablity")
        for site in sites_config:
            result = check.check_site(Site(url=site["url"], name=site["name"]),
                                      site["regex"]).to_json()
            producer.publish(topic, result)
    elif operation == "consume_site":
        consumer = Consumer()

        logger.info(
            "Consuming site message on topic {topic}".format(topic=topic))
        signal.signal(signal.SIGINT, close(consumer))
        consumer.consume(topic, check_process)
    elif operation == "log_metrics":
        log_metrics("google")
    else:
        logger.info("unknown operation")
        sys.exit(1)


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

    parser.add_argument(
        "--operation",
        help="operation to run. one of produce, consume, check_site")

    return parser.parse_args()


if __name__ == '__main__':
    main()
