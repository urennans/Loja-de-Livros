# app/crud.py

from sqlalchemy.orm import Session
from app.models import livro as models_livro
from app.schemas import livro as schemas_livro 
from fastapi import HTTPException

def criar_livro(db: Session, livro):
    # Se for um schema Pydantic, converte com model_dump()
    if hasattr(livro, "model_dump"):
        livro_data = livro.model_dump()
    else:
        # Caso contrário, assume que é um dicionário comum
        livro_data = livro

    novo = models_livro.livro(**livro_data)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def listar_livros(db: Session):
    return db.query(models_livro.livro).all()

def buscar_livro(db: Session, livro_id: int):
    livro = db.query(models_livro.livro).filter(models_livro.livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    return livro

def atualizar_livro(db: Session, livro_id: int, dados: schemas_livro.livroCreate):
    livro = db.query(models_livro.livro).filter(models_livro.livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="livro não encontrado")

    livro.nome = dados.nome
    livro.marca = dados.marca
    livro.preco = dados.preco
    livro.estoque = dados.estoque
    livro.volume = dados.volume
    livro.descricao = dados.descricao
    livro.imagem_url = dados.imagem_url  


    db.commit()
    db.refresh(livro)
    return livro

def deletar_livro(db: Session, livro_id: int):
    livro = db.query(models_livro.livro).filter(models_livro.livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    db.delete(livro)
    db.commit()

def listar_destaques(db: Session, limite: int = 4):
    return db.query(models_livro.livro).limit(limite).all()
