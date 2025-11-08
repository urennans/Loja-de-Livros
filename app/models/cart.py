from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    usuario = relationship("Usuario", back_populates="carrinho")
    itens = relationship("ItemCarrinho", back_populates="carrinho", cascade="all, delete-orphan")


class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"))
    livro_id = Column(Integer, ForeignKey("livros.id"))
    quantidade = Column(Integer, default=1)

    carrinho = relationship("Carrinho", back_populates="itens")
    livro = relationship("livro")