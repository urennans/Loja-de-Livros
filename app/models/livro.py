from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy.orm import relationship  

class livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True ,autoincrement=True)
    nome = Column(String, index=True)
    marca = Column(String)
    preco = Column(Float)
    estoque = Column(Integer)
    volume = Column(String)
    descricao =  Column(String)
    imagem_url = Column(String, nullable=True) 
    avaliacoes = relationship("Avaliacao", back_populates="livro", cascade="all, delete")