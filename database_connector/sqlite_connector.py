from database_connector.base import DatabaseConnector
import sqlite3

class SQLiteConnector(DatabaseConnector):
    def __init__(self, db_path):
        super().__init__(db_path)
        
    def connect(self):
        '''Connects to the DB'''
        self._connection=sqlite3.connect(self.connection_string)
        
    def disconnect(self):
        '''Closes the connection to the DB'''
        self._connection.close()
        self._connection = None
    
    def execute(self, query, params=()):
        '''Executes Queries'''
        if self._connection is None:
            raise ConnectionError("Not connected to the database")
        
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        self._connection.commit()
        
        if cursor.description is None:
            return []
        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        
        return [dict(zip(columns, row)) for row in rows]
        
        
    

               