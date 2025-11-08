from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas import user as schemas_user
from app.crud import user as crud_user
from app import database
from app.models import user as models_user

# Chave secreta e configurações do token
SECRET_KEY = "chave_super_secreta_para_token_jwt"  # (dica: usar env em produção)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# URL padrão do token (OAuth2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ===============================
# GERAÇÃO DO TOKEN
# ===============================
def criar_token(dados: dict, expira_em: Optional[timedelta] = None):
    to_encode = dados.copy()

    if expira_em:
        expire = datetime.utcnow() + expira_em
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ===============================
# VERIFICAÇÃO DO TOKEN
# ===============================
def verificar_token(token: str, credenciais_excecao):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credenciais_excecao
        return schemas_user.TokenData(id=int(user_id))
    except JWTError:
        raise credenciais_excecao


# ===============================
# DEPENDÊNCIA DE AUTENTICAÇÃO
# ===============================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credenciais_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verificar_token(token, credenciais_excecao)

    usuario = crud_user.buscar_usuario_por_id(db, user_id=token_data.id)

    if usuario is None:
        raise credenciais_excecao

    return usuario



def verificar_admin(usuario: models_user.Usuario = Depends(get_current_user)):
    if not usuario.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem acessar esta funcionalidade"
        )
    return usuario
