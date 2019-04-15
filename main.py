import traceback
import time
import multiprocessing
import logging
from concurrent import futures

import grpc

from proto_pb2 import PingRequest, PingResponse
from proto_pb2_grpc import PingServicer, add_PingServicer_to_server, PingStub

ADDR = '127.0.0.1:50051'

class PingServicerImpl(PingServicer):
	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)

	def Ping(self, request, context):
		self.logger.info('Received Ping call')
		return PingResponse()

class ServerThread(multiprocessing.Process):
	def __init__(self):
		super().__init__()
		self.logger = logging.getLogger(self.__class__.__name__)
		self.pipe1, self.pipe2 = multiprocessing.Pipe()

	def run(self):
		self.logger.info('Building server')
		self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
		add_PingServicer_to_server(PingServicerImpl(), self.server)
		self.server.add_insecure_port(ADDR)
		
		self.logger.info('Server start')
		self.server.start()
		self.pipe2.send(True)

		self.pipe2.recv()
		self.logger.info('Stopping server')
		self.server.stop(True)
		self.pipe2.send(True)
	
	def wait_for_start(self):
		self.pipe1.recv()
	
	def stop(self):
		self.pipe1.send(True)
		self.pipe1.recv()
		self.logger.info('Server stopped')


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)

	# Start server
	server = ServerThread()
	server.start()
	server.wait_for_start()

	# Fire up first call
	logging.info('Sending first call')
	channel = grpc.insecure_channel(ADDR)
	client = PingStub(channel)
	logging.info('Ping response: %s', client.Ping(PingRequest()))

	# Restart server
	logging.info('Restarting server')
	server.stop()
	server = ServerThread()
	server.start()
	server.wait_for_start()

	# Fire second call
	logging.info('Sending second call')
	try:
		logging.info('Ping response: %s', client.Ping(PingRequest()))
	except:
		traceback.print_exc()

	# Fire third call
	logging.info('Sending third call')
	logging.info('Ping response: %s', client.Ping(PingRequest()))

	server.stop()
