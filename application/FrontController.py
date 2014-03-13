'''
Created on Mar 12, 2014

@author: amit
'''

import humongolus as orm 
import logging
import BaseHTTPServer
import sys
from urlparse import urlparse
from urlparse import parse_qs
import UserControllers
from UsersRepository import UsersRepository
from pymongo.connection import Connection

class FrontController(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	A 
	"""

	def __init__(self, request, client_address, server, controllers):
		self.controllers = controllers
		BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
	
	def do_GET(self):
		parsedUrl = urlparse(self.path)
		params = parse_qs(parsedUrl.query)
		
		'Based on the path, find and invoke a pre-mapped controller'
		if not parsedUrl.path in self.controllers:
			self.send_response(200)
			return
		
		controller = self.controllers[parsedUrl.path]
		response = controller.process(params)
		
		
		if response.err:
			self.send_error(response.code, response.err)
			return
		
		self.wfile.write(response.content)
		#self.send_header("Content-Length", len(response.content))
		#self.send_header("Content-type", response.content_type)
		self.end_headers()
		self.send_response(response.code)


class ControllersHttpServer(BaseHTTPServer.HTTPServer):

	controllers = {}

	def __init__(self, server_address):
		BaseHTTPServer.HTTPServer.__init__(self, server_address, None)

	def add_controller(self, url, ctrl):
		self.controllers[url] = ctrl
	
	def finish_request(self, request, client_address):
		"""Finish one request by instantiating a request handler class."""
		FrontController(request, client_address, self, self.controllers)



' Set up DB '
DB_HOST = "localhost"
DB_PORT = 27017
conn = Connection(DB_HOST, DB_PORT)

logging.basicConfig(format='%(asctime)-15s %(message)s')
logger = logging.getLogger("humongolus")
orm.settings(logger, conn)

users_repo = UsersRepository()


' Set up HTTP controllers and the HTTP server'
HTTP_HOST = "localhost"
if len(sys.argv) > 1:
	HTTP_HOST = sys.argv[1]

HTTP_PORT = 8080
if len(sys.argv) > 2:
	HTTP_PORT = int(sys.argv[2])

server = ControllersHttpServer((HTTP_HOST, HTTP_PORT))
server.add_controller("/user/create", UserControllers.CreateUserController(users_repo))




print "HTTP server", FrontController.server_version, "started"
print "Listening on", HTTP_HOST + ":" + str(HTTP_PORT)
try:
	server.serve_forever()
except KeyboardInterrupt:
	print "\
	aYE 0wnz t3h h77p!$%\
	"