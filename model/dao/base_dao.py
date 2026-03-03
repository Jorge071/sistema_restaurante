from abc import ABC, abstractmethod
import mysql.connector

class BaseDAO(ABC):
    def __init__(self, db_config):
        self.db_config = db_config
    

    def _get_connection(self):
        try:
            cfg = self.db_config or {}
            return mysql.connector.connect(
                host=cfg.get("host") or "127.0.0.1",
                user=cfg.get("user") or "root",
                password=cfg.get("password") or "",
                database=cfg.get("database") or "restaurante_poo",
                port=int(cfg.get("port") or 3306)
            )
        except mysql.connector.Error as err:
            raise ConnectionAbortedError(f"Problemas ao conectar: {err}")
        
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
