import grpc
import datetime as dt
from google.protobuf.timestamp_pb2 import Timestamp
import src.connection_pb2 as connection_pb2
import src.connection_pb2_grpc as connection_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""


def for_testing_only():
    channel = grpc.insecure_channel("localhost:5006")
    stub = connection_pb2_grpc.ConnectionServiceStub(channel)

    def str2dt(strdt: str) -> dt.datetime:
        timestamp = Timestamp()
        y = int(strdt[:4])
        m = int(strdt[5:7].lstrip('0'))
        d = int(strdt[8:].lstrip('0'))
        pydt = dt.datetime(y, m, d)
        timestamp.FromDatetime(dt=pydt)
        return timestamp

    fake_request = connection_pb2.ConnectionRequest(person_id=6, meters=6, start_date=str2dt('2020-07-01'),
                                                    end_date=str2dt('2022-04-11'))
    response = stub.Get(fake_request)
    print(response)


if __name__ == "__main__":
    # delete after testing
    for_testing_only()