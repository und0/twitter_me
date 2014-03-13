class User:

    def __init__(self, entity):
        self.entity = entity

    def get_id(self):
        return self.entity._id
        
    def follow(self, user_id):
        self.entity.following.append(user_id)
    
    def unfollow(self, user_id):
        self.entity.following.remove(user_id)
    
    def add_follower(self, user_id):
        self.entity.followers.append(user_id)
    
    def remove_follower(self, user_id):
        self.entity.followers.remove(user_id)
    
    def post(self, message):
        pass
    
    def getFeed(self):
        pass
    
    def persist(self):
        self.entity.save()