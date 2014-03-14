import humongolus.field as field
import humongolus as orm
from model.PostMessage import PostMessage
from domain.Exceptions import NoSuchUser

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    following = orm.List(type=int)
    posts = orm.List()
    
    def read(self, user_id):
        query = {'_id':user_id}
        coll = self._conn[self._db][self._collection]
        user_doc = coll.find_one(query)
        if not user_doc:
            raise NoSuchUser(user_id)
        
        self.set_from_dict(user_doc)
        return self
        
    def remove_following(self, following_uid):
        query = {"_id":self._id}
        update = {'$pull':{"following":following_uid}}
        self._coll.update(query, update);
        
    def add_post(self, post):
        query = {"_id":self._id}
        update = { '$push':{ "posts":{'$each':[post.get_dict()], '$sort':{"created":1}, '$slice':-1000}} }
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
        docs_cursor = coll.find(query, fields)
        users = []
        for doc in docs_cursor:
            ent = UserEntity()
            ent.set_from_dict(doc)
            users.append(ent)
        return users

    def set_from_dict(self, dic):
        self._id = dic['_id']
        self.name = dic['name']
        
        self.following = []
        if 'following' in dic:
            self.following = dic['following']
        
        self.posts = []
        if 'posts' in dic:
            for post in dic['posts']:
                self.posts.append( PostMessage().set_from_dict(post) )
        return self
    
    def get_dict(self):
        dic = {}
        dic['id']=self._id
        dic['name']=str(self.name)
        dic['posts'] = []
        for post in self.posts:
            dic['posts'].append(post.get_dict())
        return dic
    
    def __str__(self):
        if not self._id:
            return "_id=None"
        return "_id="+self._id

    @classmethod
    def all_fields(cls):
        return ["name", "following", "followers", "posts"]
