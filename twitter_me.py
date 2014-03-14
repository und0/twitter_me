import humongolus as orm 
import logging
import sys
from web import UserControllers
from pymongo.connection import Connection
from web.FrontController import SimpleControllersHttpServer
from model import Mongo

def setup_orm(host, port):
    Mongo.db_connection = Connection(host, port)
    
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    db_logger = logging.getLogger("humongolus")
    orm.settings(db_logger, Mongo.db_connection)
    
def setup_server(host, port):
    server = SimpleControllersHttpServer((host, port))
    users_controller = UserControllers.UserController()
    server.bind_controller("/user/create", users_controller, 'create_user')
    server.bind_controller("/user/follow", users_controller, 'follow_user')
    server.bind_controller("/user/unfollow", users_controller, 'unfollow_user')
    server.bind_controller("/user/tweet", users_controller, 'post_message')
    server.bind_controller("/user/tweets/get", users_controller, 'get_global_feed')
    server.bind_controller("/tweets/get", users_controller, 'get_user_feed')
    return server
    

def main():
    
    DB_HOST = "localhost"
    DB_PORT = 27017
    
    HTTP_HOST = "localhost"
    if len(sys.argv) > 1:
        HTTP_HOST = sys.argv[1]
    HTTP_PORT = 8080
    if len(sys.argv) > 2:
        HTTP_PORT = int(sys.argv[2])
    
    ' Set up DB '
    setup_orm(DB_HOST, DB_PORT)

    ' Set up the server '
    server = setup_server(HTTP_HOST, HTTP_PORT)
    
    ' Start! '    
    print "Twitter.me HTTP server started"
    print "Listening on", HTTP_HOST + ":" + str(HTTP_PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "\
            Goodbye\
            "
    
    
if __name__ == '__main__':
    main()
