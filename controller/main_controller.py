from model.dao.mesas_dao import Mesas_DAO
from model.dao.categoria_dao import Categoria_DAO
from model.dao.produto_dao import Produto_DAO
from model.dao.produto_categoria_dao import Produto_categoria_DAO

from controller.categoria_controller import Categoria_Controller
from controller.mesas_controller import Mesas_Controller
from controller.produto_controller import Produto_Controller
from controller.produto_categoria_controller import Produto_categoria_Controller

from view.categoria_gui import Categoria_View
from view.mesas_gui import  Mesas_View
from view.produto_gui import Produto_View



class Main_Controller:
    def __init__(self, main_view, db_config):
        self.main_view = main_view
        self.db_config = db_config

    def exibir_mesas(self):
        dao = Mesas_DAO(self.db_config)
        view = Mesas_View() 
        ctrl = Mesas_Controller(dao, view)
        view.run()

    def exibir_categoria(self):
        dao = Categoria_DAO(self.db_config)
        view = Categoria_View() 
        ctrl = Categoria_Controller(dao, view)
        view.run()

    def exibir_produto_categoria(self):
        dao_rel = Produto_categoria_DAO(self.db_config)
        dao_prod = Produto_DAO(self.db_config)
        dao_cat = Categoria_DAO(self.db_config)

        view = Produto_categoria_View()
        ctrl = Produto_categoria_Controller(dao_rel, dao_prod, dao_cat, view)

        view.controller = ctrl
        ctrl.list_related_dados()

    def exibir_produtos(self):
        dao = Produto_DAO(self.db_config)
        view = Produto_View() 
        ctrl = Produto_Controller(dao, view)
        view.run()