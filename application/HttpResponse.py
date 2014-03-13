class HttpResponse:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.content = ""
        self.content_type = "Content-type", "text/html; charset=UTF_8"
        self.code = 200
        self.err = None