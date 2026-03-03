from model.produto import Produto
from model.dao.produto_dao import Produto_DAO

class Produto_Controller:

    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def carregar_categorias_combo(self):
        categorias = self.dao_categoria.get_all()
        self.view.preencher_combo_categorias(categorias)

    def add_produto(self):
        try:
            dados = self.view.get_dados_produto()
            novo = Produto(
                id=None,
                categoria_id=dados['categoria_id'],
                nome=dados['nome'],
                valor=dados['valor']
            )
            produto_salvo = self.dao.save(novo)
            self.view.show_message(f"Adicionado com ID: {produto_salvo._id}")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def update_produto(self):
        try:
            id_produto = self.view.get_id()
            produto_existente = self.dao.get_by_id(id_produto)

            if not produto_existente:
                self.view.show_error("Não encontrado!")
                return

            dados = self.view.get_dados_produto(produto_existente)

            produto_atualizado = Produto(
                id=id_produto,
                categoria_id=dados['categoria_id'],
                nome=dados['nome'],
                valor=dados['valor']
            )

            if self.dao.update(produto_atualizado):
                self.view.show_message("Atualizado com sucesso!")
            else:
                self.view.show_error("Erro ao atualizar!")

        except Exception as e:
            self.view.show_error(f"Erro ao atualizar: {str(e)}")

    def delete_produto(self):
        try:
            id_produto = self.view.get_id()

            if self.dao.delete(id_produto):
                self.view.show_message("Deletado com sucesso!")
            else:
                self.view.show_error("Não encontrado!")

        except Exception as e:
            self.view.show_error(f"Erro ao deletar: {str(e)}")

    def list_produto(self):
        try:
            produtos = self.dao.get_all()
            self.view.show_produto(produtos)
        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    def list_produto_by_id(self):
        try:
            id_produto = self.view.get_id()
            produto = self.dao.get_by_id(id_produto)

            if produto is None:
                self.view.show_error("Não encontrado!")
                return

            self.view.show_produto_details(produto)

        except Exception as e:
            self.view.show_error(f"Erro ao buscar: {str(e)}")