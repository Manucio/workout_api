from pydantic import BaseModel, Field
from typing import Optional

class AtletaCreate(BaseModel):
    nome: str = Field(..., example="João da Silva")
    cpf: str = Field(..., example="12345678900")
    centro_treinamento_id: int
    categoria_id: int

class AtletaListOut(BaseModel):
    nome: str
    centro_treinamento: str
    categoria: str

    class Config:
        orm_mode = True

