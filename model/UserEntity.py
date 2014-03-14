import humongolus.field as field
import humongolus as orm
from model.PostMessage import PostMessage
from domain.Exceptions import NoSuchUser
from model import Mongo

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    following = orm.List(type=int)
    posts = orm.List()
    
    @classmethod
    def find_user(cls, user_id):
        query = {'_id':user_id}
        user_doc = cls.get_coll().find_one(query)
        if not user_doc:
            raise NoSuchUser(user_id)
        
        return UserEntity().set_from_dict(user_doc);
    
    def remove_follow(self, following_uid):
        # This is merely a patch to replace the lines above, seeing that the ORM for some reason
        # can't handle list items removal via remove() (BUG???) -- though append() works fine!!! 
        query = {"_id":self._id}
        update = {'$pull':{"following":following_uid}}
        self.get_collection().update(query, update);
        
    def add_post(self, post):
        query = {"_id":self._id}
        update = { '$push':{ "posts":{'$each':[post.get_dict()], '$sort':{"created":1}, '$slice':-1000}} }
        self.get_collection().update(query, update);
        
    def get_followed_users(self, user):
        if not user.following or len(user.following)==0:
            return []
        
        query = []
        for f_user_id in user.following:
            query.append({'_id':f_user_id})
        query = {'$or': query}
        fields = {"_id":1, "name":1, "posts":1}
        
        docs_cursor = self.get_collection().find(query, fields)
        users = []
        for doc in docs_cursor:
            ent = UserEntity().set_from_dict(doc)
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
        dic['following']=self.following
        dic['posts'] = []
        for post in self.posts:
            dic['posts'].append(post.get_dict())
        return dic
    
    def __str__(self):
        if not self._id:
            return "_id=None"
        return "_id="+self._id

    
    
    
    @classmethod
    def get_coll(cls):
        conn = Mongo.db_connection
        coll = conn[cls._db][cls._collection]
        return coll
    
    def get_collection(self):
        return self.__class__.get_coll();