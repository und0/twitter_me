import humongolus.field as field
from model.UserPost import UserPost

class PostMessage(UserPost):

    message = field.Char()
    
    def set_message(self, message):
        self.message = message
        return self

    def set_from_dict(self, dic):
        UserPost.set_from_dict(self, dic)
        self.message = dic['message']
        return self
    
    def get_dict(self):
        dic = UserPost.get_dict(self)
        dic['message'] = str(self.message)
        return dic
        