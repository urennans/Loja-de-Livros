from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core import auth
from app.schemas import livro as schemas_livro
from app.schemas import pedido as schemas
from app.crud import livro as crud_livro
from app.models import user as models_user
from app.models.user import Usuario
from app.database import get_db

router = APIRouter()

@router.get("/")
def root():
    return {"mensagem": "Bem-vindo à Loja de livros!"}

@router.post("/livros/", response_model=schemas_livro.livro)
def criar_livro(
    livro: schemas_livro.livroCreate, 
    db: Session = Depends(get_db), 
    admin: models_user.Usuario = Depends(auth.verificar_admin)
):
    return crud_livro.criar_livro(db, livro)

@router.get("/livros/", response_model=List[schemas_livro.livro])
def listar_livros(db: Session = Depends(get_db)):
    return crud_livro.listar_livros(db)

@router.get("/livros/destaques", response_model=List[schemas_livro.livro])
def get_livros_destaques(db: Session = Depends(get_db)):
    return crud_livro.listar_destaques(db)

@router.get("/livros/{livro_id}", response_model=schemas_livro.livro)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    return crud_livro.buscar_livro(db, livro_id)

@router.put("/livros/{livro_id}", response_model=schemas_livro.livro)
def atualizar_livro(
    livro_id: int, 
    dados: schemas_livro.livroCreate, 
    db: Session = Depends(get_db), 
    admin: models_user.Usuario = Depends(auth.verificar_admin)
):
    return crud_livro.atualizar_livro(db, livro_id, dados)

@router.delete("/livros/{livro_id}", status_code=204)
def deletar_livro(
    livro_id: int, 
    db: Session = Depends(get_db), 
    admin: models_user.Usuario = Depends(auth.verificar_admin)
):
    crud_livro.deletar_livro(db, livro_id)

@router.get("/admin/pedidos", response_model=List[schemas.Pedido])
def listar_pedidos_admin(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(auth.verificar_admin),
):
    from app.crud import pedido as crud_pedido  # importe local para não misturar imports
    return crud_pedido.listar_todos_pedidos(db)
