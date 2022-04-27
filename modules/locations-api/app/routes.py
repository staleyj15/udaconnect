from .src import register_routes as attach_udaconnect


def register_routes(api, app, root="api"):
    # Add routes
    attach_udaconnect(api, app)
