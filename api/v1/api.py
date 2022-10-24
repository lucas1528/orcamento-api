from fastapi import APIRouter

from api.v1.endpoints import orcamento
from api.v1.endpoints import fornecedor
from api.v1.endpoints import produto
from api.v1.endpoints import resposta
from api.v1.endpoints import usuario



api_router = APIRouter()
api_router.include_router(orcamento.router, prefix='/orcamentos', tags=['orcamentos'])
api_router.include_router(fornecedor.router, prefix='/fornecedores', tags=['fornecedores'])
api_router.include_router(produto.router, prefix='/produtos', tags=['produtos'])
api_router.include_router(resposta.router, prefix='/respostas', tags=['respostas'])
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])


# /api/v1/orcamentos
# /api/v1/fornecedores
# /api/v1/produtos
# /api/v1/respostas
# /api/v1/usuarios