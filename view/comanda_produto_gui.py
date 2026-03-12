import tkinter as tk
from tkinter import messagebox, ttk

class Comanda_produto_View:
    def __init__(self):
        self.controller = None
        self.root = tk.Toplevel()
        self.root.title("Gestão de Comandas (Mesas x Produtos)")
        self.root.geometry("700x550")

        self.root.protocol("WM_DELETE_WINDOW", self._ocultar_janela)
        
        self.var_m = tk.StringVar()
        self.var_p = tk.StringVar()
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="COMANDA PRODUTO", font=("Arial", 14, "bold"), pady=10).pack()
        

        frame = tk.LabelFrame(self.root, text=" Novo Vínculo ", padx=10, pady=10)
        frame.pack(fill="x", padx=20)

        tk.Label(frame, text="Mesas:").grid(row=0, column=0)
        self.cb_m = ttk.Combobox(frame, textvariable=self.var_m, width=30, state="readonly")
        self.cb_m.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Produtos:").grid(row=0, column=2)
        self.cb_p = ttk.Combobox(frame, textvariable=self.var_p, width=30, state="readonly")
        self.cb_p.grid(row=0, column=3, padx=5)


        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="SALVAR", bg="#d4edda", width=15, command=self._acao_vincular).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="EXCLUIR", bg="#f8d7da", width=15, command=self._acao_excluir).pack(side=tk.LEFT, padx=5)


        self.tree = ttk.Treeview(self.root, columns=("m_id", "p_id", "preco"), show="headings")
        self.tree.heading("m_id", text="ID Mesa")
        self.tree.heading("p_id", text="ID Produto")
        self.tree.heading("preco", text="Preço")
        
        self.tree.column("m_id", width=100)
        self.tree.column("p_id", width=100)
        self.tree.column("preco", width=100)
        
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        frame_vtotal = tk.LabelFrame(self.root, text=" Valor total ", padx=10, pady=10)
        frame_vtotal.pack(fill="x", padx=20)




    def _ocultar_janela(self):
        """Oculta a janela em vez de destruí-la para permitir reabertura."""
        self.root.grab_release() 
        self.root.withdraw()     

    def _acao_vincular(self):
        if self.controller:
            self.controller.add_comanda_produto()
            self.controller.list_comanda_produto()

    def _acao_excluir(self):
        if self.controller:
            if messagebox.askyesno("Confirmar", "Deseja excluir este vínculo?"):
                self.controller.delete_comanda_produto()
                self.controller.list_comanda_produto()

    # --- Métodos chamados pelo Controller ---
    def get_dados_comanda_produto(self):
        try:
            return {
                "mesas_id": int(self.var_m.get().split(" - ")[0]), 
                "produto_id": int(self.var_p.get().split(" - ")[0])
            }
        except Exception:
            self.show_error("Selecione uma Mesa e um Produto válidos!")
            return None

    def preencher_combo_mesas(self, mesas):
        self.cb_m['values'] = [f"{m._numero} - Capacidade {m._capacidade}" for m in mesas]

    def preencher_combo_produtos(self, produtos):
        self.cb_p['values'] = [f"{p._id} - {p._nome} - {p._categoria_id}" for p in produtos]

    def show_comanda_produto(self, lista):
        for i in self.tree.get_children(): 
            self.tree.delete(i)
            
        for item in lista:
            self.tree.insert("", "end", values=(
                item._mesas_id,
                item._produto_id,
                f"R$ {item._preco_unitario:.2f}"
            ))

    def run(self):
        # Garante que a janela reapareça caso tenha sido fechada no "X" antes
        self.root.deiconify() 
        
        if self.controller:
            self.controller.list_related_dados()
            self.controller.list_comanda_produto()
            
        self.root.grab_set()
        self.root.focus_force()

    def show_message(self, m): 
        messagebox.showinfo("Sucesso", m)
        
    def show_error(self, e): 
        messagebox.showerror("Erro", e)