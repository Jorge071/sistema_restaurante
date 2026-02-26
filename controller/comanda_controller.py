from model.comanda import Comanda
from model.dao.comanda_dao import Comanda_DAO

class Comanda_Controller:

    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def add_comanda(self):
        try:
            dados = self.view.get_dados_comanda()
            novo = Comanda(
                id=None,
                mesa_id=dados['mesa_id'],
                valor_total=dados['valor_total']
            )
            comanda_salvo = self.dao.save(novo)
            self.view.show_message(f"Adicionada com ID: {comanda_salvo._id}")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def update_comanda(self):
        try:
            id_comanda = self.view.get_id()
            comanda_existente = self.dao.get_by_id(id_comanda)

            if not comanda_existente:
                self.view.show_error("Não encontrada!")
                return

            dados = self.view.get_dados_comanda(comanda_existente)

            comanda_atualizado = Comanda(
                id=id_comanda,
                mesa_id=dados['mesa_id'],
                valor_total=dados['valor_total']
            )

            if self.dao.update(comanda_atualizado):
                self.view.show_message("Atualizada com sucesso!")
            else:
                self.view.show_error("Erro ao atualizar!")

        except Exception as e:
            self.view.show_error(f"Erro ao atualizar: {str(e)}")

    def delete_comanda(self):
        try:
            id_comanda = self.view.get_id()

            if self.dao.delete(id_comanda):
                self.view.show_message("Deletada com sucesso!")
            else:
                self.view.show_error("Não encontrada!")

        except Exception as e:
            self.view.show_error(f"Erro ao deletar: {str(e)}")

    def list_comanda(self):
        try:
            comandas = self.dao.get_all()
            self.view.show_comanda(comandas)
        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    def list_comanda_by_id(self):
        try:
            id_comanda = self.view.get_id()
            comanda = self.dao.get_by_id(id_comanda)

            if comanda is None:
                self.view.show_error("Não encontrada!")
                return

            self.view.show_comanda_details(comanda)

        except Exception as e:
            self.view.show_error(f"Erro ao buscar: {str(e)}")
