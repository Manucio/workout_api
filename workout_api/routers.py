from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.get("", response_model=Page[schemas.AtletaListOut])
def listar_atletas(
    nome: Optional[str] = Query(None, description="Buscar por nome"),
    cpf: Optional[str] = Query(None, description="Buscar por CPF exato"),
    db: Session = Depends(get_db)
):
    base = db.query(models.Atleta).join(models.Atleta.centro_treinamento).join(models.Atleta.categoria)
    if nome:
        base = base.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        base = base.filter(models.Atleta.cpf == cpf)
    return paginate(base)

@router.post("", response_model=schemas.AtletaListOut, status_code=status.HTTP_201_CREATED)
def cadastrar_atleta(dados: schemas.AtletaCreate, db: Session = Depends(get_db)):
    novo = models.Atleta(**dados.dict())
    try:
        db.add(novo)
        db.commit()
        db.refresh(novo)
        return novo
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {dados.cpf}"
        )
