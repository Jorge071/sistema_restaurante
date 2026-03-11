import tkinter as tk
from tkinter import ttk  # Importação necessária para as abas

class Main_Gui:

    def __init__(self):
        self.controller = None

        self.root = tk.Tk()
        self.root.title("Sistema de Gestão")
        self.root.state("zoomed")

        self._setup_menu()

        # 1. Criação do Notebook principal
        # expand=True e fill="both" garantem que as abas ocupem toda a tela
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # 2. Criação das abas (Frames)
        self.aba_inicio = ttk.Frame(self.notebook)
        self.aba_mesas = ttk.Frame(self.notebook)
        self.aba_categoria = ttk.Frame(self.notebook)
        self.aba_produtos = ttk.Frame(self.notebook)
        self.aba_comanda = ttk.Frame(self.notebook)

        # 3. Adicionando as abas ao Notebook com seus respectivos títulos
        self.notebook.add(self.aba_inicio, text="Início")
        self.notebook.add(self.aba_mesas, text="Mesas")
        self.notebook.add(self.aba_categoria, text="Categorias")
        self.notebook.add(self.aba_produtos, text="Produtos")
        self.notebook.add(self.aba_comanda, text="Comanda Produto")

        # Movi a sua mensagem de boas-vindas para a aba "Início"
        tk.Label(
            self.aba_inicio,
            text="Seja Bem-vindo ao Sistema",
            font=("Arial", 16)
        ).pack(expand=True)

        # Exemplo: Textos temporários para você visualizar que as abas funcionam
        tk.Label(self.aba_mesas, text="Conteúdo de Mesas virá aqui.").pack(pady=20)
        tk.Label(self.aba_categoria, text="Conteúdo de Categorias virá aqui.").pack(pady=20)


    def _setup_menu(self):
        barra_menu = tk.Menu(self.root)
        menu_cadastros = tk.Menu(barra_menu, tearoff=0)
        
        menu_cadastros.add_command(label="Mesas", command=self._abrir_mesas)
        menu_cadastros.add_command(label="Categoria", command=self._abrir_categoria)
        menu_cadastros.add_command(label="Produtos", command=self._abrir_produtos)
        menu_cadastros.add_command(label="Comanda_Produto", command=self._abrir_comanda_produto)
        
        menu_cadastros.add_separator()
        menu_cadastros.add_command(label="Sair", command=self.root.quit)

        barra_menu.add_cascade(label="Módulos", menu=menu_cadastros)
        self.root.config(menu=barra_menu)


    # --- Métodos de ação dos Menus ---
    # Agora, além de chamar o controller, eles mudam o foco para a aba clicada

    def _abrir_mesas(self):
        self.notebook.select(self.aba_mesas)  # Traz a aba "Mesas" para a frente
        if self.controller:
            # Dica: Você pode passar a aba para o controller saber onde desenhar os botões/tabelas
            self.controller.exibir_mesas(self.aba_mesas) 

    def _abrir_categoria(self):
        self.notebook.select(self.aba_categoria)
        if self.controller:
            self.controller.exibir_categoria(self.aba_categoria)

    def _abrir_produtos(self):
        self.notebook.select(self.aba_produtos)
        if self.controller:
            self.controller.exibir_produtos(self.aba_produtos)

    def _abrir_comanda_produto(self):
        self.notebook.select(self.aba_comanda)
        if self.controller:
            self.controller.exibir_comanda_produto(self.aba_comanda)

    def run(self):
        self.root.mainloop()

# Para testar visualmente, basta rodar:
if __name__ == "__main__":
    app = Main_Gui()
    app.run()