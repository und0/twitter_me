from __builtin__ import Exception

class NoSuchUser(Exception):
    
    def __init__(self, user_id):
        self.user_id = user_id