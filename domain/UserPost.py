import humongolus.field as field
import humongolus as orm 
from datetime import datetime

class UserPost(orm.EmbeddedDocument):

    created = field.Date()
    
    def __init__(self):
        orm.EmbeddedDocument.__init__(self)
        self.created = datetime.now()
        
    def dict(self):
        return {'created':self.created}        