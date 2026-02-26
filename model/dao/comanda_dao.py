from model.comanda import Comanda
from model.dao.base_dao import BaseDAO
class Comanda_DAO(BaseDAO):
    def save(self, comanda:Comanda):
        sql = "insert into comanda (mesa_id, valor_total) values (%s,%s)"
        
        values = (comanda._mesa_id, comanda._valor_total)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        comanda._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return comanda
    
    def get_all(self):
        sql = "select id, mesa_id, valor_total from comanda"    
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        comanda = []
        for (id, mesa_id, valor_total) in cursor:
            comanda.append(Comanda(id, mesa_id, valor_total))
        cursor.close()
        conn.close()
        return comanda
    
    def get_by_id(self, id):
        sql = "select id, mesa_id, valor_total from comanda where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        comanda = None # Variável local
        if row:
           id, mesa_id,valor_total = row
           comanda = Comanda(id, mesa_id, valor_total)
        
        cursor.close()
        conn.close()    
        return comanda
    
    def delete(self, id):
        sql = "delete from comanda where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, comanda_atualizado:Comanda):
        sql = "update comanda set mesa_id = %s, valor_total = %s where id = %s"
        values = (
        comanda_atualizado._mesa_id,
        comanda_atualizado._valor_total,
        comanda_atualizado._id
        )
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
