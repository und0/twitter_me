import humongolus.field as field
from domain.UserPost import UserPost

class PostMessage(UserPost):

    message = field.Char()
    
    def set_message(self, message):
        self.message = message
        return self

    def set_from_dict(self, dict):
        UserPost.set_from_dict(self, dict)
        self.message = dict['message']
        return self
    
    def get_dict(self):
        dict = UserPost.get_dict(self)
        dict['message'] = str(self.message)
        return dict
        