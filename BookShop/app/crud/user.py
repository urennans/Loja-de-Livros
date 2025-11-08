from sqlalchemy.orm import Session
from app.models import user as models_user
from app.schemas import user as  schemas_user
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================
# Gerar hash da senha
# ============================
def get_password_hash(senha: str):
    return pwd_context.hash(senha)

# ============================
# Verifica senha (login)
# ============================
def verify_password(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)

# ============================
# Criar novo usuário
# ============================
def criar_usuario(db: Session, usuario: schemas_user.UsuarioCreate):
    senha_hash = get_password_hash(usuario.senha)
    db_usuario = models_user.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash,
        is_admin=getattr(usuario, "is_admin", False)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# ============================
# Buscar usuário por email
# ============================
def buscar_usuario_por_email(db: Session, email: str):
    return db.query(models_user.Usuario).filter(models_user.Usuario.email == email).first()

# ============================
# Buscar usuário por ID
# ============================
def buscar_usuario_por_id(db: Session, user_id: int):
    return db.query(models_user.Usuario).filter(models_user.Usuario.id == user_id).first()
