from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ProdutoModel(settings.DBBaseModel):
    __tablename__ = 'produtos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    referencia: str = Column(String)
    quantidade_desejada: int = Column(Integer)
    orcamento_id: int = Column(Integer, ForeignKey('orcamentos.id'))
    respostas = relationship(
        'RespostaModel',
        cascade='all,delete-orphan',
        lazy='joined'
    )