from core.configs import settings

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(256), nullable=True)
    email: str = Column(String(256), index=True, nullable=False, unique=True)
    senha: str = Column(String(256), nullable=False)
    eh_admin: bool = Column(Boolean, default=False)
    orcamentos = relationship(
        'OrcamentoModel',
        cascade='all,delete-orphan',
        lazy='joined'
    )
    fornecedores = relationship(
        'FornecedorModel',
        cascade='all,delete-orphan',
        lazy='joined'
    )