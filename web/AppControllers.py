'''
The application's controllers.
Currently, only one controller is required - to handle user-related requests.
'''

from web.ControllerResponse import ControllerResponse
from model.UserDAO import NoSuchUser
from domain.UserManagement import UnauthorizedAction

class UserController:
    '''
    A controller that handles user-related requests:
      - User creation
      - User follow assignment (i.e. have a different user's posts in my feed)
      - User unfollow
      - Post a message (followers will see it in their feeds)
      - Get my feed
      - Get a specified user's posts
    
    Essentially interacts with the UserManagement module (i.e. the business logic
    layer) to handle these requests.
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
        return ControllerResponse().set_ok( {'id':user.get_id()} )
    
    def follow_user(self, params):
        '''
        Handle a request for a user to follow another.
        Required parameters:
         - uid
         - fuid - The ID of the user to follow.
        '''
        
        ' Extract the user''s ID '
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        ' Extract the follow-user''s ID '
        follow_user_id = self.get_param('fuid', params)
        if not follow_user_id:
            return ControllerResponse().set_bad_request("Follow-user's ID not specified")
        try:
            follow_user_id = int(follow_user_id)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        

        ' Invoke business logic. '
        try:
            user = self.users_repo.get_user(user_id)
            user.follow(follow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok()
    
    def unfollow_user(self, params):
        '''
        Handle a request for a user to unfollow another.
        Required parameters:
         - uid
         - ufuid - The ID of the user to unfollow.
        '''
        
        ' Extract the user''s ID '
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")

        ' Extract the unfollow-user'' ID '        
        unfollow_user_id = self.get_param('ufuid', params)
        if not unfollow_user_id:
            return ControllerResponse().set_bad_request("Unfollow-user's ID not specified")
        try:
            unfollow_user_id = int(unfollow_user_id)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")

        ' invoke business logic '        
        try:
            user = self.users_repo.get_user(user_id)
            user.unfollow(unfollow_user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok()
    
    def post_message(self, params):
        '''
        Handle a request for a user to post (tweet) a text-based message.
        Required parameters:
         - uid
         - m - The message's content
        '''
        
        ' Extract the user''s ID '
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")

        ' Extract the message to post'        
        message = self.get_param('m', params)
        if not message:
            return ControllerResponse().set_bad_request("Message not specified")
        
        ' invoke business logic '
        try:
            user = self.users_repo.get_user(user_id)
            user.post(message)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        return ControllerResponse().set_ok();
    
    def get_user_feed(self, params):
        '''
        Handle a request to retrieve a user's feed (user-specific posts).
        Required parameters:
         - uid
         - fuid - The user whose posts should be retrieved.
        '''
        
        ' Extract the user''s ID '
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        ' Extract the target user''s ID '
        target_user_id = self.get_param('fuid', params)
        if not target_user_id:
            return ControllerResponse().set_bad_request("Feed-user not specified")
        try :
            target_user_id = int(target_user_id)
        except ValueError: return ControllerResponse().set_bad_request("Target-user's ID is invalid")

        '\
        Invoke business logic\
        '
                
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e: return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))
        
        try:
            posts = user.get_posts(target_user_id)
        except UnauthorizedAction as e: return ControllerResponse().set_error(500, e.desc)
        
        ' Convert posts-data to their dictionary form (as clients usually require) '
        data = []
        for post in posts:
            data.append(post.get_dict())
        return ControllerResponse().set_ok(data)
    
    def get_global_feed(self, params):
        '''
        Handle a request to retrieve a user's global-feed, i.e. the accumulative
        posts for all users they follow.
        Require parameters:
         - uid  
        '''
        
        try:
            user_id = self.get_uid(params)
        except ValueError: return ControllerResponse().set_bad_request("User ID is invalid")
        if not user_id: return ControllerResponse().set_bad_request("User ID not specified")
        
        try:
            user = self.users_repo.get_user(user_id)
        except NoSuchUser as e:
            return ControllerResponse().set_error(500, "No such user: "+str(e.user_id))

        '\
        Invoke business logic\
        '
        
        try:
            posts = user.get_feed()
        except UnauthorizedAction as e:
            return ControllerResponse().set_error(500, e.desc)

        ' Convert to a <user_id:user_doc> dictionary form '
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
