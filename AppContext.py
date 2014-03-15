from domain.UsersRepository import UsersRepository
from model.UserDAO import UserDAO
from db.DbConnection import DbConnection

class SimpleAppContext:
    ''' An extremely simplified, not in any way generic,
        version of an application-context - just to enable
        basic dependency injection '''

    def __init__(self):
        self.db_connection = DbConnection()
        self.user_dao = UserDAO(self.db_connection)
        self.users_repo = UsersRepository(self.user_dao)

app_context = SimpleAppContext()

def get_app_context():
    return app_context