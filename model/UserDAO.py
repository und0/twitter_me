from model.MongoDAO import MongoDAO
from model.UserEntity import UserEntity

class NoSuchUser(Exception):
    ''' An exception indicating a user-get operation has failed since the user was not found. '''
    def __init__(self, user_id):
        self.user_id = user_id

class UserDAO:
    
    '''
    A DAO (Data Access Object), providing a Data Abstraction Layer
    for the system's user entities. Implementation assumes a MongoDB
    and thus implements the requires operations using Mongo-DB queries and
    uses the MongoDAO as a helper class.
    
    @see MongoDAO
    '''

    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def init(self):
        ''' Late-initialize; Must be called after the DB connection has been established. '''
        self.mongo_dao = MongoDAO(UserEntity, self.db_connection.get_connection(), UserEntity._db, UserEntity._collection)
        self.collection = self.mongo_dao.collection()
        del self.db_connection
    
    def create_user(self, user_name):
        ''' Create a new user. '''
        entity = UserEntity()
        entity.name = user_name
        return self.mongo_dao.create_entity(entity)
      
    def get_user(self, user_id):
        user = self.mongo_dao.get_entity(user_id)
        if not user:
            raise NoSuchUser(user_id)
        return user

    def add_follow(self, user, follow_uid):

        # Trouble with trying to implement this directly via the ORM - as follows:        
        # user.following.append(follow_uid)
        # user.save()
        # So a manual implementation is used instead.
        
        query = {"_id":user._id}
        update = {'$push':{"following":follow_uid}}
        self.collection.update(query, update);
        user = self.get_user(user._id)
    
    def remove_follow(self, user, follow_uid):

        # This could have easily been implemented directly via the ORM as follows:
        #   user.following.remove(follow_uid)
        #   user.save()
        # BUT! the ORM appears to be buggy!!! So have have to do this manually
        
        query = {"_id":user._id}
        update = {'$pull':{"following":follow_uid}}
        self.collection.update(query, update);
        user = self.get_user(user._id)

    def add_post(self, user, post):
        ''' Add a new post (post-type agnostic).'''

        # The ORM fails a great deal in dealing with these complex queries, so
        # we have to do this manually
        
        query = {"_id":user._id}
        update = { '$push':{ "posts":{'$each':[post.get_dict()], '$sort':{"created":1}, '$slice':-1000}} }
        self.collection.update(query, update);
        user = self.get_user(user._id)
        
    def get_followed_users(self, user):
        '''
        Retrieve the list of users (data and everything) followed by the given user.
        Returns the users as a list of UserEntity objects. 
        '''
        
        if not user.following or len(user.following)==0:
            return []
        
        # A 'get' of multiple keys: this is definitely too tricky for the ORM to handle,
        # so we do both this and the 'translation' manually
        
        # Build query string; final form of it should be like so:
        # { $or : [ {_id:X}, {_id:Y}, {_id:Z} ] }
        # Which would lookup users whose ID's are in this set: (X, Y, Z).
        query = []
        for f_user_id in user.following:
            query.append({'_id':f_user_id})
        query = {'$or': query}
        
        docs_cursor = self.collection.find(query)
        users = []
        for doc in docs_cursor:
            ent = UserEntity().set_from_dict(doc)
            users.append(ent)
        return users
    