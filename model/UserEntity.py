import humongolus.field as field
import humongolus as orm
from model.PostMessage import PostMessage

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    following = orm.List(type=int)
    posts = orm.List()
    
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
