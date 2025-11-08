from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.schemas import livro as schemas_livro
from app.schemas import cart as schemas_cart
from app.schemas import pedido as schemas_pedido
from app.schemas import avaliacao as schemas_avaliacao
from app.crud import livro as crud_livro
from app.crud import cart as crud_cart
from app.crud import pedido as crud_pedido
from app.crud import avaliacao as crud_avaliacao
from app.core.auth import get_current_user
from app.models.user import Usuario

# Cria as tabelas do banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="livroShop API",
    description="API distribuída do sistema livroShop",
    version="1.0.0"
)

# Middleware para permitir requisições externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Livros ----------------
@app.get("/livros/", response_model=List[schemas_livro.livroOut])
def listar_livros_endpoint(db: Session = Depends(get_db)):
    return crud_livro.listar_livros(db)

@app.get("/livros/{livro_id}", response_model=schemas_livro.livroOut)
def buscar_livro_endpoint(livro_id: int, db: Session = Depends(get_db)):
    return crud_livro.buscar_livro(db, livro_id)

@app.post("/livros/", response_model=schemas_livro.livroOut)
def criar_livro_endpoint(
    livro: schemas_livro.livroCreate,
    db: Session = Depends(get_db)
):
    return crud_livro.criar_livro(db, livro)

# ---------------- Carrinho ----------------
@app.post("/carrinho/adicionar", response_model=schemas_cart.Carrinho)
def adicionar_item_carrinho_endpoint(
    item: schemas_cart.ItemCarrinhoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_cart.adicionar_item(db, usuario.id, item)

@app.get("/carrinho/itens", response_model=List[schemas_cart.ItemCarrinho])
def listar_itens_carrinho_endpoint(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_cart.listar_itens(db, usuario.id)

@app.delete("/carrinho/{item_id}")
def remover_item_carrinho_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_cart.remover_item(db, usuario.id, item_id)

@app.patch("/carrinho/{item_id}", response_model=schemas_cart.ItemCarrinho)
def atualizar_quantidade_carrinho_endpoint(
    item_id: int,
    dados: schemas_cart.AtualizarQuantidade,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_cart.atualizar_quantidade(db, usuario.id, item_id, dados.quantidade)

# ---------------- Pedidos ----------------
@app.post("/pedidos/", response_model=schemas_pedido.Pedido)
def criar_pedido_endpoint(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_pedido.criar_pedido(db, usuario.id)

@app.get("/pedidos/", response_model=List[schemas_pedido.Pedido])
def listar_pedidos_endpoint(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_pedido.listar_pedidos(db, usuario.id)

# ---------------- Avaliações ----------------
@app.post("/avaliacoes/", response_model=schemas_avaliacao.Avaliacao)
def avaliar_livro_endpoint(
    avaliacao: schemas_avaliacao.AvaliacaoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return crud_avaliacao.criar_avaliacao(db, usuario.id, avaliacao)

@app.get("/avaliacoes/{livro_id}", response_model=List[schemas_avaliacao.Avaliacao])
def listar_avaliacoes_livro_endpoint(livro_id: int, db: Session = Depends(get_db)):
    return crud_avaliacao.listar_avaliacoes_por_livro(db, livro_id)

# ---------------- Raiz ----------------
@app.get("/")
def root():
    return {"message": "🧴 livroShop API rodando!"}
