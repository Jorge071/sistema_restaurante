from model.produto import Produto
from model.dao.base_dao import BaseDAO
class Produto_DAO(BaseDAO):
    def save(self, produto:Produto):
        sql = "insert into produto (categoria_id, nome, valor) values (%s,%s,%s)"
        
        values = (produto._categoria_id, produto._nome, produto._valor)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        produto._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return produto
    
    def get_all(self):
        # Adicionamos um JOIN para buscar o nome da categoria na outra tabela
        sql = """
            SELECT p.id, p.categoria_id, p.nome, p.valor, c.nome 
            FROM produto p
            INNER JOIN categoria c ON p.categoria_id = c.id
        """    
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        produtos = []
        for (id, categoria_id, nome, valor, nome_categoria) in cursor:
            p = Produto(id, categoria_id, nome, valor)
            # Criamos um atributo dinâmico para o nome da categoria
            p._nome_categoria = nome_categoria 
            produtos.append(p)
        cursor.close()
        conn.close()
        return produtos
    
    def get_by_id(self, id):
        sql = "select id, categoria_id, nome, valor from produto where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        
        produto = None # Variável local
        if row:
           id, categoria_id, nome, valor = row
           produto = Produto(id, categoria_id, nome, valor)
        
        cursor.close()
        conn.close()    
        return produto
    
    def delete(self, id):
        sql = "delete from produto where id = %s"
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, produto_atualizado:Produto):
        sql = "update produto set categoria_id = %s, nome = %s , valor = %s where id = %s"
        values = (
        produto_atualizado._categoria_id,
        produto_atualizado._nome,
        produto_atualizado._valor,
        produto_atualizado._id
        )
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
