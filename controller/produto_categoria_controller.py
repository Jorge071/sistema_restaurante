from model.produto_categoria import Produto_categoria

class Produto_categoria_Controller:
    def __init__(self, dao_prod_cat, dao_prod, dao_cat, view):
        self.dao_prod_cat = dao_prod_cat
        self.dao_prod = dao_prod
        self.dao_cat = dao_cat
        self.view = view
        self.view.controller = self

    def add_produto_categoria(self):
        try:
            dados = self.view.get_dados_produto_categoria()

            nova_relacao = Produto_categoria(
                id=None,
                id_produto=dados['id_produto'],
                id_categoria=dados['id_categoria']
            )

            self.dao_prod_cat.save(nova_relacao)
            self.view.show_message("Vínculo criado com sucesso!")

        except Exception as e:
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def update_produto_categoria(self):
        try:
            id_rel = self.view.get_id()
            dados = self.view.get_dados_produto_categoria()

            rel_atu = Produto_categoria(
                id_rel,
                dados['id_produto'],
                dados['id_categoria']
            )

            if self.dao_prod_cat.update(rel_atu):
                self.view.show_message("Vínculo atualizado com sucesso!")
            else:
                self.view.show_error("Erro ao atualizar!")

        except Exception as e:
            self.view.show_error(f"Erro: {str(e)}")

    def delete_produto_categoria(self):
        try:
            id_rel = self.view.get_id()

            if self.dao_prod_cat.delete(id_rel):
                self.view.show_message("Vínculo excluído!")
            else:
                self.view.show_error("Não encontrado!")

        except Exception as e:
            self.view.show_error(f"Erro: {str(e)}")

    def list_produto_categoria(self):
        try:
            lista = self.dao_prod_cat.get_all()
            self.view.show_produto_categoria(lista)

        except Exception as e:
            self.view.show_error(f"Erro ao listar: {str(e)}")

    def list_related_dados(self):
        # Preenche os combos igual tu faz na movimentação
        self.view.preencher_combo_produtos(self.dao_prod.get_all())
        self.view.preencher_combo_categorias(self.dao_cat.get_all())
        self.view.run()