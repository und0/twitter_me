from web.ControllerResponse import ControllerResponse
from domain.Exceptions import NoSuchUser, UnauthorizedAction
from AppContext import get_app_context

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

    def __init__(self):
        self.users_repo = get_app_context().users_repo
    
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
        return ControllerResponse().set_ok( {'id':user.get_id()} )
    
    def follow_user(self, params):
        '''
        
        '''
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        follow_user_id = self.get_param('fuid', params)
        if not follow_user_id:
            return ControllerResponse().set_bad_request("Follow-user's ID not specified")
        follow_user_id = int(follow_user_id)
        
        try:
            user = self.users_repo.get_user(user_id)
            user.follow(follow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok()
    
    def unfollow_user(self, params):
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        unfollow_user_id = self.get_param('ufuid', params)
        if not unfollow_user_id:
            return ControllerResponse().set_bad_request("Unfollow-user's ID not specified")
        unfollow_user_id = int(unfollow_user_id)
        
        try:
            user = self.users_repo.get_user(user_id)
            user.unfollow(unfollow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok()
    
    def post_message(self, params):
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        message = self.get_param('m', params)
        if not message:
            return ControllerResponse().set_bad_request("Message not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
            user.post(message)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok();
    
    def get_user_feed(self, params):
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        target_user_id = self.get_param('fuid', params)
        if not target_user_id:
            return ControllerResponse().set_bad_request("Feed-user not specified")
        target_user_id = int(target_user_id)
        
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        try:
            posts = user.get_posts(target_user_id)
        except UnauthorizedAction as e:
            return ControllerResponse().set_error(500, e.desc)
        
        data = []
        for post in posts:
            data.append(post.get_dict())
        return ControllerResponse().set_ok(data)
    
    def get_global_feed(self, params):
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))

        try:
            posts = user.get_feed()
        except UnauthorizedAction as e:
            return ControllerResponse().set_error(500, e.desc)

        data = {}
        for uid, user in posts.iteritems():
            data[uid] = user.get_dict()
        return ControllerResponse().set_ok(data)
    
    
    
    
        
    def get_uid(self, params):
        if not 'uid' in params:
            return None
        user_id = int(params['uid'][0])
        return user_id
    
    def get_param(self, param, params):
        if not param in params:
            return None
        return params[param][0]
    