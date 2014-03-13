import humongolus.field as field
import humongolus as orm 
from datetime import datetime

class UserPost(orm.EmbeddedDocument):

    created = field.Date()
    
    def __init__(self):
        orm.EmbeddedDocument.__init__(self)
        self.created = datetime.now()
        
    def set_from_dict(self, dict):
        self.created = dict['created']

    def get_dict(self):
        val = {}
        if self.created:
            val['created'] = str(self.created)
        return val
