import tkinter as tk

class Main_Gui:
    def __init__(self):
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Sistema de Gestão")
        self.root.state('zoomed')
        
        self._setup_menu()
        
        # Tela de boas-vindas simples
        tk.Label(self.root, text="Seja Bem-vindo ao Sistema", font=("Arial", 16)).pack(expand=True)

    def _setup_menu(self):
        barra_menu = tk.Menu(self.root)
        
        # Menu Cadastros
        menu_cadastros = tk.Menu(barra_menu, tearoff=0)
        menu_cadastros.add_command(label="Mesas", command=self._abrir_mesas)
        menu_cadastros.add_command(label="Categoria", command=self._abrir_categoria)
        menu_cadastros.add_command(label="Produtos", command=self._abrir_produtos)
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.root.quit)
        
        barra_menu.add_cascade(label="Módulos", menu=menu_cadastros)
        self.root.config(menu=barra_menu)

    def _abrir_mesas(self):
        if self.controller:
            self.controller.exibir_mesas()

    def _abrir_categoria(self):
        if self.controller:
            self.controller.exibir_categoria()
            
    def _abrir_produtos(self):
            if self.controller:
                self.controller.exibir_produtos()

    def run(self):
        self.root.mainloop()
    
    