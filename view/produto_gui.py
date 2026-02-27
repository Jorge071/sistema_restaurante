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

        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_categoria_str = tk.StringVar() 

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE PRODUTOS", font=("Arial", 16, "bold"), pady=10).pack()

        frame_form = tk.LabelFrame(self.root, text=" Cadastro ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_nome, width=35).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Categoria:").grid(row=0, column=2, sticky="e")
        self.combo_categorias = ttk.Combobox(frame_form, textvariable=self.var_categoria_str, state="readonly", width=25)
        self.combo_categorias.grid(row=0, column=3, padx=5, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR", command=self._acao_adicionar, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "categoria"), show="headings")
        self.tree.heading("id", text="ID"); self.tree.heading("nome", text="Nome"); self.tree.heading("categoria", text="Categoria")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    # --- O SEGREDO PARA SALVAR ESTÁ AQUI ---
    def get_dados_produto(self, obj=None):
        """O Controller chama este método. Se o nome for diferente, não salva."""
        try:
            # Pega o ID da categoria (Ex: "1 - Bebidas" vira 1)
            cat_id = int(self.var_categoria_str.get().split(" - ")[0])
            return {
                "nome": self.var_nome.get(),
                "categoria_id": cat_id,
                "valor": 0.0  # Enviamos 0.0 fixo porque o Model/Controller exigem esse campo
            }
        except Exception:
            self.show_error("Selecione uma categoria antes de salvar!")
            return None

    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_produto() # Chama o salvar do Controller
            self.controller.list_produto() # Atualiza a tabela
            self.limpar_campos()

    def show_produto(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in lista:
            cat = getattr(p, '_nome_categoria', p._categoria_id)
            self.tree.insert("", "end", values=(p._id, p._nome, cat))

    def preencher_combo_categorias(self, lista):
        self.combo_categorias['values'] = [f"{c._id} - {c._nome}" for c in lista]

    def run(self):
        if self.controller: self.controller.list_produto()
        self.root.grab_set()

    def show_message(self, m): messagebox.showinfo("Sucesso", m)
    def show_error(self, e): messagebox.showerror("Erro", e)
    def limpar_campos(self):
        self.var_nome.set(""); self.var_categoria_str.set("")
    def get_id(self): return int(self.var_id.get()) if self.var_id.get() else None
    def _acao_excluir(self): self.controller.delete_produto()