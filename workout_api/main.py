from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.endpoints.atleta_router import router as atleta_router
from workout_api import database, models

app = FastAPI(title="Workout API")

# Cria tabelas (se não existirem)
models.Base.metadata.create_all(bind=database.engine)

# Inclui routers
app.include_router(atleta_router)

# Ativa paginação
add_pagination(app)
