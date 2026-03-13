import tkinter as tk
from tkinter import messagebox, ttk

class Comanda_produto_View:
    def __init__(self):
        self.controller = None
        self.root = tk.Toplevel()
        self.root.title("Gestão de Comandas (Mesas x Produtos)")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self._ocultar_janela)
        
        self.var_m = tk.StringVar()
        self.produto_vars = {} 
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="LANÇAMENTO DE PRODUTOS", font=("Arial", 14, "bold"), pady=10).pack()

        # Frame de Seleção de Mesa (Deixe apenas UMA vez)
        frame_mesa = tk.Frame(self.root)
        frame_mesa.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_mesa, text="Mesa:").pack(side="left")
        self.cb_m = ttk.Combobox(frame_mesa, textvariable=self.var_m, width=30, state="readonly")
        self.cb_m.pack(side="left", padx=10)

        # ADICIONE ESTES DOIS BOTÕES:
        tk.Button(frame_mesa, text="VER CONTA DA MESA", bg="#cce5ff", command=self._acao_buscar_mesa).pack(side="left", padx=5)
        tk.Button(frame_mesa, text="VER TODAS", bg="#e2e3e5", command=self._acao_ver_todas).pack(side="left")
        
        #Checkboxes para Produtos
        frame_prod_container = tk.LabelFrame(self.root, text=" Selecione os Produtos ", padx=10, pady=10)
        frame_prod_container.pack(fill="x", padx=20, pady=5)
        
        self.canvas = tk.Canvas(frame_prod_container, height=100)
        scrollbar = ttk.Scrollbar(frame_prod_container, orient="vertical", command=self.canvas.yview)
        self.frame_produtos = tk.Frame(self.canvas)

        self.frame_produtos.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.frame_produtos, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botões
        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)
        tk.Button(frame_btn, text="ADICIONAR SELECIONADOS", bg="#d4edda", width=25, command=self._acao_vincular).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="EXCLUIR ITEM", bg="#f8d7da", width=15, command=self._acao_excluir).pack(side=tk.LEFT, padx=5)

        # Tabela (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("m_id", "p_id", "produto", "categoria", "preco"), show="headings")
        self.tree.heading("m_id", text="ID Mesa")
        self.tree.heading("p_id", text="ID Produto")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("preco", text="Preço")
        
        self.tree.column("m_id", width=60)
        self.tree.column("p_id", width=60)
        self.tree.column("produto", width=150)
        self.tree.column("categoria", width=100)
        self.tree.column("preco", width=80)
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Frame Valor Total
        frame_vtotal = tk.LabelFrame(self.root, text=" Valor total da Comanda ", padx=10, pady=5)
        frame_vtotal.pack(fill="x", padx=20, pady=10)
        self.lbl_total = tk.Label(frame_vtotal, text="R$ 0.00", font=("Arial", 16, "bold"), fg="green")
        self.lbl_total.pack()

    def _ocultar_janela(self):
        self.root.grab_release() 
        self.root.withdraw()     

    def _acao_vincular(self):
        if self.controller:
            self.controller.add_comanda_produto()

    def _acao_excluir(self):
        if self.controller:
            selecionado = self.tree.selection()
            if not selecionado:
                self.show_error("Selecione um item na tabela para excluir.")
                return
            
            valores = self.tree.item(selecionado[0], 'values')
            if messagebox.askyesno("Confirmar", "Deseja excluir este produto da mesa?"):
                self.controller.delete_comanda_produto(valores[0], valores[1])


    def _acao_buscar_mesa(self):
        if self.controller:
            try:
                # Pega o ID da mesa que está selecionada no Combobox
                mesa_id = int(self.var_m.get().split(" - ")[0])
                # Manda o controller buscar só essa mesa
                self.controller.list_by_mesa(mesa_id)
            except Exception:
                self.show_error("Selecione uma mesa no campo ao lado para ver a conta!")

    def _acao_ver_todas(self):
        if self.controller:
            # Lista tudo novamente
            self.controller.list_comanda_produto()

    def get_dados_selecionados(self):
        try:
            mesa_id = int(self.var_m.get().split(" - ")[0])
            produtos_selecionados = []
            
            # Pega todos os checkboxes que estão marcados (valor 1)
            for p_id, dados_prod in self.produto_vars.items():
                if dados_prod['var'].get() == 1:
                    produtos_selecionados.append({
                        "id": p_id,
                        "valor": dados_prod['valor']
                    })
            return mesa_id, produtos_selecionados
        except Exception:
            self.show_error("Selecione uma Mesa válida!")
            return None, []

    def preencher_combo_mesas(self, mesas):
        self.cb_m['values'] = [f"{m._id} - Mesa {m._numero} (Cap: {m._capacidade})" for m in mesas]

    def preencher_checkbox_produtos(self, produtos):
        # Limpa checkboxes antigos
        for widget in self.frame_produtos.winfo_children():
            widget.destroy()
        self.produto_vars.clear()

        # Cria um checkbox para cada produto do banco
        for p in produtos:
            var = tk.IntVar()
            # Assumindo que seu objeto Produto tenha os atributos _id, _nome e _valor
            texto = f"{p._nome} - R$ {p._valor:.2f}"
            chk = tk.Checkbutton(self.frame_produtos, text=texto, variable=var)
            chk.pack(anchor="w")
            
            # Guarda a variável do checkbox e o valor atual do produto
            self.produto_vars[p._id] = {'var': var, 'valor': p._valor}

    def show_comanda_produto(self, lista):
        for i in self.tree.get_children(): 
            self.tree.delete(i)
            
        valor_total = 0.0
        for item in lista:
            self.tree.insert("", "end", values=(
                item._mesas_id,
                item._produto_id,
                item._produto_nome,
                item._categoria_nome,
                f"R$ {item._preco_unitario:.2f}"
            ))
            valor_total += float(item._preco_unitario)
            
        self.lbl_total.config(text=f"R$ {valor_total:.2f}")
        
        # Desmarca todos os checkboxes após salvar
        for dados in self.produto_vars.values():
            dados['var'].set(0)

    def show_message(self, m): messagebox.showinfo("Sucesso", m)
    def show_error(self, e): messagebox.showerror("Erro", e)
    
    def run(self):
        self.root.deiconify() 
        if self.controller:
            self.controller.list_related_dados()
            self.controller.list_comanda_produto()
        self.root.grab_set()
        self.root.focus_force()