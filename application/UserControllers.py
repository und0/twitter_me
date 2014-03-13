'''
Created on Mar 12, 2014

@author: amit
'''
from application.ControllerResponse import ControllerResponse

class CreateUserController:


    def __init__(self, users_repo):
        '''
        Constructor
        '''
        self.users_repo = users_repo
    
    def process(self, params):
        if not 'u' in params:
            return ControllerResponse().set_bad_request("User name not specified")
        
        user_name = params['u'][0]
        print "Creating user", user_name + "..."
        user = self.users_repo.create_user(user_name)
        
        return ControllerResponse().set_response(200, "user_id="+str(user.get_id()))