'''
The application's business logic involving user data management.

Provides an OOD version of the traditional 'UserService' solution, by offering
the following conceptual abstraction:

1. In this layer, there system's users are presented using a designated 'User'
   class, which encapsulates data-storage details such as DB-entities; This
   class allows for clients (e.g. web controllers) to handle users in a fashion -
   decoupled and oblivious to data-storage concepts.
2. The system's users are thought of as stored in a conceptual repository; to create
   or refer to a 'user' (as explained in 1), a UsersRepository class is provided.
'''

from model.PostMessage import PostMessage

class UsersRepository:
    '''
    The conceptual repository of business-logic users.
    All references to users by the business-logic clients (e.g. web
    controllers) start here.
    
    @see User
    '''

    def __init__(self, user_dao):
        self.user_dao = user_dao

    def create_user(self, user_name):
        entity = self.user_dao.create_user(user_name)
        return User(entity, self.user_dao)
    
    def get_user(self, user_id):
        entity = self.user_dao.get_user(user_id)
        return User(entity, self.user_dao);


class User:
    '''
    The conceptual business logic user (can be thought of as a user-facade).
    '''

    def __init__(self, entity, user_dao):
        self.entity = entity
        self.user_dao = user_dao

    def get_id(self):
        return self.entity._id
        
    def follow(self, user_id):
        '''
        Handle the action of setting the user follow a different one. 
        Oblivious to whether the user is perhaps already being followed by us.
        @param user_id: The ID of the user to follow.
        @raise NoSuchUser: in case the followed user doesn't exist.
        '''
        
        ' Make sure we are to follow a user that actually exists (if it doesn''t, an exception will be raised). '
        f_entity = self.user_dao.get_user(user_id)

        ' Add the followed user to the ones Im following '        
        if not user_id in self.entity.following:
            self.user_dao.add_follow(self.entity, user_id)
    
    def unfollow(self, user_id):
        '''
        Set the user to unfollow another one. 
        Oblivious to whether the user is actually currently followed by us.
        @param user_id: The ID of the user to unfollow.
        '''
        
        ' Remove that user from the ones Im following '
        if user_id in self.entity.following:
            self.user_dao.remove_follow(self.entity, user_id)
    
    def post(self, message):
        ''' Post a message-post. '''
        
        post = PostMessage().set_message(message)
        self.user_dao.add_post(self.entity, post)
    
    def get_posts(self, user_id):
        '''
        Retrieve a specified user's posts, assumed to be followed by us.
        @param user_id: The user whose posts should be retrieved.
        @raise UnauthorizedAction: In case we're not following 'user_id'.
        @return The posts, as plain post objects.
        '''
        
        if not user_id in self.entity.following:
            raise UnauthorizedAction(self.entity._id, "User is not following "+str(user_id))
        
        f_entity = self.user_dao.get_user(user_id)
        return f_entity.posts
    
    def get_feed(self):
        '''
        Retrieve our feed - i.e. the accumulation of posts from the users we're following.
        @return The posts and meta data regarding the users, organized into a user_id:user_object dictionary.
        '''
        
        f_users = self.user_dao.get_followed_users(self.entity)
        
        ' Arrange users onto the form of a dictionary, with the user-id as a key '    
        user_posts = {}
        for u in f_users:
            if u.posts and len(u.posts)>0:
                user_posts[u._id] = u
        
        return user_posts





class UnauthorizedAction(Exception):
    def __init__(self, user_id, desc):
        self.user_id = user_id
        self.desc = desc
