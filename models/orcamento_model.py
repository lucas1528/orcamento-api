from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class OrcamentoModel(settings.DBBaseModel):
    __tablename__ = 'orcamentos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    titulo: str = Column(String(100))
    inicio: str = Column(String)
    fim: str = Column(String)
    estado: str = Column(String)
    token: str = Column(String)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    produtos = relationship(
        'ProdutoModel',
        cascade='all,delete-orphan',
        lazy='joined'
    )