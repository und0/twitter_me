import humongolus.field as field
from domain.UserPost import UserPost

class PostMessage(UserPost):

    message = field.Char()
    
    def set_message(self, message):
        self.message = message
        return self