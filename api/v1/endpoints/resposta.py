from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.orcamento_model import OrcamentoModel
from models.produto_model import ProdutoModel

from models.resposta_model import RespostaModel
from models.usuario_model import UsuarioModel
from schemas.resposta_schema import RespostaSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST resposta
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=RespostaSchema)
async def post_resposta(
    resposta: RespostaSchema,
    db: AsyncSession = Depends(get_session)):
    novo_resposta = RespostaModel(
        valor=resposta.valor,
        fornecedor_id=resposta.fornecedor_id,
    )

    db.add(novo_resposta)
    await db.commit()

    return novo_resposta

# GET respostas
@router.get('/', response_model=List[RespostaSchema])
async def get_respostas(
    produto_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().unique().one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

            if orcamento and orcamento.usuario_id == usuario_logado.id:
                query = select(RespostaModel).filter(RespostaModel.produto_id == produto_id)
                result = await session.execute(query)
                respostas: List[RespostaModel] = result.scalars().unique().all()

                return respostas

        raise HTTPException(
            detail='Resposta não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# GET resposta
@router.get('/{resposta_id}', response_model=RespostaSchema, status_code=status.HTTP_200_OK)
async def get_resposta(
    resposta_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(RespostaModel).filter(RespostaModel.id == resposta_id)
        result = await session.execute(query)
        resposta: RespostaModel = result.unique().scalar_one_or_none()

        query = select(ProdutoModel).filter(ProdutoModel.id == resposta.produto_id)
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().unique().one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

            if orcamento and orcamento.usuario_id == usuario_logado.id:
                return resposta

        raise HTTPException(
            detail='Resposta não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# PUT resposta
@router.put('/{resposta_id}', response_model=RespostaSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_resposta(
    resposta_id: int,
    resposta: RespostaSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(RespostaModel).filter(RespostaModel.id == resposta_id)
        result = await session.execute(query)
        resposta_up: RespostaModel = result.unique().scalar_one_or_none()

        query = select(ProdutoModel).filter(ProdutoModel.id == resposta_up.produto_id)
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().unique().one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

            if orcamento and orcamento.usuario_id == usuario_logado.id:
                if resposta.valor:
                    resposta_up.valor = resposta.valor
                if resposta.fornecedor_id:
                    resposta_up.fornecedor_id = resposta.fornecedor_id
                if resposta.produto_id:
                    resposta_up.produto_id = resposta.produto_id
                
                return resposta_up

        raise HTTPException(
            detail='Resposta não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# DELETE resposta
@router.delete('/{resposta_id}', response_model=RespostaSchema)
async def delete_resposta(
    resposta_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(RespostaModel).filter(RespostaModel.id == resposta_id)
        result = await session.execute(query)
        resposta: RespostaModel = result.unique().scalar_one_or_none()

        query = select(ProdutoModel).filter(ProdutoModel.id == resposta.produto_id)
        result = await session.execute(query)
        produto: ProdutoModel = result.scalars().unique().one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

            if orcamento and orcamento.usuario_id == usuario_logado.id:
                await session.delete(resposta)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)


        raise HTTPException(
            detail='Resposta não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )