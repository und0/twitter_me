from domain.UserEntity import UserEntity

class UserService:

    def create_user(self, user_name):
        entity = UserEntity()
        entity.name = user_name
        entity._id = entity.save()
        return entity
    
    def get_user(self, user_id):
        return UserEntity.find_one(user_id, UserEntity.all_fields())
    
    def get_user_feed(self, user_id):
        entity = self.get_user(user_id)
        if not entity:
            return None
        
        if not entity.following:
            return None
        
        users = UserEntity.find(entity.following, UserEntity.field_posts())
        posts = {}
        for u in users:
            posts[u._id] = u.posts
        
        return posts