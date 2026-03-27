import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk

class Produto_View:
    def __init__(self, master=None):
        self.controller = None

        if master:
            self.root = master
            for widget in self.root.winfo_children():
                widget.destroy()
        else:
            if tk._default_root is None:
                self.root = ctk.CTk()
            else:
                self.root = ctk.CTkToplevel()
            self.root.title("Gestão de Produtos")
            self.root.geometry("800x600")

        self.var_id = ctk.StringVar(value="")
        self.var_nome = ctk.StringVar(value="")
        self.var_categoria_str = ctk.StringVar(value="")
        self.var_valor = ctk.StringVar(value="")

        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self.root, text="CONTROLE DE PRODUTOS", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        frame_form = ctk.CTkFrame(self.root)
        frame_form.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_form, text="Adicionar Produtos", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, pady=(10, 5), sticky="w", padx=10)

        ctk.CTkLabel(frame_form, text="ID:").grid(row=1, column=0, padx=(10, 5), pady=10, sticky="e")
        ctk.CTkEntry(frame_form, textvariable=self.var_id, state="readonly", width=80).grid(row=1, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Nome:").grid(row=1, column=2, padx=(15, 5), pady=10, sticky="e")
        ctk.CTkEntry(frame_form, textvariable=self.var_nome, width=200).grid(row=1, column=3, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Categoria:").grid(row=2, column=0, padx=(10, 5), pady=10, sticky="e")
        self.combo_categorias = ctk.CTkComboBox(frame_form, variable=self.var_categoria_str, state="readonly", width=180)
        self.combo_categorias.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Valor (R$):").grid(row=2, column=2, padx=(15, 5), pady=10, sticky="e")
        ctk.CTkEntry(frame_form, textvariable=self.var_valor, width=120).grid(row=2, column=3, padx=5, pady=10, sticky="w")

        frame_btn = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_btn.pack(pady=10)

        ctk.CTkButton(frame_btn, text="SALVAR NOVO", fg_color="#28a745", hover_color="#218838", width=120, command=self._acao_adicionar).pack(side="left", padx=5)
        ctk.CTkButton(frame_btn, text="ATUALIZAR", fg_color="#ffc107", text_color="black", hover_color="#e0a800", width=120, command=self._acao_editar).pack(side="left", padx=5)
        ctk.CTkButton(frame_btn, text="EXCLUIR", fg_color="#dc3545", hover_color="#c82333", width=120, command=self._acao_excluir).pack(side="left", padx=5)
        ctk.CTkButton(frame_btn, text="LIMPAR", fg_color="#17a2b8", hover_color="#138496", width=120, command=self.limpar_campos).pack(side="left", padx=5)

        frame_table = ctk.CTkFrame(self.root)
        frame_table.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#343638')])

        self.tree = ttk.Treeview(frame_table, columns=("id", "nome", "categoria", "valor"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("valor", text="Valor")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=200, anchor="center")
        self.tree.column("categoria", width=150, anchor="center")
        self.tree.column("valor", width=100, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        if type(self.root) == ctk.CTk: self.root.mainloop()

    def get_dados_produto(self, obj=None):
        try:
            cat_id = int(self.var_categoria_str.get().split(" - ")[0])
            return {"nome": self.var_nome.get(), "categoria_id": cat_id, "valor": self.var_valor.get()}
        except:
            self.show_error("Selecione uma categoria!")
            return None

    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_produto()
            self.limpar_campos()
            self.controller.list_produto()

    def _acao_editar(self):
        if self.controller:
            self.controller.update_produto()
            self.limpar_campos()
            self.controller.list_produto()

    def _acao_excluir(self):
        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            if self.controller:
                self.controller.delete_produto()
                self.limpar_campos()
                self.controller.list_produto()

    def show_produto(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in lista:
            cat_display = getattr(p, "nome_categoria", "Sem categoria")
            categoria_combo_display = f"{getattr(p, '_categoria_id', '')} - {cat_display}"
            self.tree.insert("", "end", values=(getattr(p, '_id', ''), getattr(p, '_nome', ''), categoria_combo_display, getattr(p, '_valor', '')))

    def preencher_combo_categorias(self, lista):
        valores = [f"{c._id} - {c._nome}" for c in lista]
        self.combo_categorias.configure(values=valores)

    def _ao_selecionar_tabela(self, event):
        item = self.tree.selection()
        if item:
            v = self.tree.item(item[0])["values"]
            if v:
                self.var_id.set(v[0])
                self.var_nome.set(v[1])
                self.var_categoria_str.set(v[2])
                self.var_valor.set(str(v[3]).replace("R$ ", ""))

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None

    def limpar_campos(self):
        for var in [self.var_id, self.var_nome, self.var_categoria_str, self.var_valor]: var.set("")

    def show_message(self, txt): messagebox.showinfo("Sucesso", txt)
    def show_error(self, txt): messagebox.showerror("Erro", txt)

    def show_produto_details(self, produto):
        if not produto: return
        self.var_id.set(getattr(produto, '_id', ''))
        self.var_nome.set(getattr(produto, '_nome', ''))
        self.var_valor.set(getattr(produto, '_valor', ''))