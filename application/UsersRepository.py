from User import User
from application.NoSuchUser import NoSuchUser
from domain.UserEntity import UserEntity

class UsersRepository:

    def __init__(self, user_service):
        self.user_service = user_service

    def create_user(self, user_name):
        entity = self.user_service.create_user(user_name)
        return User(entity, self.user_service)
    
    def get_user(self, user_id):
        #entity = self.user_service.get_user(user_id)
        entity = UserEntity.find_one(user_id)
        if not entity:
            raise NoSuchUser(user_id)
        return User(entity, self.user_service);