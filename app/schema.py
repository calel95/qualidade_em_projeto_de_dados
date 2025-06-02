import pandera.pandas as pa
from pandera.typing import Series

class ProdutoSchema(pa.DataFrameModel):
    """
    Esquema para validação de dados de produtos com Pandera.

    Attributes:
        id_produto (Series[int]): Identificador único do produto.
        nome (Series[str]): Nome do produto.
        quantidade (Series[int]): Quantidade disponível em estoque.
        preco (Series[float]): Preço unitário do produto.
        categoria (Series[str]): Categoria à qual o produto pertence.
    """
    id_produto: Series[int]
    nome: Series[str]
    quantidade: Series[int]
    preco: Series[float]
    categoria: Series[str]
    
    class Config:
        coerce = True
        strict = True  # garante que o schema seja exatamente igual, nao aceita colunas a mais
