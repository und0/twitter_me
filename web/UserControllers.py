import json
from StringIO import StringIO
from web.ControllerResponse import ControllerResponse
from application.Exceptions import NoSuchUser

class UserController:
    '''
    A controller that handles user-related requests:
      - User creation
      - User follow assignment (i.e. have a different user's posts in my feed)
      - User unfollow
      - Post a message (followers will see it in their feeds)
      - Get my feed
      - Get a specified user's posts
    '''

    def __init__(self, users_repo):
        self.users_repo = users_repo
    
    def create_user(self, params):
        '''
        Handle a request to create a new user in the system.
        Required parameters:
          - uname: The user's name.
        Upon creation, the user's ID gets automatically assigned, and its value
        will be encoded into a JSON response.
        '''
        user_name = self.get_param('uname', params)
        if not user_name:
            return ControllerResponse().set_bad_request("User name not specified")
        
        user = self.users_repo.create_user(user_name)
        return ControllerResponse().set_ok( str({"id":user.get_id()}) )
    
    def follow_user(self, params):
        '''
        
        '''
        user_id = self.get_uid(params)
        if not user_id:
            return ControllerResponse().set_bad_request("User ID not specified")
        user_id = int(user_id)
        
        follow_user_id = self.get_param('fuid', params)
        if not follow_user_id:
            return ControllerResponse().set_bad_request("Follow-user's ID not specified")
        follow_user_id = int(follow_user_id)
        
        try:
            user = self.users_repo.get_user(user_id)
            user.follow(follow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok('cool')
    
    def unfollow_user(self, params):
        user_id = self.get_uid(params)
        if not user_id:
            return ControllerResponse().set_bad_request("User ID not specified")
        
        unfollow_user_id = self.get_param('ufuid', params)
        if not unfollow_user_id:
            return ControllerResponse().set_bad_request("Unfollow-user's ID not specified")
        unfollow_user_id = int(unfollow_user_id)
        
        try:
            user = self.users_repo.get_user(user_id)
            user.unfollow(unfollow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok('cool')
    
    def post_message(self, params):
        user_id = self.get_uid(params)
        if not user_id:
            return ControllerResponse().set_bad_request("User ID not specified")
        
        message = self.get_param('m', params)
        if not message:
            return ControllerResponse().set_bad_request("Message not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
            user.post(message)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok(message);
    
    def get_user_feed(self, params):
        user_id = self.get_uid(params)
        if not user_id:
            return ControllerResponse().set_bad_request("User ID not specified")
        message = self.get_param('fuid', params)
        if not message:
            return ControllerResponse().set_bad_request("Feed-user not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        posts = user.get_posts(user_id)
        return posts
    
    def get_global_feed(self, params):
        user_id = self.get_uid(params)
        if not user_id:
            return ControllerResponse().set_bad_request("User ID not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))

        posts = user.get_feed()
        content = StringIO()
        json.dump(posts, content)
        return ControllerResponse().set_ok(posts, content.getvalue())
    
    
    
    
        
    def get_uid(self, params):
        if not 'uid' in params:
            return None
        user_id = int(params['uid'][0])
        return user_id
    
    def get_param(self, param, params):
        if not param in params:
            return None
        return params[param][0]
    