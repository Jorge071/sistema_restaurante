from model.comanda_produto import Comanda_Produto
from model.dao.base_dao import BaseDAO

class Comanda_Produto_DAO(BaseDAO):

    def save(self, com_prod: Comanda_Produto):
        sql = """
            INSERT INTO comanda_produto (mesas_id, produto_id, preco_unitario)
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
        # O SQL agora busca o nome do produto, o valor registrado na venda e o nome da categoria
        sql = """
        SELECT 
            cp.mesas_id, 
            cp.produto_id, 
            cp.preco_unitario,
            p.nome AS produto_nome,
            c.nome AS categoria_nome
        FROM comanda_produto cp
        JOIN produto p ON cp.produto_id = p.id
        JOIN categoria c ON p.categoria_id = c.id
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        lista = []
        for (mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome) in cursor:
            lista.append(
                Comanda_Produto(mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome) 
            )

        cursor.close()
        conn.close()
        return lista

    def delete(self, mesas_id, produto_id):
        sql = "DELETE FROM comanda_produto WHERE mesas_id = %s AND produto_id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (mesas_id, produto_id))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, mesas_id, produto_id_antigo, produto_id_novo, preco_unitario_novo):
        sql = """
        UPDATE comanda_produto
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
            cp.mesas_id, 
            cp.produto_id, 
            cp.preco_unitario,
            p.nome AS produto_nome,
            c.nome AS categoria_nome
        FROM comanda_produto cp
        JOIN produto p ON cp.produto_id = p.id
        JOIN categoria c ON p.categoria_id = c.id
        WHERE cp.mesas_id = %s
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_mesa,))
        
        lista = []
        for (mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome) in cursor:
            lista.append(
                Comanda_Produto(mesas_id, produto_id, preco_unitario, produto_nome, categoria_nome)
            )
            
        cursor.close()
        conn.close()    
        
        return lista