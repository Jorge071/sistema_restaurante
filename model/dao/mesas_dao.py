from model.mesas import Mesas
from model.dao.base_dao import BaseDAO

class Mesas_DAO(BaseDAO):
    def save(self, mesas: Mesas):

        sql = "insert into mesas (numero, capacidade, status) values (%s, %s, %s)"
        values = (mesas._numero, mesas._capacidade, mesas._status)

        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            mesas._id = cursor.lastrowid
            conn.commit()
            return mesas
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def get_all(self):
        sql = "select id, numero, capacidade, status from mesas"    
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            lista = []
            for (id, numero, capacidade, status) in cursor:
                lista.append(Mesas(id, numero, capacidade, status))
            return lista
        finally:
            cursor.close()
            conn.close()
    
    def get_by_id(self, id):
        sql = "select id, numero, capacidade, status from mesas where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            mesas = None 
            if row:
                id, numero, capacidade, status = row
                mesas = Mesas(id, numero, capacidade, status)
            return mesas
        finally:
            cursor.close()
            conn.close()    
    
    def delete(self, id):
        sql = "delete from mesas where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def update(self, mesas_atualizado: Mesas):
        sql = "update mesas set numero = %s, capacidade = %s, status = %s where id = %s"
        values = (
            mesas_atualizado._numero, 
            mesas_atualizado._capacidade, 
            mesas_atualizado._status, 
            mesas_atualizado._id
        )
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_by_numero(self, numero):
        sql = "select id, numero, capacidade, status from mesas where numero = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (numero,))
            row = cursor.fetchone()
            if row:
                id, numero, capacidade, status = row
                return Mesas(id, numero, capacidade, status)
            return None
        finally:
            cursor.close()
            conn.close()