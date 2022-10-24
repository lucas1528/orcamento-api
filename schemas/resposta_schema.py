from typing import Optional
from pydantic import BaseModel



class RespostaSchema(BaseModel):
    id: Optional[int] = None
    valor: float
    fornecedor_id: Optional[int]
    produto_id: Optional[int]

    class Config:
        orm_mode = True