from model.mesas import Mesas
from model.dao.base_dao import Base_DAO

class Mesas_DAO(Base_DAO):
    def save(self, mesas:Mesas):
        sql = "insert into mesas (id, numero, capacidade, status) values (%s, %s, %s, %s)"
        
        values = (mesas._id, )

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        mesas._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return mesas
    
    def get_all(self):
        sql = "select id, numero, capacidade, status from mesas"    
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        Mesas = []
        for (id, numero, capacidade, status) in cursor:
            Mesas.append(Mesas(id, numero, capacidade, status))
        cursor.close()
        conn.close()
        return Mesas
    
    def get_by_id(self, id):
        sql = "select id, numero, capacidade, status from mesas where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        mesas = None # Variável local
        if row:
           id, numero, capacidade, status = row
           mesas = Mesas(id, numero, capacidade, status)
        
        cursor.close()
        conn.close()    
        return mesas
    
    def delete(self, id):
        sql = "delete from mesas where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, mesas_atualizado:Mesas):
        sql = "update mesas set numero = %s, capacidade = %s, status = %s where id = %s"
        values = (mesas_atualizado._numero, mesas_atualizado._capacidade, mesas_atualizado._status, 
                   mesas_atualizado._id)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    