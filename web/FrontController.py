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
from web import UserControllers
from application.UsersRepository import UsersRepository
from pymongo.connection import Connection
from domain.UserService import UserService

class SimpleFrontController(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	A 
	"""

	def __init__(self, request, client_address, server, controllers):
		self.controller_callbacks = controllers
		BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
	
	def do_GET(self):
		parsedUrl = urlparse(self.path)
		params = parse_qs(parsedUrl.query)
		
		'Based on the path, find and invoke a pre-mapped controller callback'
		if not parsedUrl.path in self.controller_callbacks:
			self.send_response(404)
			return
		
		controller_cb = self.controller_callbacks[parsedUrl.path]
		controller, callback = controller_cb[0], controller_cb[1]
		method = getattr(controller, callback);
		response = method(params)
		
		
		if response.err:
			self.send_error(response.code, response.err)
			return
		
		self.wfile.write(response.content)
		#self.send_header("Content-Length", len(response.content))
		#self.send_header("Content-type", response.content_type)
		self.end_headers()
		self.send_response(response.code)


class SimpleControllersHttpServer(BaseHTTPServer.HTTPServer):

	controller_callbacks = {}

	def __init__(self, server_address):
		BaseHTTPServer.HTTPServer.__init__(self, server_address, None)

	def bind_controller(self, url, controller, callback):
		self.controller_callbacks[url] = (controller, callback)
	
	def finish_request(self, request, client_address):
		''' Overridden in order to perform an instantiation of our very own
			front-controller as a request handler rather than instantiating
			a handler in the default fashion.
			The main reason is that the default instantiation, though generic
			in terms of the concrete class, doesn't expect a class that would
			also take the controller_callbacks dictionary as an init-parameter; our
			customized front-controller relies on it, however.
			(source is BaseServer.finish_request)
			@see: SimpleFrontController '''
		SimpleFrontController(request, client_address, self, self.controller_callbacks)



' Set up DB '
DB_HOST = "localhost"
DB_PORT = 27017
db_connection = Connection(DB_HOST, DB_PORT)

logging.basicConfig(format='%(asctime)-15s %(message)s')
db_logger = logging.getLogger("humongolus")
orm.settings(db_logger, db_connection)

users_service = UserService()
users_repo = UsersRepository(users_service)


' Set up HTTP controller_callbacks and the HTTP server'
HTTP_HOST = "localhost"
if len(sys.argv) > 1:
	HTTP_HOST = sys.argv[1]

HTTP_PORT = 8080
if len(sys.argv) > 2:
	HTTP_PORT = int(sys.argv[2])

server = SimpleControllersHttpServer((HTTP_HOST, HTTP_PORT))
users_controller = UserControllers.UserController(users_repo)
server.bind_controller("/user/create", users_controller, 'create_user')
server.bind_controller("/user/follow", users_controller, 'follow_user')
server.bind_controller("/user/unfollow", users_controller, 'unfollow_user')
server.bind_controller("/user/post", users_controller, 'post_message')
server.bind_controller("/user/feed/get", users_controller, 'get_feed')



print "HTTP server", SimpleFrontController.server_version, "started"
print "Listening on", HTTP_HOST + ":" + str(HTTP_PORT)
try:
	server.serve_forever()
except KeyboardInterrupt:
	print "\
	aYE 0wnz t3h h77p!$%\
	"