'''
Created on Mar 12, 2014

@author: amit
'''
from RequestController import RequestController
from application.HttpResponse import HttpResponse

class CreateUserController(RequestController):
    '''
    TODO
    '''


    def __init__(self, users_repo):
        '''
        Constructor
        '''
        RequestController.__init__(self)
        self.users_repo = users_repo
    
    def process(self, params):
        if not 'u' in params:
            print "user name not specified"
            return
        user_name = params['u'][0]
        print "Creating user", user_name + "..."
        user = self.users_repo.create_user(user_name)
        
        resp = HttpResponse();
        resp.content = "user_id="+str(user.get_id())
        return resp