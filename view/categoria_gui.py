import tkinter as tk
from tkinter import messagebox, ttk


class Categoria_View:
    def __init__(self, master=None):
        self.controller = None
        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()

        self.root.title("Cadastro de Categoria")
        self.root.geometry("800x500")

        self.var_id = tk.StringVar(self.root)
        self.var_nome = tk.StringVar(self.root)

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE CATEGORIA", font=("Arial", 14, "bold"), pady=10).pack()

        frame_form = tk.LabelFrame(self.root, text="Dados da Categoria", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Nome:").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_nome, width=35).grid(row=0, column=3, padx=5, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="ATUALIZAR", command=self._acao_editar, bg="#fff3cd", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos, bg="lightskyblue", width=15).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "nome")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")

        for col in self.colunas:
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        if self.controller:
            self.controller.list_categoria()
        
        if not isinstance(self.root, tk.Toplevel):
            self.root.mainloop()

    def get_dados_categoria(self, categoria_existente=None):
        return {"nome": self.var_nome.get()}

    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_categoria()
            self._acao_listar()

    def _acao_listar(self):
        if self.controller:
            try:
                self.controller.list_categoria()
            except Exception:
                pass

    def show_categoria(self, lista):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in lista:
            self.tree.insert("", "end", values=(p._id, p._nome))


    def show_clientes(self, lista):
        self.show_categoria(lista)

    def _acao_editar(self):
        if self.controller:
            self.controller.update_categoria()
            self._acao_listar()

    def get_id(self, operacao=""):
        val = self.var_id.get()
        return int(val) if val else None

    def _acao_excluir(self):
        if messagebox.askyesno("Confirmação", "Deseja Excluir?"):
            if self.controller:
                self.controller.delete_categoria()
                self._acao_listar()
                self.limpar_campos()

    def limpar_campos(self):
        for var in [self.var_id, self.var_nome]:
            var.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel[0])['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])

    def show_message(self, txt):
        messagebox.showinfo("Sucesso", txt)

    def show_error(self, err):
        messagebox.showerror("Erro", err)

    def show_categoria_details(self, categoria):
        if not categoria:
            return
        self.var_id.set(getattr(categoria, '_id', ''))
        self.var_nome.set(getattr(categoria, '_nome', ''))