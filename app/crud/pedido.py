from sqlalchemy.orm import Session
from app import models, schemas
from app.services.pagamento import gerar_pix
from app.schemas.pedido import PedidoCreate
from app.models import pedido as models_pedido
from app.models.cart import Carrinho, ItemCarrinho
from sqlalchemy.orm import Session, joinedload
from app.models.pedido import Pedido, ItemPedido


def criar_pedido(db: Session, usuario_id: int, pedido: PedidoCreate, usuario):
    novo_pedido = models_pedido.Pedido( 
        usuario_id=usuario_id,
        endereco=pedido.endereco,
        cidade=pedido.cidade,
        cep=pedido.cep,
        metodo_pagamento=pedido.metodo_pagamento,
        total=pedido.total,
        status="pendente"
    )
    db.add(novo_pedido)
    db.flush() 

    for item in pedido.itens:
        item_db = models_pedido.ItemPedido(
            pedido_id=novo_pedido.id,
            livro_id=item.livro_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        )
        db.add(item_db)

    email_usuario = usuario.email

    resposta_pix = gerar_pix(valor=pedido.total, descricao="Compra livro Shop", email=email_usuario)

    novo_pedido.pix_id = resposta_pix.get("id")
    novo_pedido.qr_code_base64 = resposta_pix.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")
    
    db.commit()
    db.refresh(novo_pedido)

    carrinho = db.query(Carrinho).filter(Carrinho.usuario_id == usuario_id).first()
    if carrinho:
        db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho.id).delete()
        db.delete(carrinho)

    db.commit()

    return novo_pedido



def atualizar_status_pagamento(db: Session, pix_id: str, novo_status: str):
    pedido = db.query(models.Pedido).filter(models.Pedido.pix_id == pix_id).first()
    if pedido:
        pedido.status = novo_status
        db.commit()
    return pedido

def listar_todos_pedidos(db: Session):
    return db.query(Pedido)\
        .options(
            joinedload(Pedido.usuario),             
            joinedload(Pedido.itens).joinedload(ItemPedido.livro) 
        ).all()
