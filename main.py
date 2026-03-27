from dotenv import load_dotenv
import os
from view.main_gui2 import Main_Gui2
from controller.main_controller import Main_Controller

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

def main():
    view_principal = Main_Gui2()
    controller_geral = Main_Controller(view_principal, DB_CONFIG)
    view_principal.controller = controller_geral
    view_principal.run()

if __name__ == "__main__":
    main()
