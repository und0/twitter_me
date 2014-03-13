class ControllerResponse:

    def __init__(self):
        self.content = ""
        self.content_type = "Content-type", "text/html; charset=UTF_8"
        self.code = 200
        self.err = None
        
    def set_error(self, code, message=None):
        self.code = code
        self.err = message
        return self
    
    def set_bad_request(self, message=None):
        self.code = 400
        self.err = message
        return self
    
    def set_not_found(self):
        self.code = 404
        return self
    
    def set_ok(self, content=None, content_type=None):
        self.code = 200
        if content:
            self.content = content
        if content_type:
            self.content_type = content_type
        return self