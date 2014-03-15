class MongoDAO:

    '''
    A generic, reuseable DAO (Data Access Object) for data in a
    MongoDB environment.
    Can be optionally used by concrete DAO's to implement common DB
    operations associated with DAO's. The recommended method for doing
    that is the delegation of a MongoDAO instance, seeing that the
    inheritance for provide a generic interface likely not to fit
    concrete implementations.
    '''

    def __init__(self, entity_cls, db_connection, db_name, coll_name):
        '''
        @param entity_cls: The concrete class of the managed entity.
        @param db_connection: An instance of the Mongo.connection class.
        @param db_name: Name of the DB where entities are stored.
        @param coll_name: Collection within the DB where entities are stored.
        '''
        self.db_collection = db_connection[db_name][coll_name]
        self.entity_cls = entity_cls

    def create_entity(self, entity):
        '''
        Creates an empty entity in the DB. The ID will be automatically assigned,
        and is expected not to be set.
        @param: entity: The entity to create.
        @return: The entity, which the freshly assigned ID set.
        '''
        entity._id = entity.save()
        return entity

    def get_entity(self, key):
        ''' Retrieve an entity. '''
        query = {'_id':key}
        doc = self.db_collection.find_one(query)
        if not doc:
            return None
        
        entity = self.entity_cls()
        return entity.set_from_dict(doc);

    def collection(self):
        ''' Retrieve the Mongo-DB collection managed by this DAO. '''
        return self.db_collection