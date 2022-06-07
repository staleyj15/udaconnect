import logging
from typing import Dict
from app import db, g # noqa
from .models import Location
from .schemas import NewLocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api.consumer")


class LocationConsumer:
    @staticmethod
    def read_from_topic_write_to_db() -> None:
        for message in g.kafka_consumer:
            validation_results: Dict = NewLocationSchema().validate(message.value)
            if validation_results:
                logger.warning(f"Unexpected data format in payload: {validation_results}")
                raise Exception(f"Invalid payload: {validation_results}")

            new_location = Location()
            new_location.person_id = message.value["person_id"]
            new_location.creation_time = message.value["creation_time"]
            new_location.coordinate = ST_Point(message.value["latitude"], message.value["longitude"])
            try:
                db.session.add(new_location)
                db.session.commit()
            except Exception as e:
                print(f'{e}\nUnable to insert {message.value} into Location table')

