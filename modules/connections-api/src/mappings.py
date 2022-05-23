from mercator import (
    ProtoMapping,
    ProtoKey,
    SinglePropertyMapping
)
from google.protobuf.timestamp_pb2 import Timestamp
from . import connection_pb2
from . import sql_models as sql
from datetime import datetime


def pydt2ts(x: datetime) -> int:
    return int(x.timestamp())


def str2dt(strdt: str) -> datetime:
    timestamp = Timestamp()
    y = int(strdt[:4])
    m = int(strdt[5:7].lstrip('0'))
    d = int(strdt[8:].lstrip('0'))
    pydt = datetime(y, m, d)
    timestamp.FromDatetime(dt=pydt)
    return timestamp


ProtobufTimestamp = SinglePropertyMapping(pydt2ts, Timestamp, 'seconds')


class PersonMapping(ProtoMapping):
    # the destination type from .proto file
    __proto__ = connection_pb2.PersonMessage
    # the base type of sqlalchemy types
    __source_input_type__ = sql.Person

    id = ProtoKey('id', int)
    first_name = ProtoKey('first_name', str)
    last_name = ProtoKey('last_name', str)
    company_name = ProtoKey('company_name', str)


class LocationMapping(ProtoMapping):
    # the destination type from .proto file
    __proto__ = connection_pb2.LocationMessage
    # the base type of sqlalchemy types
    __source_input_type__ = sql.Location

    id = ProtoKey('id', int)
    person_id = ProtoKey('person_id', int)
    longitude = ProtoKey('longitude', str)
    latitude = ProtoKey('latitude', str)
    creation_time = ProtoKey('creation_time', ProtobufTimestamp)


class ConnectionMapping(ProtoMapping):
    # the destination type from .proto file
    __proto__ = connection_pb2.ConnectionMessage
    # the base type of sqlalchemy types
    __source_input_type__ = sql.Connection

    location = ProtoKey('location', LocationMapping)
    person = ProtoKey('person', PersonMapping)