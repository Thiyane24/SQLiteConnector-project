class ConnectionPool:
    def __init__(self,connector_class, size, **kwargs):
        self.connector_class = connector_class
        self.size = size
        self._available= []
        self._active = []
        
        for i in range(size):
            connection = connector_class(**kwargs)
            connection.connect()
            self._available.append(connection)
            
    
    def get_connection(self):
        if not self._available:
            raise RuntimeError("No connection available")
        removed = self._available.pop()
        self._active.append(removed)
        return removed
    
    def release_connection(self,conn):
        self._active.remove(conn)
        self._available.append(conn)
        return conn
    
    @property
    def connection_count(self):
        add = self._available + self._active
        return len(add)
        
    @property
    def active_count(self):
        return len(self._active)
    
    @property
    def available_count(self):
        return len(self._available)
    
    @property
    def is_healthy(self):
        if self._available:
            return True
        else:
            return False
        
    
    def close_all(self):
        for conn in self._available:
            conn.disconnect()
            
        self._available = []
        
        for conn in self._active:
            conn.disconnect()
        
        
        self._active = []