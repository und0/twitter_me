from data.UserService import UserService
from application.UsersRepository import UsersRepository

class SimpleAppContext:
    ''' An extremely simplified, not in any way generic, version of an application-context -
      just to enable dependency injection '''

    def __init__(self):
        self.users_service = UserService()
        self.users_repo = UsersRepository(self.users_service)
