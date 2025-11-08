from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    endereco = Column(String)
    cidade = Column(String)
    cep = Column(String)
    metodo_pagamento = Column(String)
    total = Column(Float)
    criado_em = Column(DateTime, default=datetime.utcnow)

    # 🔽 Campos adicionados para integração com PIX
    status = Column(String, default="pendente")                   # Ex: pendente, pago, cancelado
    pix_id = Column(String, nullable=True)                        # ID de pagamento do Mercado Pago
    qr_code_base64 = Column(String, nullable=True)                # QR Code do Pix em imagem base64

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    livro_id = Column(Integer, ForeignKey("livros.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)

    pedido = relationship("Pedido", back_populates="itens")
    livro = relationship("livro")