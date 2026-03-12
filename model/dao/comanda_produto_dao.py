from model.comanda_produto import Comanda_Produto
from model.dao.base_dao import BaseDAO

class Comanda_Produto_DAO(BaseDAO):

    def save(self, com_prod: Comanda_Produto):
        sql = """
            INSERT INTO comanda_produto (mesas_id, produto_id)
            VALUES (%s, %s)
            """

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
                cursor.execute(sql, (
                    com_prod._mesas_id,
                    com_prod._produto_id
                ))
                conn.commit()
                return com_prod

        except Exception as e:
                conn.rollback()
                raise e

        finally:
                cursor.close()
                conn.close()


    def get_all(self):
        sql = """
        SELECT mesas_id, produto_id, 
        FROM comanda_produto
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        lista = []

        for (mesas_id, produto_id) in cursor:
            lista.append(
                Comanda_Produto(mesas_id, produto_id, 0.0) 
            )

        cursor.close()
        conn.close()

        return lista

 
    def delete(self, mesas_id, produto_id):
        sql = """
        DELETE FROM comanda_produto
        WHERE mesas_id = %s AND produto_id = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (mesas_id, produto_id))
        conn.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()

        return affected_rows > 0


    def update(self, mesas_id, produto_id_antigo, produto_id_novo):
        sql = """
        UPDATE comanda_produto
        SET produto_id = %s
        WHERE mesas_id = %s AND produto_id = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(sql, (
            produto_id_novo,
            mesas_id,
            produto_id_antigo
        ))

        conn.commit()
        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()

        return affected_rows > 0
    
    def get_by_id(self, id):
        sql = """
        SELECT mesas_id, produto_id 
        FROM comanda_produto 
        WHERE mesas_id = %s
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        
        lista = []
        for (mesas_id, produto_id) in cursor:
            lista.append(
                Comanda_Produto(mesas_id, produto_id, 0.0)
            )
            
        cursor.close()
        conn.close()    
        
        return lista