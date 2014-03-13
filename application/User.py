from domain.PostMessage import PostMessage
from application.NoSuchUser import NoSuchUser

class User:

    def __init__(self, entity, user_service):
        self.entity = entity
        self.user_service = user_service

    def get_id(self):
        return self.entity._id
        
    def follow(self, user_id):
        f_entity = self.user_service.get_user(user_id)
        if not f_entity:
            raise NoSuchUser(user_id)
        
        if not user_id in self.entity.following:
            self.entity.following.append(user_id)
            self.entity.save()
        
        if not self.entity._id in f_entity.followers:
            f_entity.followers.append(self.entity._id)
            f_entity.save()
    
    def unfollow(self, user_id):
        uf_entity = self.user_service.get_user(user_id)
        if not uf_entity:
            raise NoSuchUser(user_id)

        if user_id in self.entity.following:        
            self.entity.following.remove(user_id)
            self.entity.save()
        
        if self.entity._id in uf_entity.followers:
            uf_entity.followers.remove(self.entity._id)
            uf_entity.save()
    
    def post(self, message):
        #self.entity.posts.insert(0, PostMessage().set_message(message));
        self.entity.posts.append( PostMessage().set_message(message) )
        self.entity.save();
    
    def get_feed(self):
        return self.user_service.get_user_feed(self.entity._id);
