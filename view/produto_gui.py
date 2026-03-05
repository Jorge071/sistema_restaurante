import tkinter as tk
from tkinter import messagebox, ttk

class Produto_View:

    def __init__(self, master=None):
        self.controller = None

        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()

        self.root.title("Gestão de Produtos")
        self.root.geometry("800x600")

        self.var_id = tk.StringVar(self.root)
        self.var_nome = tk.StringVar(self.root)
        self.var_categoria_str = tk.StringVar(self.root)
        self.var_valor = tk.StringVar(self.root)

        self._setup_ui()


    def _setup_ui(self):

        tk.Label(self.root,text="CONTROLE DE PRODUTOS",font=("Arial", 16, "bold")).pack(pady=10)

        frame_form = tk.LabelFrame(self.root, text="Adicionar Produtos")
        frame_form.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0)
        tk.Entry(frame_form,textvariable=self.var_id,state="readonly").grid(row=0, column=1)

        tk.Label(frame_form, text="  Nome:").grid(row=0, column=3)
        tk.Entry(frame_form,textvariable=self.var_nome).grid(row=0, column=4)

        tk.Label(frame_form, text="  Categoria:").grid(row=0, column=6)

        tk.Label(frame_form, text="  Valor:").grid(row=0, column=10)
        tk.Entry(frame_form, textvariable=self.var_valor).grid(row=0, column=11)

        self.combo_categorias = ttk.Combobox(frame_form,textvariable=self.var_categoria_str,state="readonly")

        self.combo_categorias.grid(row=0, column=7, columnspan=2)



        frame_btn = tk.Frame(self.root)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn,text="SALVAR NOVO",bg="#d4edda",
                  command=self._acao_adicionar,width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_btn,text="ATUALIZAR",bg="#fff3cd",
                  command=self._acao_editar,width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_btn,text="EXCLUIR",bg="#f8d7da",
            command=self._acao_excluir,width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_btn, text="LIMPAR", 
                  command=self.limpar_campos, bg="lightskyblue", width=15).pack(side=tk.LEFT, padx=5)


        frame_table = tk.Frame(self.root)
        frame_table.pack(expand=True, fill="both", padx=20)

        self.tree = ttk.Treeview(frame_table,columns=("id", "nome", "categoria", "valor"),show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("valor", text="Valor")

        self.tree.pack(expand=True, fill="both")

        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)




    def run(self):
        if self.controller:
            self.controller.list_produto()

        if not isinstance(self.root, tk.Toplevel):
            self.root.mainloop()


    
  

    def get_dados_produto(self, obj=None):
        try:
            cat_id = int(self.var_categoria_str.get().split(" - ")[0])

            return {
                "nome": self.var_nome.get(),
                "categoria_id": cat_id,
                "valor": self.var_valor.get()
                
            }

        except:
            self.show_error("Selecione uma categoria!")
            return None

    def _acao_adicionar(self):
        if self.controller:
            self.controller.add_produto()
            self.limpar_campos()


    def _acao_editar(self):
        if self.controller:
            self.controller.update_produto()
            self.limpar_campos()


    def _acao_excluir(self):
        if messagebox.askyesno("Confirmar", "Deseja excluir?"):
            if self.controller:
                self.controller.delete_produto()
                self.limpar_campos()


    def show_produto(self, lista):

        for i in self.tree.get_children():
            self.tree.delete(i)

        for p in lista:
            cat_display = getattr(p, "nome_categoria", "Sem categoria")
            categoria_combo_display = f"{getattr(p, '_categoria_id', '')} - {cat_display}"

            self.tree.insert("", "end", values=(
                getattr(p, '_id', ''),
                getattr(p, '_nome', ''),
                categoria_combo_display,
                getattr(p, '_valor', '')
                
            ))


    def preencher_combo_categorias(self, lista):

        self.combo_categorias["values"] = [
            f"{c._id} - {c._nome}" for c in lista
        ]


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

    def show_message(self, txt):
        messagebox.showinfo("Sucesso", txt)
    
    def show_error(self, txt):
        messagebox.showerror("Erro", txt)

    def show_produto_details(self, produto):
        if not produto:
            return
        self.var_id.set(getattr(produto, '_id', ''))
        self.var_nome.set(getattr(produto, '_nome', ''))
        self.var_valor.set(getattr(produto, '_valor', ''))