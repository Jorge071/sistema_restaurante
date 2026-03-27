from model.dao.mesas_dao import Mesas_DAO
from model.dao.categoria_dao import Categoria_DAO
from model.dao.produto_dao import Produto_DAO
from model.dao.comanda_produto_dao import Comanda_Produto_DAO

from controller.categoria_controller import Categoria_Controller
from controller.mesas_controller import Mesas_Controller
from controller.produto_controller import Produto_Controller
from controller.comanda_produto_controller import Comanda_Produto_Controller

from view.categoria_gui import Categoria_View
from view.mesas_gui import Mesas_View
from view.produto_gui import Produto_View
from view.comanda_produto_gui import Comanda_produto_View

class Main_Controller:
    def __init__(self, main_view, db_config):
        self.main_view = main_view
        self.db_config = db_config

    def exibir_mesas(self, aba_master=None):
        dao = Mesas_DAO(self.db_config)
        view = Mesas_View(master=aba_master)
        ctrl = Mesas_Controller(dao, view)
        view.controller = ctrl
        view.run()

    def exibir_categoria(self, aba_master=None):
        dao = Categoria_DAO(self.db_config)
        view = Categoria_View(master=aba_master) 
        ctrl = Categoria_Controller(dao, view)
        view.controller = ctrl
        view.run()

    def exibir_produtos(self, aba_master=None):
        dao = Produto_DAO(self.db_config)
        view = Produto_View(master=aba_master) 
        ctrl = Produto_Controller(dao, view)
        
        dao_cat = Categoria_DAO(self.db_config)
        categorias = dao_cat.get_all()
        view.preencher_combo_categorias(categorias) 
        
        ctrl.list_produto() 
        view.controller = ctrl
        view.run()

    def exibir_comanda_produto(self, aba_master=None):
        dao_rel = Comanda_Produto_DAO(self.db_config)
        dao_prod = Produto_DAO(self.db_config)
        dao_cat = Mesas_DAO(self.db_config)

        view = Comanda_produto_View(master=aba_master)
        ctrl = Comanda_Produto_Controller(dao_rel, dao_prod, dao_cat, view)

        view.controller = ctrl
        ctrl.list_related_dados()
        view.run()