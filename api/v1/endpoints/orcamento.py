from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from models.orcamento_model import OrcamentoModel
from schemas.orcamento_schema import OrcamentoSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST orcamento
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrcamentoSchema)
async def post_orcamento(
    orcamento: OrcamentoSchema,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)):
    novo_orcamento: OrcamentoModel = OrcamentoModel(
        titulo=orcamento.titulo,
        inicio=orcamento.inicio,
        fim=orcamento.fim,
        estado=orcamento.estado,
        token=orcamento.token,
        usuario_id=usuario_logado.id
    )

    db.add(novo_orcamento)
    await db.commit()

    return novo_orcamento

# GET orcamentos
@router.get('/', response_model=List[OrcamentoSchema])
async def get_orcamentos(
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(OrcamentoModel).filter(OrcamentoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        orcamentos: List[OrcamentoModel] = result.scalars().unique().all()

        return orcamentos

# GET orcamento
@router.get('/{orcamento_id}', response_model=OrcamentoSchema, status_code=status.HTTP_200_OK)
async def get_orcamento(
    orcamento_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(OrcamentoModel).filter(OrcamentoModel.id == orcamento_id)
        result = await session.execute(query)
        orcamento: OrcamentoModel = result.unique().scalar_one_or_none()

        if orcamento and orcamento.usuario_id == usuario_logado.id:
            return orcamento
        else:
            raise HTTPException(
                detail='Orçamento não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )

# PUT orcamento
@router.put('/{orcamento_id}', response_model=OrcamentoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_orcamento(
    orcamento_id: int,
    orcamento: OrcamentoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(OrcamentoModel).filter(OrcamentoModel.id == orcamento_id)
        result = await session.execute(query)
        orcamento_up: OrcamentoModel = result.unique().scalar_one_or_none()

        if orcamento_up and orcamento_up.usuario_id == usuario_logado.id:
            if orcamento.titulo:
                orcamento_up.titulo = orcamento.titulo
            if orcamento.inicio:
                orcamento_up.inicio = orcamento.inicio
            if orcamento.fim:
                orcamento_up.fim = orcamento.fim
            if orcamento.estado:
                orcamento_up.estado = orcamento.estado
            if orcamento.token:
                orcamento_up.token = orcamento.token
            if usuario_logado.id != orcamento_up.usuario_id:
                orcamento_up.usuario_id = usuario_logado.id

            await session.commit()

            return orcamento_up
        else:
            raise HTTPException(
                detail='Orçamento não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )

# DELETE orcamento
@router.delete('/{orcamento_id}', response_model=OrcamentoSchema)
async def delete_orcamento(
    orcamento_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(OrcamentoModel).filter(OrcamentoModel.id == orcamento_id)
        result = await session.execute(query)
        orcamento: OrcamentoModel = result.unique().scalar_one_or_none()

        if orcamento and orcamento.usuario_id == usuario_logado.id:
            await session.delete(orcamento)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail='Orçamento não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )