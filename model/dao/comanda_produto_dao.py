from model.comanda_produto import Comanda_Produto
from model.dao.base_dao import BaseDAO

class Comanda_Produto_DAO(BaseDAO):

    def save(self, com_prod: Comanda_Produto):
        sql = """
            INSERT INTO comanda_produto (mesa_id, produto_id)
            VALUES (%s, %s)
            """

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
                cursor.execute(sql, (
                    com_prod._mesa_id,
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
        SELECT mesa_id, produto_id
        FROM comanda_produto
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        lista = []

        for (mesa_id, produto_id) in cursor:
            lista.append(
                Comanda_Produto(mesa_id, produto_id, 0.0) 
            )

        cursor.close()
        conn.close()

        return lista

 
    def delete(self, mesa_id, produto_id):
        sql = """
        DELETE FROM comanda_produto
        WHERE mesa_id = %s AND produto_id = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (mesa_id, produto_id))
        conn.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()

        return affected_rows > 0


    def update(self, mesa_id, produto_id_antigo, produto_id_novo):
        sql = """
        UPDATE comanda_produto
        SET produto_id = %s
        WHERE mesa_id = %s AND produto_id = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(sql, (
            produto_id_novo,
            mesa_id,
            produto_id_antigo
        ))

        conn.commit()
        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()

        return affected_rows > 0
    
    def get_by_id(self, id):
        sql = """
        SELECT mesa_id, produto_id 
        FROM comanda_produto 
        WHERE mesa_id = %s
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        
        lista = []
        for (mesa_id, produto_id) in cursor:
            lista.append(
                Comanda_Produto(mesa_id, produto_id, 0.0)
            )
            
        cursor.close()
        conn.close()    
        
        return lista