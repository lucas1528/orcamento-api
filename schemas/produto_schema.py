from typing import List, Optional
from pydantic import BaseModel

from schemas.resposta_schema import RespostaSchema



class ProdutoSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    referencia: str
    quantidade_desejada: int
    orcamento_id: Optional[int]

    class Config:
        orm_mode = True

class ProdutoSchemaRespostas(ProdutoSchema):
    respostas: Optional[List[RespostaSchema]]
