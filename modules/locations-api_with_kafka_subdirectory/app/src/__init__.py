from .models import Connection, Location, Person  # noqa
from .schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa
from .controllers import api as udaconnect_api


def register_routes(api, app, root="api"):
    api.add_namespace(udaconnect_api, path=f"/{root}")
