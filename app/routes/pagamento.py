from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.services.pagamento import gerar_pix, verificar_status
from app import database
from app.crud import pedido as crud


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PixRequest(BaseModel):
    valor: float
    descricao: str
    email: EmailStr

@router.post("/pagamento/pix")
async def criar_pagamento_pix(pix_request: PixRequest, token: str = Depends(oauth2_scheme)):
    print(f"Valor recebido para pagamento PIX: {pix_request.valor}")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    resposta = gerar_pix(
        valor=pix_request.valor,
        descricao=pix_request.descricao,
        email=pix_request.email
    )

    if "id" not in resposta:
        print("Erro ao gerar Pix:", resposta)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao gerar pagamento PIX")

    return resposta

@router.post("/pagamento/webhook")
async def receber_webhook(request: Request, db: Session = Depends(database.get_db)):
    dados = await request.json()
    print("Webhook recebido:", dados)

    payment_id = dados.get("data", {}).get("id")
    if not payment_id:
        raise HTTPException(status_code=400, detail="ID do pagamento não informado")

    # Consulta o status real do pagamento
    pagamento_info = verificar_status(str(payment_id))
    status_pagamento = pagamento_info.get("status")  # Ex: 'approved', 'pending', etc.
    print("Status do pagamento:", status_pagamento)

    if not status_pagamento:
        raise HTTPException(status_code=400, detail="Status do pagamento não encontrado")

    # Atualiza o pedido no banco com esse status
    pedido = crud.atualizar_status_pagamento(db, pix_id=str(payment_id), novo_status=status_pagamento)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado para este pagamento")

    return {"status": "ok", "pedido_id": pedido.id}


@router.get("/pagamento/{pix_id}")
async def status_pagamento(pix_id: str, db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    pagamento_info = verificar_status(pix_id)
    status_pagamento = pagamento_info.get("status")

    if not status_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    if status_pagamento == "approved":
        crud.atualizar_status_pagamento(db, pix_id=pix_id, novo_status="pago")

    return {"status": status_pagamento}

