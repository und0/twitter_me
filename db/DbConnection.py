from pymongo.connection import Connection

class DbConnection:
    '''
    Wrapper of the DB connection (to a Mongo DB).
    Holds the connection internally, which would only become applicable after a
    call to connect() has been successfully issued.
    Once the call completes, the connection is widely available (i.e. to
    various DAO instances) via get_connection().
    '''
    def connect(self, host, port):
        ''' Perform actual connect-action to DB. '''
        self.connection = Connection(host, port)
    
    def get_connection(self):
        ''' Retrieve the connection; should only be called after connect() has successfully completed. '''
        return self.connection