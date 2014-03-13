from domain.UserEntity import UserEntity
from domain.PostMessage import PostMessage

class UserService:

    def create_user(self, user_name):
        entity = UserEntity()
        entity.name = user_name
        entity._id = entity.save()
        return entity
    
    def update_user(self, user):
        user.save()
    
    def get_user(self, user_id):
        return UserEntity.find_one(user_id)
    
    def get_users(self, user_ids, fields):
        return UserEntity
    
    def remove_follower(self, user, follower_uid):
        user.remove_follower(follower_uid);

    def remove_following(self, user, following_uid):
        user.remove_following(following_uid)
        
    def add_post(self, user, post):
        user.add_post(post)
    
    def get_user_feed(self, user_id):
        entity = self.get_user(user_id)
        if not entity:
            return None
        
        #f_users = UserEntity.find(entity.following, UserEntity.field_posts())
        f_users = entity.get_followed_users(entity)
        
        ' Arrange posts onto the form of a user-oriented dictionary '    
        posts = {}
        for u in f_users:
            if u.posts and len(u.posts)>0:
                posts[u._id] = u
        
        return posts