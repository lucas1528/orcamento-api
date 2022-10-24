from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(title='Orcamentos API - FastAPI')
app.include_router(api_router, prefix=settings.API_V1_STR)

# /api/v1/orcamentos


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        log_level='info',
        reload=True
    )