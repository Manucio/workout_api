from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/atletas", tags=["Atletas"])

@router.get("", response_model=Page[schemas.AtletaListOut])
def listar_atletas(
    nome: Optional[str] = Query(None, description="Filtra por nome (contém)"),
    cpf: Optional[str] = Query(None, description="Filtra por CPF exato"),
    db: Session = Depends(get_db)
):
    consulta = db.query(models.Atleta).join(models.Atleta.centro_treinamento).join(models.Atleta.categoria)
    if nome:
        consulta = consulta.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        consulta = consulta.filter(models.Atleta.cpf == cpf)
    return paginate(consulta)

@router.post("", response_model=schemas.AtletaListOut, status_code=status.HTTP_201_CREATED)
def criar_atleta(dados: schemas.AtletaCreate, db: Session = Depends(get_db)):
    obj = models.Atleta(**dados.dict())
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {dados.cpf}"
        )

