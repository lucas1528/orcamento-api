from pydantic import BaseModel
from typing import List, Optional

from schemas.produto_schema import ProdutoSchema



class OrcamentoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    inicio: str
    fim: str
    estado: str
    token: str
    usuario_id: Optional[int]

    class Config:
        orm_mode = True

class OrcamentoSchemaProdutos(OrcamentoSchema):
    produtos: Optional[List[ProdutoSchema]]