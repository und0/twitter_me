import BaseHTTPServer
from urlparse import urlparse
from urlparse import parse_qs

class SimpleFrontController(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	A 
	"""

	def __init__(self, request, client_address, server, controllers):
		self.controller_callbacks = controllers
		BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
	
	def send_header(self, keyword, value):
		' Overridden cause we''re an API - we don'' have headers '
		pass
	
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
			content = str({'success':'false', 'error':response.err})
		else:
			content = str({'success':'true', 'payload':response.content})
		self.wfile.write(content)
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

