import humongolus.field as field
import humongolus as orm
from model.PostMessage import PostMessage

class UserEntity(orm.Document):
    '''
    The actual entity containing user data, as stored in the DB.
    
    Inherits the orm.Document class in order to enable ORM operations
    such as update() and save(), but since the ORM implementation is severely
    buggy and not complete, object<->dictionary adapter-methods have been
    manually written, and can be used whenever the entity is read directly
    from the DB rather than via the ORM's API (e.g. find_one()).
    
    Effectively, this can be handy in two cases:
    * A complex query / multiple-results operation has been manually run on the DB
      due to the fact that the ORM API was found insufficient.
    * A simple query has been run but the result contains complex fields (e.g. embedded
      documents) the ORM can't handle.
    '''

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
