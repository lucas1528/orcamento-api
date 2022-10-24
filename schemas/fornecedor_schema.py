from typing import Optional
from pydantic import BaseModel



class FornecedorSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    contato: str
    token: str
    usuario_id: Optional[int]

    class Config:
        orm_mode = True