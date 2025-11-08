from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database
from app.schemas import pedido as schemas
from app.crud import pedido as crud
from app.core.auth import get_current_user
from app.models.user import Usuario
from app.services import pagamento  # ✅ novo import

router = APIRouter()

@router.post("/pedidos", response_model=schemas.Pedido)
def criar_pedido(
    pedido: schemas.PedidoCreate,
    db: Session = Depends(database.get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crud.criar_pedido(db, usuario.id, pedido, usuario)


# ✅ Listar pedidos do usuário autenticado
@router.get("/pedidos", response_model=List[schemas.Pedido])
def listar_pedidos(
    db: Session = Depends(database.get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crud.listar_pedidos(db, usuario.id)

# ✅ Consultar status do pagamento Pix
@router.get("/pagamento/{pix_id}")
def verificar_status(pix_id: str):
    return pagamento.verificar_status(pix_id)
