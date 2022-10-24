from os import access
from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaOrcamentos
from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get('/logado', response_model=UsuarioSchema)
def get_logado(
    usuario_logado: UsuarioModel = Depends(get_current_user)
    ):
    return usuario_logado

# POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)
async def post_usuario(
    usuario: UsuarioSchemaCreate,
    db: AsyncSession = Depends(get_session)
    ):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin
    )
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail='Já existe um usuário com este email cadastrado.'
            )

#GET Usuarios
@router.get('/', response_model=List[UsuarioSchema])
async def get_usuarios(
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
    ):
    if usuario_logado.eh_admin:
        async with db as session:
            query = select(UsuarioModel)
            result = await session.execute(query)
            usuarios: List[UsuarioSchema] = result.scalars().unique().all()

            return usuarios

    raise HTTPException(
        detail='Acesso negado.',
        status_code=status.HTTP_401_UNAUTHORIZED
    )

# GET Usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaOrcamentos, status_code=status.HTTP_200_OK)
async def get_usuario(
    usuario_id: int,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
    ):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario = result.scalars().unique().one_or_none()

        if usuario and usuario_logado.eh_admin:
            return usuario
        elif usuario and usuario.id == usuario_logado.id:
            return usuario
        
        raise HTTPException(
            detail='Usuario não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchemaUp,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
    ):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario_up and usuario_logado.eh_admin:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            
            await session.commit()

            return usuario_up

        elif usuario_up and usuario_up.id == usuario_logado.id:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            
            await session.commit()

            return usuario_up
        
        raise HTTPException(
            detail='Usuario não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )

# DELETE Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    usuario_logado: UsuarioModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario and usuario_logado.eh_admin:
            await session.delete(usuario)
            await session.commit()

            return Response(
                status_code=status.HTTP_204_NO_CONTENT,
            )
        
        raise HTTPException(
            detail='Usuario não encontrado.',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
# POST Login
@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
    ):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(
            detail='Dados de acesso incorretos.',
            status_code=status.HTTP_400_BAD_REQUEST
            )
    
    return JSONResponse(
        content={
            'access_token': criar_token_acesso(sub=usuario.id),
            'token_type': 'bearer'
        },
        status_code=status.HTTP_200_OK
    )