import humongolus.field as field
from model.UserPost import UserPost

class PostMessage(UserPost):
    '''
    A concrete user-post containing a textual message.
    
    @see UserPost
    @see UserEntity
    '''

    message = field.Char()
    
    def set_message(self, message):
        self.message = message
        return self

    def set_from_dict(self, dic):
        ''' @see UserEntity '''
        UserPost.set_from_dict(self, dic)
        self.message = dic['message']
        return self
    
    def get_dict(self):
        ''' @see UserEntity '''
        dic = UserPost.get_dict(self)
        dic['message'] = str(self.message)
        return dic
        