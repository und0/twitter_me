from __builtin__ import Exception

class NoSuchUser(Exception):
    
    def __init__(self, user_id):
        self.user_id = user_id
        
class UnauthorizedAction(Exception):
    def __init__(self, user_id, desc):
        self.user_id = user_id
        self.desc = desc