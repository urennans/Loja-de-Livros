from sqlalchemy.orm import Session
from app.models.avaliacao import Avaliacao
from app.schemas.avaliacao import AvaliacaoCreate
from sqlalchemy import func

def criar_avaliacao(db: Session, usuario_id: int, avaliacao: AvaliacaoCreate):
    nova = Avaliacao(
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        livro_id=avaliacao.livro_id,
        usuario_id=usuario_id
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_avaliacoes_por_livro(db: Session, livro_id: int):
    return db.query(Avaliacao).filter(Avaliacao.livro_id == livro_id).all()

def listar_avaliacoes_por_usuario(db: Session, usuario_id: int):
    return db.query(Avaliacao).filter(Avaliacao.usuario_id == usuario_id).all()

def media_avaliacao_por_livro(db: Session, livro_id: int):
    media = db.query(func.avg(Avaliacao.nota))\
              .filter(Avaliacao.livro_id == livro_id)\
              .scalar()
    return round(media or 0, 2)
