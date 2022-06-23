from datetime import datetime

from .models import Connection, Location, Person
from .schemas import (
    ConnectionSchema,
    NewLocationSchema,
    LocationSchema,
    PersonSchema,
)
from .services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
class LocationsResource(Resource):
    @accepts(schema=NewLocationSchema)
    @responds(status_code=201)
    def post(self) -> Location:
        request_body = request.json
        LocationService.create(location=request_body)
        # location: Location = LocationService.return_request_as_response(location=request_body)
        # return location

    @responds(schema=LocationSchema, many=True)
    def get(self) -> List[Location]:
        location: List[Location] = LocationService.retrieve_all()
        return location


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location