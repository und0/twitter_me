from model.PostMessage import PostMessage
from domain.Exceptions import UnauthorizedAction

class User:

    def __init__(self, entity, user_dao):
        self.entity = entity
        self.user_dao = user_dao

    def get_id(self):
        return self.entity._id
        
    def follow(self, user_id):
        f_entity = self.user_dao.get_user(user_id)

        ' Add the followed user to the ones Im following '        
        if not user_id in self.entity.following:
            self.user_dao.add_follow(self.entity, user_id)
    
    def unfollow(self, user_id):
        uf_entity = self.user_dao.get_user(user_id)

        ' Remove that user from the ones Im following '
        if user_id in self.entity.following:
            self.user_dao.remove_follow(self.entity, user_id)        
    
    def post(self, message):
        post = PostMessage().set_message(message)
        self.user_dao.add_post(self.entity, post)
    
    def get_posts(self, user_id):
        
        if not user_id in self.entity.following:
            raise UnauthorizedAction(self.entity._id, "User is not following "+str(user_id))
        
        f_entity = self.user_dao.get_user(user_id)
        return f_entity.posts
    
    def get_feed(self):
        f_users = self.user_dao.get_followed_users(self.entity)
        
        ' Arrange users onto the form of a dictionary, with the user-id as a key '    
        user_posts = {}
        for u in f_users:
            if u.posts and len(u.posts)>0:
                user_posts[u._id] = u
        
        return user_posts
