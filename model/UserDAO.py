from model.MongoDAO import MongoDAO
from model.UserEntity import UserEntity

class NoSuchUser(Exception):
    def __init__(self, user_id):
        self.user_id = user_id

class UserDAO:

    def __init__(self, db_connection):
        self.db_connection = db_connection
        
    def init(self):
        self.mongo_dao = MongoDAO(UserEntity, self.db_connection.get_connection(), UserEntity._db, UserEntity._collection)
        self.collection = self.mongo_dao.collection()
        del self.db_connection
    
    def create_user(self, user_name):
        entity = UserEntity()
        entity.name = user_name
        return self.mongo_dao.create_entity(entity)
      
    def get_user(self, user_id):
        user = self.mongo_dao.get_entity(user_id)
        if not user:
            raise NoSuchUser
        return user

    def add_follow(self, user, follow_uid):
        user.following.append(follow_uid)
        user.save()
    
    def remove_follow(self, user, follow_uid):

        # This could have easily been implemented directly via the ORM as follows:
        #   user.following.remove(follow_uid)
        #   user.save()
        # BUT! the ORM appears to be buggy!!! So have have to do this manually
        
        query = {"_id":user}
        update = {'$pull':{"following":follow_uid}}
        self.collection.update(query, update);
        user = self.get_user(user._id)

    def add_post(self, user, post):

        # The ORM fails a great deal in dealing with these complex queries, so
        # we have to do this manually
        
        query = {"_id":user._id}
        update = { '$push':{ "posts":{'$each':[post.get_dict()], '$sort':{"created":1}, '$slice':-1000}} }
        self.collection.update(query, update);
        user = self.get_user(user._id)
        
    def get_followed_users(self, user):
        if not user.following or len(user.following)==0:
            return []
        
        ###
        # A 'get' of multiple keys: this is definitely too tricky for the ORM to handle,
        # so we do both this and the 'deserialization' manually
        query = []
        for f_user_id in user.following:
            query.append({'_id':f_user_id})
        query = {'$or': query}
        fields = {"_id":1, "name":1, "posts":1}
        
        docs_cursor = self.collection.find(query, fields)
        users = []
        for doc in docs_cursor:
            ent = UserEntity().set_from_dict(doc)
            users.append(ent)
        return users
    