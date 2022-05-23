import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from connection_client import for_testing_only

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

engine = create_engine(
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
session = Session(engine)
metadata = MetaData(engine)

if __name__ == "__main__":
    from src.server import start_grpc_server
    start_grpc_server()

    # delete after testing
    # for_testing_only()