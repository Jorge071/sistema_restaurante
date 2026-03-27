import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk

class Categoria_View:
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
                
            self.root.title("Cadastro de Categoria")
            self.root.geometry("800x500")

        self.var_id = ctk.StringVar(value="")
        self.var_nome = ctk.StringVar(value="")

        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self.root, text="CONTROLE DE CATEGORIA", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        frame_form = ctk.CTkFrame(self.root)
        frame_form.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame_form, text="ID:").grid(row=0, column=0, sticky="e", padx=(10, 5), pady=10)
        ctk.CTkEntry(frame_form, textvariable=self.var_id, state="readonly", width=80).grid(row=0, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Nome:").grid(row=0, column=2, sticky="e", padx=(20, 5), pady=10)
        ctk.CTkEntry(frame_form, textvariable=self.var_nome, width=300).grid(row=0, column=3, padx=5, pady=10)

        frame_botoes = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_botoes.pack(pady=10)

        ctk.CTkButton(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, fg_color="#28a745", hover_color="#218838", width=120).pack(side="left", padx=5)
        ctk.CTkButton(frame_botoes, text="ATUALIZAR", command=self._acao_editar, fg_color="#ffc107", text_color="black", hover_color="#e0a800", width=120).pack(side="left", padx=5)
        ctk.CTkButton(frame_botoes, text="EXCLUIR", command=self._acao_excluir, fg_color="#dc3545", hover_color="#c82333", width=120).pack(side="left", padx=5)
        ctk.CTkButton(frame_botoes, text="LIMPAR", command=self.limpar_campos, fg_color="#17a2b8", hover_color="#138496", width=120).pack(side="left", padx=5)

        frame_tabela = ctk.CTkFrame(self.root)
        frame_tabela.pack(expand=True, fill="both", padx=20, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#343638')])

        self.colunas = ("id", "nome")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")

        for col in self.colunas:
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        if type(self.root) == ctk.CTk: 
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
            self.tree.insert("", "end", values=(getattr(p, '_id', ''), getattr(p, '_nome', '')))

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
        self.var_id.set("")
        self.var_nome.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel[0])['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])

    def show_message(self, txt): messagebox.showinfo("Sucesso", txt)
    def show_error(self, err): messagebox.showerror("Erro", err)

    def show_categoria_details(self, categoria):
        if not categoria: return
        self.var_id.set(getattr(categoria, '_id', ''))
        self.var_nome.set(getattr(categoria, '_nome', ''))

    def run(self):
        if self.controller:
            self.controller.list_categoria()
            
        if type(self.root) == ctk.CTk: 
            self.root.mainloop()