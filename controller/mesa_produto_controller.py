from model.mesa_produto import Mesa_Produto

class Mesa_Produto_Controller:

    def __init__(self, dao_com_prod, dao_prod, dao_mesa, view):
        self.dao_com_prod = dao_com_prod
        self.dao_prod = dao_prod
        self.dao_mesa = dao_mesa
        self.view = view
        self.view.controller = self
        self.mesa_atual_filtro = None 

    def add_mesa_produto(self):
        mesa_id, produtos_selecionados = self.view.get_dados_selecionados()
        
        if not mesa_id: return
        if not produtos_selecionados:
            self.view.show_error("Selecione pelo menos um produto!")
            return

        try:
            for prod in produtos_selecionados:
                nova_relacao = Mesa_Produto(
                    mesas_id=mesa_id,
                    produto_id=prod["id"],
                    preco_unitario=prod["valor"]
                )
                self.dao_com_prod.save(nova_relacao)
                
            self.view.show_message("Produtos adicionados com sucesso!")
            if self.mesa_atual_filtro:
                self.list_by_mesa(self.mesa_atual_filtro)
            else:
                self.list_mesa_produto()
                
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def delete_mesa_produto(self, id):
        try:
            if self.dao_com_prod.delete(id):
                self.view.show_message("Produto removido da mesa com sucesso!")
                if self.mesa_atual_filtro:
                    self.list_by_mesa(self.mesa_atual_filtro)
                else:
                    self.list_mesa_produto()
            else:
                self.view.show_error("Vínculo não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao excluir: {str(e)}")

    def list_mesa_produto(self):
        try:
            self.mesa_atual_filtro = None 
            
            lista = self.dao_com_prod.get_all()
            self.view.show_mesa_produto(lista)
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
            self.mesa_atual_filtro = mesa_id 
            
            lista = self.dao_com_prod.get_by_id(mesa_id)
            self.view.show_mesa_produto(lista)
        except Exception as e:
            self.view.show_error(f"Erro ao buscar conta da mesa: {str(e)}")