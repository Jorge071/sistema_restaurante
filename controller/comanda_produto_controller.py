from model.comanda_produto import Comanda_Produto

class Comanda_Produto_Controller:

    def __init__(self, dao_com_prod, dao_prod, dao_mesa, view):
        self.dao_com_prod = dao_com_prod
        self.dao_prod = dao_prod
        self.dao_mesa = dao_mesa
        self.view = view
        self.view.controller = self

    def add_comanda_produto(self):
        mesa_id, produtos_selecionados = self.view.get_dados_selecionados()
        
        if not mesa_id: return
        if not produtos_selecionados:
            self.view.show_error("Selecione pelo menos um produto!")
            return

        try:
            # Salva cada produto que estava com o checkbox marcado
            for prod in produtos_selecionados:
                nova_relacao = Comanda_Produto(
                    mesas_id=mesa_id,
                    produto_id=prod["id"],
                    preco_unitario=prod["valor"] # Pega o valor real do produto no momento
                )
                self.dao_com_prod.save(nova_relacao)
                
            self.view.show_message("Produtos adicionados com sucesso!")
            self.list_comanda_produto() # Atualiza a tabela e a soma do valor total

        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def delete_comanda_produto(self, mesa_id, produto_id):
        try:
            if self.dao_com_prod.delete(mesa_id, produto_id):
                self.view.show_message("Produto removido da mesa com sucesso!")
                self.list_comanda_produto()
            else:
                self.view.show_error("Vínculo não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao excluir: {str(e)}")

    def list_comanda_produto(self):
        try:
            lista = self.dao_com_prod.get_all()
            self.view.show_comanda_produto(lista)
        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    def list_related_dados(self):
        try:
            self.view.preencher_combo_mesas(self.dao_mesa.get_all())
            self.view.preencher_checkbox_produtos(self.dao_prod.get_all())
        except Exception as e:
            self.view.show_error(f"Algum erro ao carregar dados: {str(e)}")

    def list_by_mesa(self, mesa_id):
        try:
            # Em vez de get_all(), usamos o get_by_id() passando a mesa
            lista = self.dao_com_prod.get_by_id(mesa_id)
            # A view vai desenhar a tabela e somar O VALOR TOTAL apenas dessa lista!
            self.view.show_comanda_produto(lista)
        except Exception as e:
            self.view.show_error(f"Erro ao buscar conta da mesa: {str(e)}")