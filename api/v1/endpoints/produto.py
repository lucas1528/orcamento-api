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
from models.usuario_model import UsuarioModel
from schemas.produto_schema import ProdutoSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST produto
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProdutoSchema)
async def post_produto(
    produto: ProdutoSchema,
    db: AsyncSession = Depends(get_session)):
    novo_produto = ProdutoModel(
        nome=produto.nome,
        referencia=produto.referencia,
        quantidade_desejada=produto.quantidade_desejada,
        orcamento_id=produto.orcamento_id
    )

    db.add(novo_produto)
    await db.commit()

    return novo_produto

# GET produtos
@router.get('/orc/{orcamento_id}', response_model=List[ProdutoSchema])
async def get_produtos(
    orcamento_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
    ):
    async with db as session:
        query = select(OrcamentoModel).filter(OrcamentoModel.id == orcamento_id)
        result = await session.execute(query)
        orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

        if orcamento and orcamento.usuario_id == usuario_logado.id:
            query = select(ProdutoModel).filter(ProdutoModel.orcamento_id == orcamento_id)
            result = await session.execute(query)
            produtos: List[ProdutoModel] = result.scalars().unique().all()

            return produtos
        else:
            raise HTTPException(
                detail='Produto não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )

# GET produto
@router.get('/{produto_id}', response_model=ProdutoSchema, status_code=status.HTTP_200_OK)
async def get_produto(
    produto_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)
    ):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto: ProdutoModel = result.unique().scalar_one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()

            if orcamento and orcamento.usuario_id == usuario_logado.id:
                return produto
        
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# PUT produto
@router.put('/{produto_id}', response_model=ProdutoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_produto(
    produto_id: int,
    produto: ProdutoSchema,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto_up = result.unique().scalar_one_or_none()

        if produto_up:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()
            
            if orcamento and orcamento.usuario_id == usuario_logado.id:
                if produto.nome:
                    produto_up.nome = produto.nome
                if produto.referencia:
                    produto_up.referencia = produto.referencia
                if produto.quantidade_desejada:
                    produto_up.quantidade_desejada = produto.quantidade_desejada
                if produto_up.orcamento_id != produto.orcamento_id:
                    produto_up.nome = produto.nome

                await session.commit()

                return produto_up
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# DELETE produto
@router.delete('/{produto_id}', response_model=ProdutoSchema)
async def delete_produto(
    produto_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ProdutoModel).filter(ProdutoModel.id == produto_id)
        result = await session.execute(query)
        produto = result.unique().scalar_one_or_none()

        if produto:
            query = select(OrcamentoModel).filter(OrcamentoModel.id == produto.orcamento_id)
            result = await session.execute(query)
            orcamento: OrcamentoModel = result.scalars().unique().one_or_none()
            
            if orcamento and orcamento.usuario_id == usuario_logado.id:
                await session.delete(produto)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)
                
        raise HTTPException(
            detail='Produto não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )