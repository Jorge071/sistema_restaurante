from abc import ABC, abstractmethod
import mysql.connector

class BaseDAO(ABC):
    def __init__(self, db_config):
        self.db_config = db_config
    

    def _get_connection(self):
        try: 
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            raise ConnectionAbortedError(f"Problemas ao connectar: {err}")
        
    @abstractmethod
    def save(self, objeto):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass    

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def update(self, objeto):
        pass