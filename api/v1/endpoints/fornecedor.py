from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.fornecedor_model import FornecedorModel
from models.usuario_model import UsuarioModel
from schemas.fornecedor_schema import FornecedorSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST fornecedor
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=FornecedorSchema)
async def post_fornecedor(
    fornecedor: FornecedorSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    novo_fornecedor: FornecedorModel = FornecedorModel(
        nome=fornecedor.nome,
        email=fornecedor.email,
        contato=fornecedor.contato,
        token=fornecedor.token,
        usuario_id=usuario_logado.id
    )

    db.add(novo_fornecedor)
    await db.commit()

    return novo_fornecedor

# GET fornecedores
@router.get('/', response_model=List[FornecedorSchema])
async def get_fornecedors(
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(FornecedorModel).filter(FornecedorModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        fornecedores: List[FornecedorModel] = result.scalars().unique().all()

        return fornecedores

# GET fornecedor
@router.get('/{fornecedor_id}', response_model=FornecedorSchema, status_code=status.HTTP_200_OK)
async def get_fornecedor(
    fornecedor_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(FornecedorModel).filter(FornecedorModel.id == fornecedor_id)
        result = await session.execute(query)
        fornecedor: FornecedorModel = result.unique().scalar_one_or_none()

        if fornecedor and fornecedor.usuario_id == usuario_logado.id:
            return fornecedor
        else:
            raise HTTPException(
                detail='Fornecedor não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )

# PUT fornecedor
@router.put('/{fornecedor_id}', response_model=FornecedorSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_fornecedor(
    fornecedor_id: int,
    fornecedor: FornecedorSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(FornecedorModel).filter(FornecedorModel.id == fornecedor_id)
        result = await session.execute(query)
        fornecedor_up: FornecedorModel = result.unique().scalar_one_or_none()

        if fornecedor_up and fornecedor_up.usuario_id == usuario_logado.id:
            if fornecedor.nome:
                fornecedor_up.nome = fornecedor.nome
            if fornecedor.email:
                fornecedor_up.email = fornecedor.email
            if fornecedor.contato:
                fornecedor_up.contato = fornecedor.contato
            if fornecedor.token:
                fornecedor_up.token = fornecedor.token
            if fornecedor_up.usuario_id != usuario_logado.id:
                fornecedor_up.usuario_id = usuario_logado.id

            await session.commit()

            return fornecedor_up
        else:
            raise HTTPException(
                detail='Fornecedor não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )

# DELETE fornecedor
@router.delete('/{fornecedor_id}', response_model=FornecedorSchema)
async def delete_fornecedor(
    fornecedor_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(FornecedorModel).filter(FornecedorModel.id == fornecedor_id)
        result = await session.execute(query)
        fornecedor: FornecedorModel = result.unique().scalar_one_or_none()

        if fornecedor and fornecedor.usuario_id == usuario_logado.id:
            await session.delete(fornecedor)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                detail='Fornecedor não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )