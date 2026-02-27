import tkinter as tk
from tkinter import messagebox, ttk

class Produto_View:
    def __init__(self, master=None):
        self.controller = None
        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()
            
        self.root.title("Gestão de Produtos")
        self.root.geometry("800x600")

        # Variáveis de Controle (Removido o var_valor da interface)
        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_categoria_str = tk.StringVar() # Para o Combobox (Ex: "1 - Bebidas")

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE PRODUTOS", font=("Arial", 16, "bold"), pady=10).pack()

        # --- FORMULÁRIO ---
        frame_form = tk.LabelFrame(self.root, text=" Dados do Produto ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        tk.Label(frame_form, text="Nome do Produto:").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_nome, width=35).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Categoria:").grid(row=1, column=0, sticky="e")
        self.combo_categorias = ttk.Combobox(frame_form, textvariable=self.var_categoria_str, width=30, state="readonly")
        self.combo_categorias.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        # --- BOTÕES ---
        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="ATUALIZAR", command=self._acao_editar, bg="#fff3cd", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos, width=15).pack(side=tk.LEFT, padx=5)

        # --- TABELA ---
        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both")

        # Colunas apenas com ID, Nome e Categoria
        self.colunas = ("id", "nome", "categoria")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome do Produto")
        self.tree.heading("categoria", text="Categoria")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("nome", width=350, anchor="w")
        self.tree.column("categoria", width=250, anchor="w")
        
        self.tree.pack(side="left", expand=True, fill="both")
        
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        if self.controller:
            self.controller.list_produto() # Chama o método do teu controller
        self.root.grab_set()

    # --- INTEGRAÇÃO COM CONTROLLER ---

    def get_dados_produto(self, obj=None):
        """Coleta os dados. Envia valor=0.0 fixo para não quebrar o Model/Banco"""
        try:
            cat_id = int(self.var_categoria_str.get().split(" - ")[0])
            return {
                "nome": self.var_nome.get(),
                "valor": 0.0, # Valor padrão oculto
                "categoria_id": cat_id
            }
        except:
            self.show_error("Selecione uma categoria!")
            return None

    def show_produto(self, lista):
        """Preenche a tabela"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in lista:
            # Tenta mostrar o nome da categoria (_nome_categoria), senão mostra o ID
            cat_display = getattr(p, '_nome_categoria', p._categoria_id)
            self.tree.insert("", "end", values=(p._id, p._nome, cat_display))

    def preencher_combo_categorias(self, lista_categorias):
        self.combo_categorias['values'] = [f"{c._id} - {c._nome}" for c in lista_categorias]

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None

    # --- AÇÕES ---

    def _acao_adicionar(self):
        self.controller.add_produto()
        self.limpar_campos()

    def _acao_editar(self):
        self.controller.update_produto()

    def _acao_excluir(self):
        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            self.controller.delete_produto()
            self.limpar_campos()

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])
            self.var_categoria_str.set(v[2])

    def limpar_campos(self):
        self.var_id.set("")
        self.var_nome.set("")
        self.var_categoria_str.set("")

    def show_message(self, m): messagebox.showinfo("Sucesso",)