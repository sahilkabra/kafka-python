#!/usr/bin/env python3

import argparse
import logging
import signal
import sys

from common.consume import Consumer
from common.produce import Producer
from config import kafka_config, sites_config
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

    logger.info(f"running {operation}")

    if operation == "check_site":
        producer = Producer()

        for site in sites_config:
            logger.info(f"checking availablity for {site}")
            result = check.check_site(Site(url=site["url"], name=site["name"]),
                                      site["regex"]).to_json()
            producer.publish(topic, result)

    elif operation == "consume_site":
        consumer = Consumer()

        logger.info(f"Consuming site message on topic {topic}")

        signal.signal(signal.SIGINT,
                      close(consumer))  # handle CTRL-C to stop consumer

        consumer.consume(topic, check_process)  # blocking operation
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
