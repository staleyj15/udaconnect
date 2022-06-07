import logging
from typing import Dict, List
from app import db, g # noqa
from .models import Location
from .producer import LocationProducer
from .consumer import LocationConsumer
from .schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class LocationService:
    @staticmethod
    def retrieve_all() -> List[Location]:
        return db.session.query(Location).all()

    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def return_request_as_response(location: Dict) -> Location:
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        return new_location

    @staticmethod
    def create(location: Dict) -> dict:
        LocationProducer.write_location_to_topic(location)
        LocationConsumer.read_from_topic_write_to_db()
