import humongolus.field as field
import humongolus as orm
from domain.PostMessage import PostMessage

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    following = orm.List(type=int)
    posts = orm.List()
        
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
        fields = {"_id":1, "name":1, "posts":1}
        coll = self._conn[self._db][self._collection]
        users_cursor = coll.find(query, fields)
        users = []
        for doc in users_cursor:
            ent = UserEntity()
            ent.set_from_dict(doc)
            users.append(ent)
        return users

    def set_from_dict(self, dict):
        self._id = dict['_id']
        self.name = dict['name']
        
        self.following = []
        if 'following' in dict:
            self.following = dict['following']
        
        self.posts = []
        if 'posts' in dict:
            for post in dict['posts']:
                self.posts.append( PostMessage().set_from_dict(post) )
        return self
    
    def get_dict(self):
        dict = {}
        dict['id']=self._id
        dict['name']=self.name
        dict['posts'] = []
        for post in self.posts:
            dict['posts'].append(post.get_dict())
        return dict
    
    def __str__(self):
        if not self._id:
            return "_id=None"
        return "_id="+self._id

    @classmethod
    def all_fields(cls):
        return ["name", "following", "followers", "posts"]
