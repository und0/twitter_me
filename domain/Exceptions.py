from __builtin__ import Exception

class UnauthorizedAction(Exception):
    def __init__(self, user_id, desc):
        self.user_id = user_id
        self.desc = desc