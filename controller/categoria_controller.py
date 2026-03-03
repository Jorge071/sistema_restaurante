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
            
            # Validation - ensure dados is a dict and has 'nome' key
            if dados is None:
                self.view.show_error("Erro: dados vazios")
                return
            
            if not isinstance(dados, dict):
                self.view.show_error(f"Erro: tipo inválido {type(dados)}")
                return
            
            if 'nome' not in dados:
                self.view.show_error("Erro: nome não encontrado nos dados")
                return
            
            nome = dados['nome']
            if isinstance(nome, str):
                nome = nome.strip()
            
            if not nome:
                self.view.show_error("Erro: nome vazio! Digite um nome para a categoria")
                return
            
            novo = Categoria(
                nome=nome,
                id=None
            )
            categoria_salvo = self.dao.save(novo)
            self.view.show_message(f"categoria adicionado com ID: {categoria_salvo._id}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.view.show_error(f"Erro ao adicionar: {str(e)}")

    def update_categoria(self):
        try:
            id_categoria = self.view.get_id()
            if not id_categoria:
                self.view.show_error("Selecione uma categoria para atualizar")
                return
            
            categoria_existente = self.dao.get_by_id(id_categoria)
            if not categoria_existente:
                self.view.show_error("não encontrado!")
                return
            
            dados = self.view.get_dados_categoria(categoria_existente)
            if dados is None or 'nome' not in dados:
                self.view.show_error("Dados inválidos")
                return
            
            categoria_atualizado = Categoria(
                nome=dados['nome'].strip(),
                id=id_categoria
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
            if not id_categoria:
                self.view.show_error("Selecione uma categoria para deletar")
                return
            
            if self.dao.delete(id_categoria):
                self.view.show_message("deletado com sucesso!")
            else:
                self.view.show_error("não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar: {str(e)}")

    def list_categoria(self):
        try:
            categoria = self.dao.get_all()
            self.view.show_categoria(categoria)
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
