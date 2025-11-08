from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database
from app.schemas.avaliacao import AvaliacaoCreate, Avaliacao
from app.crud import avaliacao as crud
from app.core.auth import get_current_user
from app.models.user import Usuario

router = APIRouter()

@router.post("/avaliacoes", response_model=Avaliacao)
def criar_avaliacao(avaliacao: AvaliacaoCreate, db: Session = Depends(database.get_db), usuario: Usuario = Depends(get_current_user)):
    return crud.criar_avaliacao(db, usuario.id, avaliacao)

@router.get("/avaliacoes/livro/{livro_id}", response_model=List[Avaliacao])
def listar_avaliacoes_livro(livro_id: int, db: Session = Depends(database.get_db)):
    return crud.listar_avaliacoes_por_livro(db, livro_id)

@router.get("/avaliacoes/usuario/{usuario_id}", response_model=List[Avaliacao])
def listar_avaliacoes_usuario(usuario_id: int, db: Session = Depends(database.get_db)):
    return crud.listar_avaliacoes_por_usuario(db, usuario_id)

@router.get("/avaliacoes/livro/{livro_id}/media")
def media_avaliacao(livro_id: int, db: Session = Depends(database.get_db)):
    return {"media": crud.media_avaliacao_por_livro(db, livro_id)}
