'''
Tools providing a simplified form of a front-controller.
The main module class is SimpleFrontControllerHTTPServer, and in order to
use the module front-controller, this is the class to be instantiated
and initialized.

Implementation is based upon Python's BaseHTTPServer module.
'''

import BaseHTTPServer
from urlparse import urlparse
from urlparse import parse_qs
import json
from StringIO import StringIO


class SimpleFrontControllerHTTPServer(BaseHTTPServer.HTTPServer):
	'''
	The HTTP request server. Provides a means of controllers invocation according
	to pre-binding based upon requests' URI paths.
	
	For example, in order to create a handler for requests over /foo/bar URL
	path (URL parameters are oblivious), one must create a class HandlerClass and
	a designated handleFooBar(params) method; then, the method can be registered via the bind_controller()
	method, as follows:
	
	myClass = HandlerClass()
	server.bind_controller("/foo/bar", myClass, 'handleFooBar')
	
	Once activated, the server will invoke myClass.handleFooBar(params) whenever a request is
	made to /foo/bar.
	
	Bind methods should be able to get one parameter, which is a dictionary of HTTP parameters.
	In addition, the server expects for them to return an instance of the ControllerResponse class.
	Finally, take note that the server always returns response in a JSON format, having the
	method's returned value sub-encoded into the JSON structure.
	
	@see ControllerResponse
	@see SimpleFrontController
	'''

	controller_callbacks = {}

	def __init__(self, server_address):
		BaseHTTPServer.HTTPServer.__init__(self, server_address, None)

	def bind_controller(self, url, controller, callback):
		'''
		Bind a controller to a URL path.
		
		@param url: The path to bind the controller to (e.g. '/foo/bar').
		@param controller: The controller instance to invoke.
		@param callback: The controll's method to invoke.
		'''
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




class SimpleFrontController(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	A simplified form of a front-controller.
	Invoked by the companion class SimpleFrontControllerHTTPServer which provides the
	core HTTP server functionality. 
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
		
		content = StringIO()
		if response.err:
			json.dump({'success':'false', 'error':response.err}, content)
		else:
			json.dump({'success':'true', 'payload':response.content}, content)
		content = content.getvalue()
		self.wfile.write(content)
	
