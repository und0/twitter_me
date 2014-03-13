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

    @classmethod
    def all_fields(cls):
        return ["following", "followers", "posts"]
    
    @classmethod
    def field_posts(cls):
        return ["posts"]