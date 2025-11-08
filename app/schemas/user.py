from pydantic import BaseModel, EmailStr
from typing import Optional

# =========================
# ENTRADA: Cadastro do usuário
# =========================
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str  # senha em texto plano na criação
    is_admin: Optional[bool] = False

# =========================
# SAÍDA: Dados públicos do usuário (sem senha)
# =========================
class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    is_admin: bool

    class Config:
        from_attributes = True  # para funcionar com ORM e Pydantic v2

# =========================
# ENTRADA: Login do usuário
# =========================
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

# =========================
# SAÍDA: Token JWT
# =========================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenComAdmin(BaseModel):
    access_token: str
    token_type: str = "bearer"
    is_admin: bool


class TokenData(BaseModel):
    id: Optional[int] = None
