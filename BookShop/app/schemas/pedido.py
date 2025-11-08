from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.livro import livro  
from app.schemas.user import UsuarioOut

class ItemPedidoBase(BaseModel):
    livro_id: int
    quantidade: int
    preco_unitario: float

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedido(ItemPedidoBase):
    id: int
    livro: livro 

    class Config:
        from_attributes = True

class PedidoBase(BaseModel):
    endereco: str
    cidade: str
    cep: str
    metodo_pagamento: str
    total: float

class PedidoCreate(PedidoBase):
    itens: List[ItemPedidoCreate]
    email: EmailStr  

class Pedido(PedidoBase):
    id: int
    criado_em: datetime
    status: str  
    pix_id: Optional[str] = None  
    qr_code_base64: Optional[str] = None  
    itens: List[ItemPedido]
    usuario: Optional[UsuarioOut] = None 
    class Config:
        from_attributes = True
