import logging
import json
from app import db, TOPIC_NAME, KAFKA_SERVER # noqa
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api.consumer")


class LocationProducer:
    @staticmethod
    def write_location_to_topic(location):
        kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        kafka_data = json.dumps(location, indent=2).encode('utf-8')
        kafka_producer.send(TOPIC_NAME, kafka_data)
        kafka_producer.flush()
        logger.info(f'published to topic={TOPIC_NAME}:\t{location}')
