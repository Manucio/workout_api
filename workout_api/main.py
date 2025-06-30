from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .endpoints.atleta_router import router as atleta_router

app = FastAPI(title="Workout API")

app.include_router(atleta_router)

# ativa paginação globalmente
add_pagination(app)
