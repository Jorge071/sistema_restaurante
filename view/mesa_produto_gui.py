import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk

class Mesa_produto_View:
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
                
            self.root.title("Gestão de Comandas (Mesas x Produtos)")
            self.root.geometry("800x600")
        
        if not master and hasattr(self.root, "protocol"):
            self.root.protocol("WM_DELETE_WINDOW", self._ocultar_janela)
        
        self.var_m = ctk.StringVar(value="")
        self.produto_vars = {} 
        self._setup_ui()

    def _setup_ui(self):
        ctk.CTkLabel(self.root, text="LANÇAMENTO DE PRODUTOS", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        frame_mesa = ctk.CTkFrame(self.root)
        frame_mesa.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(frame_mesa, text="Mesa:").pack(side="left", padx=(10, 5), pady=10)
        self.cb_m = ctk.CTkComboBox(frame_mesa, variable=self.var_m, width=250, state="readonly")
        self.cb_m.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(frame_mesa, text="VER CONTA DA MESA", fg_color="#17a2b8", hover_color="#138496", command=self._acao_buscar_mesa).pack(side="left", padx=5)
        ctk.CTkButton(frame_mesa, text="VER TODAS", fg_color="#6c757d", hover_color="#5a6268", command=self._acao_ver_todas).pack(side="left", padx=5)
        
        ctk.CTkLabel(self.root, text="Selecione os Produtos", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=25, pady=(10,0))
        self.frame_produtos = ctk.CTkScrollableFrame(self.root, height=120)
        self.frame_produtos.pack(fill="x", padx=20, pady=5)

        frame_btn = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_btn.pack(pady=10)
        ctk.CTkButton(frame_btn, text="ADICIONAR SELECIONADOS", fg_color="#28a745", hover_color="#218838", width=200, command=self._acao_vincular).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_btn, text="EXCLUIR ITEM", fg_color="#dc3545", hover_color="#c82333", width=150, command=self._acao_excluir).pack(side=tk.LEFT, padx=5)

        # Estilização da Tabela
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=25, fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#343638')])

        frame_tabela = ctk.CTkFrame(self.root)
        frame_tabela.pack(expand=True, fill="both", padx=20, pady=5)

        self.tree = ttk.Treeview(frame_tabela, columns=("m_id", "p_id", "produto", "categoria", "preco"), show="headings")
        self.tree.heading("m_id", text="ID Mesa")
        self.tree.heading("p_id", text="ID Produto")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("preco", text="Preço")
        
        self.tree.column("m_id", width=60, anchor="center")
        self.tree.column("p_id", width=60, anchor="center")
        self.tree.column("produto", width=150, anchor="center")
        self.tree.column("categoria", width=100, anchor="center")
        self.tree.column("preco", width=80, anchor="center")
        self.tree.pack(expand=True, fill="both")

        frame_vtotal = ctk.CTkFrame(self.root)
        frame_vtotal.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_vtotal, text="Valor total da Comanda:", font=ctk.CTkFont(weight="bold")).pack(pady=(5,0))
        self.lbl_total = ctk.CTkLabel(frame_vtotal, text="R$ 0.00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#28a745")
        self.lbl_total.pack(pady=(0,5))

    def _ocultar_janela(self):
        if hasattr(self.root, "grab_release"): self.root.grab_release() 
        if hasattr(self.root, "withdraw"): self.root.withdraw()     

    def _acao_vincular(self):
        if self.controller: self.controller.add_mesa_produto()

    def _acao_excluir(self):
        if self.controller:
            selecionado = self.tree.selection()
            if not selecionado:
                self.show_error("Selecione um item na tabela para excluir.")
                return
            valores = self.tree.item(selecionado[0], 'values')
            if messagebox.askyesno("Confirmar", "Deseja excluir este produto da mesa?"):
                self.controller.delete_mesa_produto(valores[0], valores[1])

    def _acao_buscar_mesa(self):
        if self.controller:
            try:
                mesa_id = int(self.var_m.get().split(" - ")[0])
                self.controller.list_by_mesa(mesa_id)
            except Exception:
                self.show_error("Selecione uma mesa no campo ao lado para ver a conta!")

    def _acao_ver_todas(self):
        if self.controller: self.controller.list_mesa_produto()

    def get_dados_selecionados(self):
        try:
            mesa_id = int(self.var_m.get().split(" - ")[0])
            produtos_selecionados = []
            for p_id, dados_prod in self.produto_vars.items():
                if dados_prod['var'].get() == 1:
                    produtos_selecionados.append({"id": p_id, "valor": dados_prod['valor']})
            return mesa_id, produtos_selecionados
        except Exception:
            self.show_error("Selecione uma Mesa válida!")
            return None, []

    def preencher_combo_mesas(self, mesas):
        valores = [f"{m._id} - Mesa {m._numero} (Cap: {m._capacidade})" for m in mesas]
        self.cb_m.configure(values=valores)

    def preencher_checkbox_produtos(self, produtos):
        for widget in self.frame_produtos.winfo_children(): widget.destroy()
        self.produto_vars.clear()

        for p in produtos:
            var = tk.IntVar()
            texto = f"{p._nome} - R$ {p._valor:.2f}"
            chk = ctk.CTkCheckBox(self.frame_produtos, text=texto, variable=var)
            chk.pack(anchor="w", pady=2)
            self.produto_vars[p._id] = {'var': var, 'valor': p._valor}

    def show_mesa_produto(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        valor_total = 0.0
        for item in lista:
            self.tree.insert("", "end", values=(
                item._mesas_id, item._produto_id, item._produto_nome,
                item._categoria_nome, f"R$ {item._preco_unitario:.2f}"
            ))
            valor_total += float(item._preco_unitario)
            
        self.lbl_total.configure(text=f"R$ {valor_total:.2f}")
        for dados in self.produto_vars.values(): dados['var'].set(0)

    def show_message(self, m): messagebox.showinfo("Sucesso", m)
    def show_error(self, e): messagebox.showerror("Erro", e)
    
    def run(self):
        if hasattr(self.root, "focus_force"): self.root.focus_force()
        if type(self.root) == ctk.CTk: self.root.mainloop()

    def run(self):
        if self.controller:
            self.controller.list_related_dados()
            self.controller.list_mesa_produto()
            
        if hasattr(self.root, "focus_force"): 
            self.root.focus_force()
            
        if type(self.root) == ctk.CTk: 
            self.root.mainloop()