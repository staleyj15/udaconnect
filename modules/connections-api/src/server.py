import time
import logging
from concurrent import futures
from app import engine, session # noqa
import grpc
from . import connection_pb2
from . import connection_pb2_grpc
from .mappings import ConnectionMapping
from .business_logic import BusinessLogic

logging.basicConfig(
    level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s, %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'
)


class ConnectionServicer(connection_pb2_grpc.ConnectionServiceServicer):
    def Get(self, request, context):
        logging.info(f'Connections requested for person_id {request.person_id}')
        connections_list = BusinessLogic().find_all_connections_for_person(
            person_id=request.person_id,
            start_date=request.start_date.ToDatetime(),
            end_date=request.end_date.ToDatetime(),
            meters=request.meters
        )
        connections_grpc_list = [ConnectionMapping(c).to_protobuf() for c in connections_list]
        result = connection_pb2.ConnectionResult()
        result.connections.extend(connections_grpc_list)
        if result:
            logging.info(f'Returning {len(connections_list)} connections for person_id {request.person_id}')
        return result


def start_grpc_server():
    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)

    logging.info("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
