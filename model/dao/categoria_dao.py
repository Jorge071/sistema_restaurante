from model.categoria import Categoria
from model.dao.base_dao import BaseDAO
class Categoria_DAO(BaseDAO):
    def save(self, categoria:Categoria):
        sql = "insert into categoria (nome) values (%s)"
        
        values = (categoria._nome,)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        categoria._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return categoria
    
    def get_all(self):
        sql = "select id, nome from categoria"    
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        categoria = []
        for (id, nome) in cursor:
            categoria.append(Categoria(nome, id))
        cursor.close()
        conn.close()
        return categoria
    
    def get_by_id(self, id):
        sql = "select id, nome from categoria where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        categoria = None 
        if row:
           id, nome = row
           categoria = Categoria(nome, id)
        
        cursor.close()
        conn.close()    
        return categoria
    
    def delete(self, id):
        sql = "delete from categoria where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, categoria_atualizado:Categoria):
        sql = "update categoria set nome = %s where id = %s"
        values = (categoria_atualizado._nome, categoria_atualizado._id)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0