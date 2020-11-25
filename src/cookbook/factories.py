import json
import logging

from django.conf import settings

import kafka

logger = logging.getLogger("cookbook.factories")


RETRIES = 50
ACKS = "all"


RETRIES = 50


class EventBrokerFactory:
    def create_broker(self):
        security_protocol = "SSL" if settings.KAFKA_USE_SSL else "PLAINTEXT"
        servers = settings.KAFKA_BROKERS_URL

        try:
            producer = kafka.KafkaProducer(
                bootstrap_servers=servers,
                security_protocol=security_protocol,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=RETRIES,
                acks=ACKS,
            )
        except kafka.errors.NoBrokersAvailable:
            logger.exception(f"Couldn't find any brokers under '{servers}'")
        except Exception:
            logger.exception(
                "Unknown kafka error trying to connect under "
                f"'{servers}' with security protocol '{security_protocol}'"
            )
        else:
            return producer
