import tkinter as tk 
from tkinter import messagebox, ttk

class Mesas_view:
    def __init__(self, master=None):
        self.controller = None
        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()
            
        self.root.title("Cadastrinho de mesas")
        self.root.geometry("1280x720")

        self.var_id = tk.StringVar()
        self.var_numero = tk.StringVar()
        self.var_capacidade = tk.StringVar()
        self.var_status = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="CONTROLE DE MESAS", font=("Arial", 14, "bold"), pady=10).pack()
    
        frame_form = tk.LabelFrame(self.root, text=" Dados do mesas ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="ID: ").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg="#f0f0f0").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="NUMERO: ").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_numero, width=35).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="CAPACIDADE: ").grid(row=1, column=0, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_capacidade, width=15).grid(row=1, column=1, padx=5 ,pady=5)

        tk.Label(frame_form, text="STATUS: ").grid(row=1, column=2, sticky="e")
        tk.Entry(frame_form, textvariable=self.var_status, width=35).grid(row=1, column=3, padx=5, pady=5)



        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="SALVAR NOVO", command=self._acao_adicionar, 
                  bg="#d4edda", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="ATUALIZAR", command=self._acao_editar, 
                  bg="#fff3cd", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="EXCLUIR", command=self._acao_excluir, 
                  bg="#f8d7da", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos, bg="lightskyblue",
                  width=15).pack(side=tk.LEFT, padx=5)
        

        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both") 

        self.colunas = ("id", "nome", "cpf", "email", "renda")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="NOME")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("email", text="EMAIL")
        self.tree.heading("renda", text="RENDA")

        for col in self.colunas: self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        self.root.after(200, self._acao_listar)
        if not isinstance(self.root, tk.Toplevel):
            self.root.mainloop()

    def get_dados_cliente(self, produto_existente=None):
        try:
            renda_str = self.var_renda.get().replace("R$", "").replace(".", "").replace(",", ".").strip()
            return {
                "nome": self.var_nome.get(),
                "cpf": self.var_cpf.get(),
                "email": self.var_email.get(),
                "renda": float(renda_str) if renda_str else 0.0
            }
        except ValueError:
            self.show_error("Renda inválida! Use apenas números e ponto/vírgula.")
            return None
        
    def _acao_adicionar(self):
        self.controller.add_cliente()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: self.controller.list_clientes()

    def show_clientes(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in lista:
            self.tree.insert("", "end", values=(
                p._id, p._nome, p._cpf, p._email, f"R$ {p._renda:.2f}" 
            ))

    def _acao_editar(self):
        self.controller.update_cliente()
        self._acao_listar()

    def get_id(self, operacao=""):
        val = self.var_id.get()
        return int(val) if val else None
    
    def _acao_excluir(self):
        if messagebox.askyesno("Confirmação", "Deseja Excluir?"): 
            self.controller.delete_cliente()
            self._acao_listar()
            self.limpar_campos()

    def limpar_campos(self):
        for var in [self.var_id, self.var_nome, self.var_cpf, self.var_email, self.var_renda]: var.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])
            self.var_cpf.set(v[2])
            self.var_email.set(v[3])
            self.var_renda.set(str(v[4]).replace("R$ ", ""))

    def show_message(self, txt): messagebox.showinfo("Sucesso", txt)
    def show_error(self, err): messagebox.showerror("Erro", err)