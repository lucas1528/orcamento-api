from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.fornecedor_schema import FornecedorSchema

from schemas.orcamento_schema import OrcamentoSchema


class UsuarioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchema):
    senha: str

class UsuarioSchemaOrcamentos(UsuarioSchema):
    orcamentos: Optional[List[OrcamentoSchema]]
    fornecedores: Optional[List[FornecedorSchema]]

class UsuarioSchemaUp(UsuarioSchema):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]