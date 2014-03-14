from model.UserService import UserService
from domain.UsersRepository import UsersRepository

class SimpleAppContext:
    ''' An extremely simplified, not in any way generic, version of an domain-context -
      just to enable dependency injection '''

    def __init__(self):
        self.users_service = UserService()
        self.users_repo = UsersRepository(self.users_service)
