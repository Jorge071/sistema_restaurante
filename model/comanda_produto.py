class Comanda_Produto:
    def __init__(self, mesas_id, produto_id, preco_unitario, produto_nome="", categoria_nome=""):
        self._mesas_id = mesas_id 
        self._produto_id = produto_id
        self._preco_unitario = preco_unitario
        self._produto_nome = produto_nome
        self._categoria_nome = categoria_nome