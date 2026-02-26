class Produto_categoria:
    def __init__(self, id, id_produto, id_categoria, nome_produto="", nome_categoria=""):
        self._id = id
        self._id_produto = id_produto
        self._id_categoria = id_categoria
        self._nome_categoria = nome_categoria
        self._nome_produto = nome_produto

