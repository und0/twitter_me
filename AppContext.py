from domain.UsersRepository import UsersRepository
from domain.UserService import UserService

class SimpleAppContext:
    ''' An extremely simplified, not in any way generic, version of an application-context -
      just to enable dependency injection '''

    def __init__(self):
        self.users_service = UserService()
        self.users_repo = UsersRepository(self.users_service)

app_context = SimpleAppContext()

def get_app_context():
    return app_context