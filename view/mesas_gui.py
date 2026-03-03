import tkinter as tk
from tkinter import messagebox, ttk


class Mesas_View:
    def __init__(self, master=None):
        self.controller = None
        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()

        self.root.title("Cadastro de Mesas")
        self.root.geometry("800x500")

        self.var_id = tk.StringVar(self.root)
        self.var_numero = tk.StringVar(self.root)
        self.var_capacidade = tk.StringVar(self.root)
        self.var_status = tk.StringVar(self.root)

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE MESAS", font=("Arial", 14, "bold"), pady=10).pack()

        frame_form = tk.LabelFrame(self.root, text="Dados da Mesa", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Número:").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_numero, width=15).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Capacidade:").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_capacidade, width=10).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Status:").grid(row=1, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_status, width=15).grid(row=1, column=3, padx=5, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="ATUALIZAR", command=self._acao_editar, bg="#fff3cd", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos, bg="lightskyblue", width=15).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "numero", "capacidade", "status")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("numero", text="Número")
        self.tree.heading("capacidade", text="Capacidade")
        self.tree.heading("status", text="Status")

        for col in self.colunas:
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        if self.controller:
            self.controller.list_mesas()
        
        if not isinstance(self.root, tk.Toplevel):
            self.root.mainloop()

    def get_dados_mesas(self, mesas_existente=None):
        try:
            numero = int(self.var_numero.get()) if self.var_numero.get() else None
        except ValueError:
            self.show_error('Número inválido')
            return None

        try:
            capacidade = int(self.var_capacidade.get()) if self.var_capacidade.get() else 0
        except ValueError:
            self.show_error('Capacidade inválida')
            return None

        return {
            "numero": numero,
            "capacidade": capacidade,
            "status": self.var_status.get()
        }

    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_mesas()
            self._acao_listar()

    def _acao_listar(self):
        if self.controller:
            self.controller.list_mesas()

    def show_mesas(self, lista):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in lista:
            self.tree.insert("", "end", values=(p._id, p._numero, p._capacidade, p._status))

    def _acao_editar(self):
        if self.controller:
            self.controller.update_mesas()
            self._acao_listar()

    def get_id(self, operacao=""):
        val = self.var_id.get()
        return int(val) if val else None

    def _acao_excluir(self):
        if messagebox.askyesno("Confirmação", "Deseja Excluir?"):
            if self.controller:
                self.controller.delete_mesas()
                self._acao_listar()
                self.limpar_campos()

    def limpar_campos(self):
        for var in [self.var_id, self.var_numero, self.var_capacidade, self.var_status]:
            var.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel[0])['values']
            self.var_id.set(v[0])
            self.var_numero.set(str(v[1]))
            self.var_capacidade.set(str(v[2]))
            self.var_status.set(str(v[3]))

    def show_mesas_details(self, mesas):
        if not mesas:
            return
        self.var_id.set(getattr(mesas, '_id', ''))
        self.var_numero.set(str(getattr(mesas, '_numero', '')))
        self.var_capacidade.set(str(getattr(mesas, '_capacidade', '')))
        self.var_status.set(getattr(mesas, '_status', ''))

    def show_message(self, txt):
        messagebox.showinfo("Sucesso", txt)

    def show_error(self, err):
        messagebox.showerror("Erro", err)
