import os
from src.config import config_by_name
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

env = os.getenv("FLASK_ENV") or "test"
engine = create_engine(config_by_name[env].SQLALCHEMY_DATABASE_URI)
session = Session(engine)
metadata = MetaData(engine)

if __name__ == "__main__":
    from src.server import start_grpc_server
    start_grpc_server()
