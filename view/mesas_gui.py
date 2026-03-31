import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk

class Mesas_View:
    def __init__(self, master=None):
        self.controller = None
        
        if master:
            self.root = master
            for widget in self.root.winfo_children():
                widget.destroy()
        else:
            self.root = ctk.CTk()
            self.root.title("Cadastro de Mesas")
            self.root.geometry("800x500")

        self.var_id = ctk.StringVar(value="")
        self.var_numero = ctk.StringVar(value="")
        self.var_capacidade = ctk.StringVar(value="")
        self.var_status = ctk.StringVar(value="Livre")

        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self.root, text="CONTROLE DE MESAS", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        frame_form = ctk.CTkFrame(self.root)
        frame_form.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(frame_form, text="ID:").grid(row=0, column=0, sticky="e", padx=(10, 5), pady=10)
        ctk.CTkEntry(frame_form, textvariable=self.var_id, state="readonly", width=80).grid(row=0, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Número:").grid(row=0, column=2, sticky="e", padx=(20, 5), pady=10)
        ctk.CTkEntry(frame_form, textvariable=self.var_numero, width=150).grid(row=0, column=3, padx=5, pady=10)

        ctk.CTkLabel(frame_form, text="Capacidade:").grid(row=1, column=0, sticky="e", padx=(10, 5), pady=10)
        ctk.CTkEntry(frame_form, textvariable=self.var_capacidade, width=80).grid(row=1, column=1, padx=5, pady=10, sticky="w")

        ctk.CTkLabel(frame_form, text="Status:").grid(row=1, column=2, sticky="e", padx=(20, 5), pady=10)
        self.combo_status = ctk.CTkComboBox(frame_form, variable=self.var_status, values=["Livre", "Ocupado"], state="readonly", width=150)
        self.combo_status.grid(row=1, column=3, padx=5, pady=10)
        self.combo_status.set("Livre") 

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
        
        if type(self.root) == ctk.CTk:
            self.root.mainloop()

    def get_dados_mesas(self, mesas_existente=None):
        try:
            val_numero = self.var_numero.get()
            if not val_numero:
                self.show_error('O número da mesa é obrigatório')
                return None
            numero = int(val_numero)
            if numero <= 0:
                self.show_error("O número da mesa deve ser um valor positivo (maior que zero)!")
                return None
        except ValueError:
            self.show_error('Número inválido! Digite apenas números inteiros.')
            return None
        try:
            capacidade = int(self.var_capacidade.get()) if self.var_capacidade.get() else 0
            if capacidade < 1:
                self.show_error("A capacidade da mesa deve ser de pelo menos 1 pessoa!")
                return None
        except ValueError:
            self.show_error('Capacidade inválida')
            return None
        return {"numero": numero, "capacidade": capacidade, "status": self.var_status.get()}

        

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
        self.var_id.set("")
        self.var_numero.set("")
        self.var_capacidade.set("")
        self.var_status.set("Livre")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel[0])['values']
            self.var_id.set(v[0])
            self.var_numero.set(str(v[1]))
            self.var_capacidade.set(str(v[2]))
            self.var_status.set(str(v[3]))

    def show_mesas_details(self, mesas):
        if not mesas: return
        self.var_id.set(getattr(mesas, '_id', ''))
        self.var_numero.set(str(getattr(mesas, '_numero', '')))
        self.var_capacidade.set(str(getattr(mesas, '_capacidade', '')))
        self.var_status.set(getattr(mesas, '_status', ''))

    def show_message(self, txt): messagebox.showinfo("Sucesso", txt)
    def show_error(self, err): messagebox.showerror("Erro", err)