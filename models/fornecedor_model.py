from core.configs import settings

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class FornecedorModel(settings.DBBaseModel):
    __tablename__ = 'fornecedores'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String)
    email: str = Column(String)
    contato: str = Column(String)
    token: str = Column(String)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'))
    respostas = relationship(
        'RespostaModel',
        cascade='all,delete-orphan',
        lazy='joined'
    )