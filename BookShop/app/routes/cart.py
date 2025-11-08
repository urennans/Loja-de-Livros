from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import database
from app.schemas import cart as schemas_cart
from app.crud import cart as crud_cart
from app.core.auth import get_current_user
from app.models.user import Usuario
from app.database import get_db






router = APIRouter()


# ------------------------------
# Adicionar item ao carrinho
# ------------------------------
@router.post("/carrinho/adicionar", response_model=schemas_cart.Carrinho)
def adicionar_item_ao_carrinho(
    item: schemas_cart.ItemCarrinhoCreate,
    db: Session = Depends(database.get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crud_cart.adicionar_item(db, usuario.id, item)


# ------------------------------
# Ver todos os itens do carrinho
# ------------------------------
@router.get("/carrinho/itens", response_model=List[schemas_cart.ItemCarrinho])
def listar_itens_do_carrinho(
    db: Session = Depends(database.get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crud_cart.listar_itens(db, usuario.id)


# ------------------------------
# Remover item do carrinho
# ------------------------------
@router.delete("/carrinho/{item_id}")
def remover_item_do_carrinho(
    item_id: int,
    db: Session = Depends(database.get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crud_cart.remover_item(db, usuario.id, item_id)


# ------------------------------
# Atualizar quantidade do item do carrinho
# ------------------------------

@router.patch("/carrinho/{item_id}", response_model=schemas_cart.ItemCarrinho)
def atualizar_quantidade(
    item_id: int,
    dados: schemas_cart.AtualizarQuantidade,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_cart.atualizar_quantidade(db, usuario.id, item_id, dados.quantidade)
