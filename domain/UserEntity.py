import humongolus.field as field
import humongolus as orm 
from domain.UserPost import UserPost

class UserEntity(orm.Document):

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    followers = orm.List(type=int)
    following = orm.List(type=int)
    posts = orm.List(type=UserPost)