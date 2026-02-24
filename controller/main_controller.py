from model.dao.mesas_dao import Mesas_DAO
from model.dao.categoria_dao import Categoria_DAO
from controller.categoria_controller import Categoria_Controller
from controller.mesas_controller import Mesas_Controller
from view.categoria_gui import Categoria_View
from view.mesas_gui import  Mesas_View

class Main_Controller:
    def __init__(self, main_view, db_config):
        self.main_view = main_view
        self.db_config = db_config

    def exibir_mesas(self):
        dao = Mesas_DAO(self.db_config)
        view = () 
        ctrl = Mesas_Controller(dao, view)
        view.run()

    def exibir_mesas(self):
        dao = Categoria_DAO(self.db_config)
        view = () 
        ctrl = Categoria_Controller(dao, view)
        view.run()