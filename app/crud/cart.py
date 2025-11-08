from sqlalchemy.orm import Session
from app.models import cart as models_cart, livro as models_livro, user as models_user
from app.schemas import cart as schemas_cart
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from app.models.cart import ItemCarrinho, Carrinho


# --------------------------------------
# Criar um carrinho para um novo usuário
# --------------------------------------
def criar_carrinho_para_usuario(db: Session, usuario_id: int):
    carrinho = models_cart.Carrinho(usuario_id=usuario_id)
    db.add(carrinho)
    db.commit()
    db.refresh(carrinho)
    return carrinho


# ------------------------------
# Obter o carrinho de um usuário
# ------------------------------
def obter_carrinho_por_usuario(db: Session, usuario_id: int):
    return db.query(models_cart.Carrinho).filter_by(usuario_id=usuario_id).first()


# ------------------------------
# Adicionar um item ao carrinho
# ------------------------------
def adicionar_item(db: Session, usuario_id: int, item: schemas_cart.ItemCarrinhoCreate):
    carrinho = obter_carrinho_por_usuario(db, usuario_id)
    
    if not carrinho:
        carrinho = criar_carrinho_para_usuario(db, usuario_id)

    # Verifica se o item já está no carrinho
    item_existente = (
        db.query(models_cart.ItemCarrinho)
        .filter_by(carrinho_id=carrinho.id, livro_id=item.livro_id)
        .first()
    )

    if item_existente:
        item_existente.quantidade += item.quantidade
    else:
        novo_item = models_cart.ItemCarrinho(
            carrinho_id=carrinho.id,
            livro_id=item.livro_id,
            quantidade=item.quantidade,
        )
        db.add(novo_item)

    db.commit()
    db.refresh(carrinho)
    return carrinho


# ------------------------------
# Listar os itens do carrinho
# ------------------------------
from sqlalchemy.orm import joinedload

def listar_itens(db: Session, usuario_id: int):
    carrinho = obter_carrinho_por_usuario(db, usuario_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    itens = (
        db.query(models_cart.ItemCarrinho)
        .options(joinedload(models_cart.ItemCarrinho.livro))  # 👈 carrega livro junto
        .filter_by(carrinho_id=carrinho.id)
        .all()
    )
    return itens


# ------------------------------
# Remover um item do carrinho
# ------------------------------
def remover_item(db: Session, usuario_id: int, item_id: int):
    carrinho = obter_carrinho_por_usuario(db, usuario_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    item = (
        db.query(models_cart.ItemCarrinho)
        .filter_by(carrinho_id=carrinho.id, id=item_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

    db.delete(item)
    db.commit()
    return {"mensagem": "Item removido com sucesso"}

def atualizar_quantidade(db: Session, usuario_id: int, item_id: int, nova_quantidade: int):
    item = (
        db.query(ItemCarrinho)
        .join(Carrinho)
        .filter(
            ItemCarrinho.id == item_id,
            Carrinho.usuario_id == usuario_id
        )
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho.")

    item.quantidade = nova_quantidade
    db.commit()
    db.refresh(item)
    return item