from dotenv import load_dotenv
import os
from view.main_gui import Main_Gui
from controller.main_controller import Main_Controller


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def main():
    view_principal = Main_Gui()
    controller_geral = Main_Controller(view_principal, DB_CONFIG)
    view_principal.controller = controller_geral
    view_principal.run()

if __name__ == "__main__":
    main()