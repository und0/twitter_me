import humongolus.field as field
import humongolus as orm 
from domain.UserPost import UserPost
from domain.PostMessage import PostMessage

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    following = orm.List(type=int)
    followers = orm.List(type=int)
    posts = orm.List(type=[UserPost,PostMessage]) 

    def remove_follower(self, follower_uid):
        query = {"_id":self._id}
        update = {'$pull':{"followers":follower_uid}}
        self._coll.update(query, update);
        
    def remove_following(self, following_uid):
        query = {"_id":self._id}
        update = {'$pull':{"following":following_uid}}
        self._coll.update(query, update);
        
    def add_post(self, post):
        query = {"_id":self._id}
        update = { '$push':{ "posts":{'$each':[post.dict()], '$sort':{"created":1}, '$slice':-1000}} }
        self._coll.update(query, update);
        
    def get_followed_users(self, user):
        if not user.following or len(user.following)==0:
            return []
        
        ids = []
        for f_user_id in user.following:
            ids.append({'_id':f_user_id})
        
        query = {'$or': ids}
        return self._coll.find(query)

    def __str__(self):
        return str({"_id":self._id, "name":self.name, "#following":len(self.following), "#followers":len(self.followers), "#posts":len(self.posts)})

    @classmethod
    def all_fields(cls):
        return ["name", "following", "followers", "posts"]
    
    @classmethod
    def field_posts(cls):
        return ["posts"]