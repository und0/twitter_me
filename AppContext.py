from domain.UsersRepository import UsersRepository
from domain.UserService import UserService
from model.UserDAO import UserDAO
from db.DbConnection import DbConnection

class SimpleAppContext:
    ''' An extremely simplified, not in any way generic,
        version of an application-context - just to enable
        basic dependency injection '''

    def __init__(self):
        self.db_connection = DbConnection()
        self.user_dao = UserDAO(self.db_connection)
        self.users_service = UserService(self.user_dao)
        self.users_repo = UsersRepository(self.users_service)

app_context = SimpleAppContext()

def get_app_context():
    return app_context