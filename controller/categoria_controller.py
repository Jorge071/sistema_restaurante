from model.dao.categoria_dao import Categoria_DAO
from model.categoria import Categoria

class Categoria_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def add_categoria(self):
        try:
            dados = self.view.get_dados_categoria()
            novo = Categoria(
                id=None,
                nome=dados['nome']
            )
            categoria_salvo = self.dao.save(novo)
            self.view.show_message(f"categoria adicionado com ID: {categoria_salvo._id}")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def update_categoria(self):
        try:
            id_categoria = self.view.get_id()
            categoria_existente = self.dao.get_by_id(id_categoria)
            if not categoria_existente:
                self.view.show_error("não encontrado!")
                return
            dados = self.view.get_dados_categoria(categoria_existente)
            categoria_atualizado = Categoria(
                id=id_categoria,
                nome=dados['nome'],
            )
            if self.dao.update(categoria_atualizado):
                self.view.show_message("atualizado com sucesso!")
            else:
                self.view.show_error("Erro ao atualizar!")
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar: {str(e)}")

    def delete_categoria(self):
        try:
            id_categoria = self.view.get_id()
            if self.dao.delete(id_categoria):
                self.view.show_message(" deletado com sucesso!")
            else:
                self.view.show_error(" não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar: {str(e)}")

    def list_categoria(self):
        try:
            categoria = self.dao.get_all()
            self.view.show_clientes(categoria)
        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    def list_categoria_by_id(self):
        try:
            id_categoria = self.view.get_id()
            categoria = self.dao.get_by_id(id_categoria)
            if categoria is None:
                self.view.show_error("não encontrado!")
                return
            self.view.show_categoria_details(categoria)
        except Exception as e:
            self.view.show_error(f"Erro ao buscar: {str(e)}")