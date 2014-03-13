from domain.PostMessage import PostMessage
from application import Exceptions.NoSuchUser
from application.Exceptions import UnauthorizedAction

class User:

    def __init__(self, entity, user_service):
        self.entity = entity
        self.user_service = user_service

    def get_id(self):
        return self.entity._id
        
    def follow(self, user_id):
        f_entity = self.user_service.get_user(user_id)
        if not f_entity:
            raise Exceptions(user_id)

        ' Add the followed user to the ones Im following '        
        if not user_id in self.entity.following:
            self.entity.following.append(user_id)
            self.user_service.update_user(self.entity)
        
        ' Add myself to the list of followers of the users '
        if not self.entity._id in f_entity.followers:
            f_entity.followers.append(self.entity._id)
            self.user_service.update_user(f_entity)
    
    def unfollow(self, user_id):
        uf_entity = self.user_service.get_user(user_id)
        if not uf_entity:
            raise Exceptions(user_id)

        ' Remove that user from the ones Im following '
        if user_id in self.entity.following:
            #self.entity.following.remove(user_id)
            #self.entity.save()
            ####################################################################################
            # This is merely a patch to replace the lines above, seeing that the ORM for some reason
            # can't handle list items removal remove() (BUG???) -- though append() works fine!!! 
            self.user_service.remove_following(self.entity, user_id)        
        

        ' Remove myself from the user I will not follow anymore '
        if self.entity._id in uf_entity.followers:
            #uf_entity.followers.remove(self.entity._id)
            #uf_entity.save()
            ####################################################################################
            # This is merely a patch to replace the lines above, seeing that the ORM for some reason
            # can't handle list items removal remove() (BUG???) -- though append() works fine!!! 
            self.user_service.remove_follower(uf_entity, self.entity._id)

    
    def post(self, message):
        post = PostMessage().set_message(message)
        #self.entity.posts.append(post);
        #self.entity.save();
        self.user_service.add_post(self.entity, post)
    
    def get_posts(self, user_id):
        
        if not user_id in self.entity.following:
            raise UnauthorizedAction(self.entity._id, "User is not following "+str(user_id))
        
        f_entity = self.user_service.get_user(user_id)
        if not f_entity:
            raise Exceptions(user_id)
        
        return f_entity.posts
    
    def get_feed(self):
        return self.user_service.get_user_feed(self.entity._id)
