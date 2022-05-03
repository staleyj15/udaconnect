import logging
import sys

from datetime import datetime
from .models import Connection, Person
from .schemas import (
    ConnectionSchema,
    PersonSchema,
)
from .services import ConnectionService, PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"
api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

# set up logger
logger = logging.getLogger("persons-api.controllers")
logger.propagate = False
formatter = logging.Formatter('%(levelname)s:%(name)s – – [%(asctime)s], "%(message)s"', datefmt='%Y-%m-%d, %H:%M:%S')
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: Optional[datetime] = datetime.strptime(
            request.args.get("start_date", '1999-01-01'), DATE_FORMAT
        )
        end_date: Optional[datetime] = datetime.strptime(
            request.args.get("end_date", datetime.now().strftime('%Y-%m-%d')), DATE_FORMAT
        )
        distance: Optional[int] = request.args.get("distance", 5)

        if not request.args.get("start_date"):
            logger.warning('no start_date passed, using default value 1999-01-01')
        if not request.args.get("end_date"):
            logger.warning(f"no end_date passed, using default value {datetime.now().strftime('%Y-%m-%d')}")

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
