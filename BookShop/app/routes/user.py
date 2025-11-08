from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import user as schemas_user
from app.crud import user as crud_user
from app.core import auth
from app import database

router = APIRouter()

# ============================
# DEPENDÊNCIA DO BANCO
# ============================
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# CADASTRAR USUÁRIO
# ============================
@router.post("/usuarios/", response_model=schemas_user.UsuarioOut)
def cadastrar_usuario(usuario: schemas_user.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = crud_user.buscar_usuario_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    novo_usuario = crud_user.criar_usuario(db, usuario)
    return novo_usuario


# ============================
# LOGIN
# ============================
@router.post("/login", response_model=schemas_user.TokenComAdmin)
def login_usuario(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_user.buscar_usuario_por_email(db, form_data.username)
    if not usuario or not crud_user.verify_password(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    token = auth.criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer","is_admin": usuario.is_admin }


# ============================
# PERFIL DO USUÁRIO AUTENTICADO
# ============================
@router.get("/perfil", response_model=schemas_user.UsuarioOut)
def perfil_usuario(usuario_atual = Depends(auth.get_current_user)):
    return usuario_atual
