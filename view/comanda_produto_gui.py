import tkinter as tk 
from tkinter import messagebox, ttk

class Comanda_produto_View:
    def __init__(self, master=None):
        self.controller = None
        if master:
            self.root = tk.Toplevel(master)
        else:
            self.root = tk.Tk()
            
        self.root.title("Cadastrinho de categoria")
        self.root.geometry("1280x720")

        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()