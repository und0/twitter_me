import humongolus.field as field
import humongolus as orm 
from datetime import datetime

class UserPost(orm.EmbeddedDocument):

    created = field.Date()
    
    def __init__(self):
        orm.EmbeddedDocument.__init__(self)
        self.created = datetime.now()
        
    def set_from_dict(self, dic):
        self.created = dic['created']

    def get_dict(self):
        dic = {}
        if self.created:
            dic['created'] = str(self.created)
        return dic
