from domain.Exceptions import NoSuchUser
from domain.User import User

class UsersRepository:

    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self, user_name):
        entity = self.user_service.create_user(user_name)
        return User(entity, self.user_service)
    
    def get_user(self, user_id):
        entity = self.user_service.get_user(user_id)
        if not entity:
            raise NoSuchUser(user_id)
        return User(entity, self.user_service);