from core.configs import settings

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class RespostaModel(settings.DBBaseModel):
    __tablename__ = 'respostas'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    valor: float = Column(Float)
    fornecedor_id: int = Column(Integer, ForeignKey('fornecedores.id'))
    produto_id: int = Column(Integer, ForeignKey('produtos.id'))

