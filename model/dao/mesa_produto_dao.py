from model.mesa_produto import Mesa_Produto
from model.dao.base_dao import BaseDAO

class Mesa_Produto_DAO(BaseDAO):

    def save(self, com_prod: Mesa_Produto):
        sql = """
            INSERT INTO mesa_produto (mesas_id, produto_id, preco_unitario)
            VALUES (%s, %s, %s)
            """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, (
                com_prod._mesas_id,
                com_prod._produto_id,
                com_prod._preco_unitario
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_all(self):
        sql = """
        SELECT 
            cp.id,  # <-- Adicionando o ID aqui
            cp.mesas_id, 
            cp.produto_id, 
            cp.preco_unitario,
            p.nome AS produto_nome,
            c.nome AS categoria_nome
        FROM mesa_produto cp
        JOIN produto p ON cp.produto_id = p.id
        JOIN categoria c ON p.categoria_id = c.id
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        lista = []
        for (id, mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome) in cursor:
            lista.append(
                Mesa_Produto(mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome, id=id) 
            )

        cursor.close()
        conn.close()
        return lista


    def delete(self, id):
        sql = "DELETE FROM mesa_produto WHERE id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,)) 
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, mesas_id, produto_id_antigo, produto_id_novo, preco_unitario_novo):
        sql = """
        UPDATE mesa_produto
        SET produto_id = %s, preco_unitario = %s
        WHERE mesas_id = %s AND produto_id = %s
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (
                produto_id_novo,
                preco_unitario_novo,
                mesas_id,
                produto_id_antigo
            ))

            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows > 0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()
    
    def get_by_id(self, id_mesa):
        sql = """
        SELECT 
            cp.id, 
            cp.mesas_id, 
            cp.produto_id, 
            cp.preco_unitario,
            p.nome AS produto_nome,
            c.nome AS categoria_nome
        FROM mesa_produto cp
        JOIN produto p ON cp.produto_id = p.id
        JOIN categoria c ON p.categoria_id = c.id
        WHERE cp.mesas_id = %s
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_mesa,))
        
        lista = []
        for (id, mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome) in cursor:
            lista.append(
                Mesa_Produto(mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome, id=id)
            )
            
        cursor.close()
        conn.close()    
        
        return lista
        
