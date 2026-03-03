from model.mesas import Mesas
from model.dao.mesas_dao import Mesas_DAO

class Mesas_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self


    def add_mesas(self):
        try:
            dados = self.view.get_dados_mesas()
            novo = Mesas(
                id=None,
                numero=dados['numero'],
                capacidade=dados['capacidade'],
                status=dados['status']
            )
            mesas_salvo = self.dao.save(novo)
            self.view.show_message(f"Mesa adicionada com ID: {mesas_salvo._id}")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar Mesa: {str(e)}")

    def update_mesas(self):
        try:
            id_mesas = self.view.get_id()
            mesas_existente = self.dao.get_by_id(id_mesas)
            if not mesas_existente:
                self.view.show_error("Mesa não encontrado!")
                return
            dados = self.view.get_dados_mesas(mesas_existente)
            mesas_atualizado = Mesas(
                id=id_mesas,
                numero=dados['numero'],
                capacidade=dados['capacidade'],
                status=dados['status']
            )
            if self.dao.update(mesas_atualizado):
                self.view.show_message("Mesa atualizada com sucesso!")
            else:
                self.view.show_error("Erro ao atualizar mesa!")
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar mesa: {str(e)}")

    def delete_mesas(self):
        try:
            id_mesas = self.view.get_id()
            if self.dao.delete(id_mesas):
                self.view.show_message("Mesa deletado com sucesso!")
            else:
                self.view.show_error("Mesa não encontrada!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar mesa: {str(e)}")

    def list_mesas(self):
        try:
            mesas = self.dao.get_all()
            self.view.show_mesas(mesas)
        except Exception as e:
            self.view.show_error(f"Erro ao listar mesas: {str(e)}")

    def list_mesa_by_id(self):
        try:
            id_mesas = self.view.get_id()
            mesas = self.dao.get_by_id(id_mesas)
            if mesas is None:
                self.view.show_error("Mesa não encontrada!")
                return
            self.view.show_mesas_details(mesas)
        except Exception as e:
            self.view.show_error(f"Erro ao buscar mesa: {str(e)}")
