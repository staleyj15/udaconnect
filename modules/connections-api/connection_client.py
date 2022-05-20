import grpc
import src.connection_pb2 as connection_pb2
import src.connection_pb2_grpc as connection_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = connection_pb2_grpc.ConnectionServiceStub(channel)

fake_request = connection_pb2.ConnectionRequest(person_id=6, meters=6, start_date='2020-07-01', end_date= '2022-04-11')
response = stub.Get(fake_request)
print(response)
