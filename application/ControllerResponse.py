class ControllerResponse:

    def __init__(self):
        self.content = ""
        self.content_type = "Content-type", "text/html; charset=UTF_8"
        self.code = 200
        self.err = None
        
    def set_error(self, code, message=None):
        self.err = message
        self.code = code
        return self
    
    def set_bad_request(self, message=None):
        self.code = 400
        self.content = message
        return self
    
    def set_not_found(self):
        self.code = 404
        return self
    
    def set_response(self, code, content, content_type=None):
        self.code = code
        self.content = content
        if content_type:
            self.content_type = content_type
        return self