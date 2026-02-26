import tkinter as tk
from tkinter import messagebox, ttk

class Produto_View:
    def __init__(self):
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Cadastrinho de produtos")
        self.root.geometry("800x600")

        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_valor = tk.StringVar()
        self.var_estoque = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE PRODUTOS", font=("Arial", 14, "bold"), pady=10).pack()

        # --- Frame do Formulário ---
        frame_form = tk.LabelFrame(self.root, text=" Dados do Produto ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Nome:").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_nome, width=35).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Preço Unit.:").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_valor, width=15).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Estoque:").grid(row=1, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_estoque, width=15).grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
        
        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, 
                  bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="ATUALIZAR", command=self._acao_editar, 
                  bg="#fff3cd", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, 
                  bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos, bg="lightskyblue",
                  width=15).pack(side=tk.LEFT, padx=5)

        # --- Tabela ---
        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "nome", "preco", "qtd", "total")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("preco", text="Preço Unit.")
        self.tree.heading("qtd", text="Estoque")
        self.tree.heading("total", text="Total R$")

        for col in self.colunas: self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)
    
    def run(self):
        self.root.after(200, self._acao_listar)
        self.root.grab_set()
        self.root.focus_force()

    def get_dados_produto(self, produto_existente=None):
        """ Retorna o dicionário com o que foi digitado nas caixas de texto """
        try:
            return {
                "nome": self.var_nome.get(),
                "valor": float(self.var_valor.get()),
                "estoque": int(self.var_estoque.get())
            }
        except ValueError:
            self.show_error("Dados numéricos inválidos!")
            return None
        
    def _acao_adicionar(self): 
        self.controller.add_produto()
        self._acao_listar()

    def _acao_listar(self): 
        if self.controller: self.controller.list_produtos()

    def show_produtos(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in lista:
            
            self.tree.insert("", "end", values=(
                p._id, p._nome, f"R$ {p._valor:.2f}", 
                p._estoque, f"R$ {(p._valor * p._estoque):.2f}"
            ))                    

    def _acao_editar(self): 
        self.controller.update_produto()
        self._acao_listar()

    def get_id(self, operacao=""):
        val = self.var_id.get()
        return int(val) if val else None        

    def _acao_excluir(self): 
        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            self.controller.delete_produto()
            self._acao_listar()
            self.limpar_campos()

    def limpar_campos(self):
        for var in [self.var_id, self.var_nome, self.var_valor, self.var_estoque]: var.set("")


    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])
            self.var_valor.set(str(v[2]).replace("R$ ", ""))
            self.var_estoque.set(v[3])

    def show_message(self, txt): messagebox.showinfo("Sucesso", txt)

    def show_error(self, err): messagebox.showerror("Erro", err)