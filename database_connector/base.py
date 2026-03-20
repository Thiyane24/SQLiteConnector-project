from abc import ABC, abstractmethod


class DatabaseConnector(ABC):
    def __init__(self,connection_string, connection = None):
        self.connection_string = connection_string
        self._connection = connection
    
    @abstractmethod    
    def connect(self):
       raise NotImplementedError("Subclasses must implement connect")
   
    @abstractmethod     
    def disconnect(self):
        raise NotImplementedError("Subclasses must implement close")
    
    @abstractmethod
    def execute(self, query, params=()):
        raise NotImplementedError("Subclasses must implement execute")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type,exc_val, exc_tb):
        self.disconnect()
        return False