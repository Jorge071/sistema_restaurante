import tkinter as tk
from tkinter import messagebox, ttk

class Comanda_produto_View:

    def __init__(self, master=None):
        self.controller = None

        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()

        self.root.title("Comanda - Produtos")
        self.root.geometry("800x600")

        self.var_mesa = tk.StringVar(self.root)
        self.var_produto = tk.StringVar(self.root)

        self._setup_ui()


    def _setup_ui(self):

        tk.Label(
            self.root,
            text="VINCULAR PRODUTOS À MESA",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        frame_form = tk.LabelFrame(self.root, text="Dados")
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="Mesa:").grid(row=0, column=0)
        self.combo_mesa = ttk.Combobox(
            frame_form,
            textvariable=self.var_mesa,
            state="readonly"
        )
        self.combo_mesa.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Produto:").grid(row=1, column=0)
        self.combo_produto = ttk.Combobox(
            frame_form,
            textvariable=self.var_produto,
            state="readonly"
        )
        self.combo_produto.grid(row=1, column=1, padx=5, pady=5)

        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)

        tk.Button(
            frame_btn,
            text="VINCULAR",
            bg="#d4edda",
            width=15,
            command=self._acao_adicionar
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_btn,
            text="ATUALIZAR",
            bg="#fff3cd",
            width=15,
            command=self._acao_editar
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_btn,
            text="EXCLUIR",
            bg="#f8d7da",
            width=15,
            command=self._acao_excluir
        ).pack(side=tk.LEFT, padx=5)

        frame_table = tk.Frame(self.root)
        frame_table.pack(expand=True, fill="both", padx=20, pady=10)

        self.tree = ttk.Treeview(
            frame_table,
            columns=("mesa", "produto"),
            show="headings"
        )

        self.tree.heading("mesa", text="Mesa")
        self.tree.heading("produto", text="Produto")

        self.tree.pack(expand=True, fill="both")

        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

   

    def run(self):
        if self.controller:
            self.controller.list_related_dados()

        if not isinstance(self.root, tk.Toplevel):
            self.root.mainloop()


    def get_dados_comanda_produto(self):
        try:
            mesa_id = int(self.var_mesa.get().split(" - ")[0])
            produto_id = int(self.var_produto.get().split(" - ")[0])

            return {
                "mesa_id": mesa_id,
                "produto_id": produto_id
            }

        except:
            self.show_error("Selecione mesa e produto!")
            return None



    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_comanda_produto()
            self._acao_listar()


    def _acao_editar(self):
        if self.controller:
            self.controller.update_comanda_produto()
            self._acao_listar()


    def _acao_excluir(self):
        if messagebox.askyesno("Confirmação", "Deseja excluir?"):
            if self.controller:
                self.controller.delete_comanda_produto()
                self._acao_listar()


    def _acao_listar(self):
        if self.controller:
            self.controller.list_comanda_produto()



  

    def preencher_combo_produtos(self, lista_produtos):
        self.combo_produto["values"] = [
            f"{p._id} - {p._nome}" for p in lista_produtos
        ]


    def preencher_combo_mesas(self, lista_mesas):
        self.combo_mesa["values"] = [
            f"{m._id} - Mesa {m._numero}" for m in lista_mesas
        ]





    def show_comanda_produto(self, lista):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in lista:
            mesa_val = getattr(item, '_mesa_id', getattr(item, 'mesa_id', ''))
            produto_val = getattr(item, '_produto_id', getattr(item, 'produto_id', ''))

            self.tree.insert("", "end", values=(
                mesa_val,
                produto_val
            ))


    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()

        if item_sel:
            v = self.tree.item(item_sel[0])["values"]

            if v:
                self.var_mesa.set(str(v[0]))
                self.var_produto.set(str(v[1]))


  

    def show_message(self, txt):
        messagebox.showinfo("Sucesso", txt)

    def show_error(self, txt):
        messagebox.showerror("Erro", txt)