class MongoDAO:

    def __init__(self, entity_cls, db_connection, db_name, coll_name):
        self.db_collection = db_connection[db_name][coll_name]
        self.entity_cls = entity_cls

    def create_entity(self, entity):
        entity._id = entity.save()
        return entity

    def get_entity(self, key):
        query = {'_id':key}
        doc = self.db_collection.find_one(query)
        if not doc:
            return None
        
        entity = self.entity_cls()
        return entity.set_from_dict(doc);

    def collection(self):
        return self.db_collection