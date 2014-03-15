from pymongo.connection import Connection

class DbConnection:
    
    def connect(self, host, port):
        self.connection = Connection(host, port)
    
    def get_connection(self): 
        return self.connection
