import humongolus.field as field
import humongolus as orm 
from datetime import datetime

class UserPost(orm.EmbeddedDocument):
    
    '''
    A user's post (tweet); really contains almost nothing, but should be
    used as a base of concrete posts (text, photos, audio, etc.).
    
    The one and only field is 'created', which indicates when the post
    has been created. This is important seeing that users usually
    wish to retrieve posts newer-to-oldest, and then expect to know the
    amount of time that has passed since they've been published.
    
    @see UserEntity
    '''

    created = field.Date()
    
    def __init__(self):
        orm.EmbeddedDocument.__init__(self)
        self.created = datetime.now()
        
    def set_from_dict(self, dic):
        ''' @see UserEntity '''
        self.created = dic['created']

    def get_dict(self):
        ''' @see UserEntity '''
        dic = {}
        if self.created:
            dic['created'] = str(self.created)
        return dic
