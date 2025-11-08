from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    carrinho = relationship("Carrinho", back_populates="usuario",uselist=False)
    pedidos = relationship("Pedido", back_populates="usuario")
    avaliacoes = relationship("Avaliacao", back_populates="usuario", cascade="all, delete")
from app.models.pedido import Pedido