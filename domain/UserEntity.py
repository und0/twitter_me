import humongolus.field as field
import humongolus as orm 

class UserEntity(orm.Document):
    '''
    classdocs
    '''

    _db = "twitter_me"
    _collection = "users"

    _id = field.AutoIncrement()
    name = field.Char()
    followers = orm.List(type=int)
    following = orm.List(type=int)

