from model.produto_categoria import Produto_categoria
from model.dao.base_dao import BaseDAO

class Produto_categoria_DAO(BaseDAO):
    def __init__(self, db_config):
        super().__init__(db_config)

    def save(self, prod_cat: Produto_categoria):
        sql = """insert into produto_categoria (id_produto, id_categoria)
                 values (%s, %s)"""

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(sql, (prod_cat._id_produto, prod_cat._id_categoria))
            prod_cat._id = cursor.lastrowid
            conn.commit()
            return prod_cat
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_all(self):
        sql = """
        select pc.id, pc.id_produto, pc.id_categoria,
               p.nome, c.nome
        from produto_categoria pc
        inner join produto p on pc.id_produto = p.id
        inner join categoria c on pc.id_categoria = c.id
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        lista = []
        for (id, id_prod, id_cat, nome_prod, nome_cat) in cursor:
            lista.append(
                Produto_categoria(id, id_prod, id_cat, nome_prod, nome_cat)
            )

        cursor.close()
        conn.close()
        return lista

    def get_by_id(self, id):
        sql = """select id, id_produto, id_categoria
                 from produto_categoria
                 where id = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()

        prod_cat = None
        if row:
            id, id_prod, id_cat = row
            prod_cat = Produto_categoria(id, id_prod, id_cat)

        cursor.close()
        conn.close()
        return prod_cat

    def delete(self, id):
        sql = "delete from produto_categoria where id = %s"

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()
        return affected_rows > 0

    def update(self, prod_cat: Produto_categoria):
        sql = """update produto_categoria
                 set id_produto = %s,
                     id_categoria = %s
                 where id = %s"""

        values = (prod_cat._id_produto,
                  prod_cat._id_categoria,
                  prod_cat._id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()

        affected_rows = cursor.rowcount

        cursor.close()
        conn.close()
        return affected_rows > 0