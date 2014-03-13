from User import User
from domain.UserEntity import UserEntity


class UsersRepository:
    '''
    '''

    def create_user(self, user_name):
        entity = UserEntity()
        entity.name = user_name
        entity._id = entity.save()
        return User(entity)
    
    def get_user(self, user_id):
        entity = UserEntity()
        entity._id = user_id
        entity = entity.find_one()
        return User(entity)