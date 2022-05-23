from collections import namedtuple
from datetime import datetime, timedelta
from typing import Dict, List
from app import engine, session # noqa
from . import sql_models as sql
from sqlalchemy.sql import text


class BusinessLogic:
    """isolates SQL queries returning objects ready for the protobuf serialization layer"""
    def __init__(self):
        self.SqlLoc = namedtuple('SqlLocation', ['person_id', 'id', 'st_x', 'st_y', 'creation_time'])

    @staticmethod
    def query_all_locations_for_person(person_id: int, start_date: datetime, end_date: datetime) -> List[sql.Location]:
        """Get list of places person has been between start date and end date."""
        locations = session.query(
            sql.Location
        ).filter(
            sql.Location.person_id == person_id
        ).filter(
            sql.Location.creation_time >= start_date
        ).filter(
            sql.Location.creation_time < end_date
        ).all()

        return locations

    @staticmethod
    def query_all_persons() -> Dict[str, sql.Person]:
        """Get dictionary of person_ids for all people."""
        persons = session.query(sql.Person).all()
        persons_map = {person.id: person for person in persons}
        return persons_map

    @staticmethod
    def prepare_query_args(person_id: int, meters:int, start_date: datetime, end_date: datetime, locations: sql.Location) \
            -> List[dict]:
        """Prepare query arguments from location objects and additional parameters."""
        query_args = []
        for location in locations:
            query_args.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )
        return query_args

    @staticmethod
    def query_locations_within_person_parameters(person_params: dict) -> List[sql.Location]:
        """Get list of connections where connecting persons are within specified parameters of person."""
        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )
        matching_locations = engine.execute(query, **person_params)
        return matching_locations.fetchall()

    @staticmethod
    def create_connection(matching_location: sql.Location, person_map: Dict[str, sql.Person]) -> sql.Connection:
        """Create connection object from Location object."""
        exposed_person_id = matching_location.person_id
        exposed_location_id = matching_location.id
        exposed_lat = matching_location.st_x
        exposed_long = matching_location.st_y
        exposed_time = matching_location.creation_time

        location = sql.Location(
            id=exposed_location_id,
            person_id=exposed_person_id,
            creation_time=exposed_time,
        )
        location.set_wkt_with_coords(exposed_lat, exposed_long)
        connection = sql.Connection(location=location, person=person_map[exposed_person_id])
        return connection

    def find_all_connections_for_person(self, person_id: int, start_date: datetime, end_date: datetime, meters: int) \
            -> List[sql.Connection]:
        """Find all connections for given person and parameters."""
        locations = self.query_all_locations_for_person(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date
        )
        person_map = self.query_all_persons()
        query_args = self.prepare_query_args(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=meters,
            locations=locations
        )
        locs: List[sql.Location] = []
        for q in query_args:
            locs += self.query_locations_within_person_parameters(person_params=q)
        connections: List[sql.Connection] = []
        for con_loc in locs:
            connections.append(self.create_connection(matching_location=self.SqlLoc(*con_loc), person_map=person_map))
        return connections