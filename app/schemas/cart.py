from pydantic import BaseModel
from typing import Optional
from app.schemas.livro import livroOut

class ItemCarrinhoBase(BaseModel):
    livro_id: int
    quantidade: int

class ItemCarrinhoCreate(ItemCarrinhoBase):
    pass

class ItemCarrinho(ItemCarrinhoBase):
    id: int
    livro: livroOut  

    class Config:
        from_attributes = True

class Carrinho(BaseModel):
    id: int
    usuario_id: int
    itens: list[ItemCarrinho]

    class Config:
        from_attributes = True

class livroOut(BaseModel):
    id: int
    nome: str
    preco: float
    imagem_url: str

    class Config:
        from_attributes = True


class AtualizarQuantidade(BaseModel):
    quantidade: int