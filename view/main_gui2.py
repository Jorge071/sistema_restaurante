import customtkinter as ctk
import tkinter as tk

class Main_Gui2:
    def __init__(self):
        self.controller = None

        self.root = ctk.CTk()
        self.root.title("Sistema de Gestão")
        self.root.geometry("1024x768")
        
        try:
            self.root.state("zoomed")
        except:
            self.root.attributes('-zoomed', True)

        self._setup_menu()

        self.tabview = ctk.CTkTabview(self.root, command=self._ao_mudar_aba)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)

        self.aba_inicio = self.tabview.add("Início")
        self.aba_mesas = self.tabview.add("Mesas")
        self.aba_categoria = self.tabview.add("Categorias")
        self.aba_produtos = self.tabview.add("Produtos")
        self.aba_comanda = self.tabview.add("Comanda Produto")

        ctk.CTkLabel(
            self.aba_inicio, 
            text="Seja Bem-vindo ao Sistema", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(expand=True)

    def _setup_menu(self):
        barra_menu = tk.Menu(self.root)
        menu_cadastros = tk.Menu(barra_menu, tearoff=0)
        
        menu_cadastros.add_command(label="Mesas", command=self._abrir_mesas)
        menu_cadastros.add_command(label="Categoria", command=self._abrir_categoria)
        menu_cadastros.add_command(label="Produtos", command=self._abrir_produtos)
        menu_cadastros.add_command(label="Comanda Produto", command=self._abrir_comanda_produto)
        
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.root.quit)

    def _ao_mudar_aba(self):
        if not self.controller:
            return
            
        aba_selecionada = self.tabview.get()
        
        if aba_selecionada == "Mesas":
            self.controller.exibir_mesas(self.aba_mesas)
        elif aba_selecionada == "Categorias":
            self.controller.exibir_categoria(self.aba_categoria)
        elif aba_selecionada == "Produtos":
            self.controller.exibir_produtos(self.aba_produtos)
        elif aba_selecionada == "Comanda Produto":
            self.controller.exibir_comanda_produto(self.aba_comanda)

    def _abrir_mesas(self):
        self.tabview.set("Mesas")
        self._ao_mudar_aba()

    def _abrir_categoria(self):
        self.tabview.set("Categorias")
        self._ao_mudar_aba()

    def _abrir_produtos(self):
        self.tabview.set("Produtos")
        self._ao_mudar_aba()

    def _abrir_comanda_produto(self):
        self.tabview.set("Comanda Produto")
        self._ao_mudar_aba()

    def run(self):
        self.root.mainloop()