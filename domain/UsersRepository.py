from domain.User import User

class UsersRepository:

    def __init__(self, user_dao):
        self.user_dao = user_dao

    def create_user(self, user_name):
        entity = self.user_dao.create_user(user_name)
        return User(entity, self.user_dao)
    
    def get_user(self, user_id):
        entity = self.user_dao.get_user(user_id)
        return User(entity, self.user_dao);