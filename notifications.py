import time

import grpc
from concurrent import futures

from protofiles.proto_pb2_grpc import notifyServicer, add_notifyServicer_to_server
from protofiles.proto_pb2 import DataResponse


class NotificationServer(notifyServicer):
    def __init__(self):
        pass

    def send_notif(self, request, context):
        print(f"Notification received: {request}\n {context}")
        response = DataResponse()
        response.message = "RECEIVED !"
        return response


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    add_notifyServicer_to_server(NotificationServer(), server)

    server.add_insecure_port('[::]:5003')

    server.start()

    try:
        while True:
            time.sleep(86400)
    except:
        server.stop()
