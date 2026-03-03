from model.comanda_produto import Comanda_Produto


class Comanda_Produto_Controller:

    def __init__(self, dao_com_prod, dao_prod, dao_com, view):
        self.dao_com_prod = dao_com_prod
        self.dao_prod = dao_prod
        self.dao_com = dao_com
        self.view = view
        self.view.controller = self

    # 🔹 Adicionar
    def add_comanda_produto(self):
        try:
            dados = self.view.get_dados_comanda_produto()

            nova_relacao = Comanda_Produto(
                dados['comanda_id'],
                dados['produto_id']
            )

            self.dao_com_prod.save(nova_relacao)
            self.view.show_message("Vínculo criado com sucesso!")

        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    # 🔹 Atualizar (trocar produto)
    def update_comanda_produto(self):
        try:
            dados = self.view.get_dados_comanda_produto()

            if self.dao_com_prod.update(
                dados['comanda_id'],
                dados['produto_id_antigo'],
                dados['produto_id_novo']
            ):
                self.view.show_message("Vínculo atualizado com sucesso!")
            else:
                self.view.show_error("Vínculo não encontrado!")

        except Exception as e:
            self.view.show_error(f"Erro ao atualizar: {str(e)}")

    # 🔹 Deletar
    def delete_comanda_produto(self):
        try:
            dados = self.view.get_dados_comanda_produto()

            if self.dao_com_prod.delete(
                dados['comanda_id'],
                dados['produto_id']
            ):
                self.view.show_message("Vínculo excluído com sucesso!")
            else:
                self.view.show_error("Vínculo não encontrado!")

        except Exception as e:
            self.view.show_error(f"Erro ao excluir: {str(e)}")

    # 🔹 Listar
    def list_comanda_produto(self):
        try:
            lista = self.dao_com_prod.get_all()
            self.view.show_comanda_produto(lista)

        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    # 🔹 Carregar combos aaaaaaaaaaaaaaaaaaaaaaaaaaa
    def list_related_dados(self):
        try:
            self.view.preencher_combo_produtos(self.dao_prod.get_all())
            self.view.preencher_combo_comandas(self.dao_com.get_all())
            self.view.run()

        except Exception as e:
            self.view.show_error(f"Algum erro ao carregar os dados: {str(e)}")
