from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import schemas

router = APIRouter(prefix="/catalogos/entes", tags=["Entes"])

# ==========================
# Rutas
# ==========================

# GET → Consulta entes
@router.get("/", response_model=List[schemas.EnteOut])
def get_entes(p_id: str = "-99", p_descripcion: str = "-99", db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_ente(:p_id, :p_descripcion)"),
            {"p_id": p_id, "p_descripcion": p_descripcion},
        )
        # Row en SQLAlchemy 2.x se accede con ._mapping
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST → Crear ente
@router.post("/", response_model=int)
def create_ente(ente: schemas.EnteCreate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, :descripcion, :siglas, :clasificacion, :id_ente_tipo, :activo
                ) AS result
            """),
            {
                "accion": "NUEVO",
                "p_id": None,
                "descripcion": ente.descripcion,
                "siglas": ente.siglas,
                "clasificacion": ente.clasificacion,
                "id_ente_tipo": ente.id_ente_tipo,  # debe coincidir con valores tipo "DEPE", "ODES"
                "activo": ente.activo,
            },
        )
        new_id = result.scalar()
        db.commit()  # ✅ IMPORTANTE
        return new_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# PUT → Editar ente
@router.put("/{ente_id}", response_model=int)
def update_ente(ente_id: int, ente: schemas.EnteUpdate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, :descripcion, :siglas, :clasificacion, :id_ente_tipo, :activo
                ) AS result
            """),
            {
                "accion": "EDITAR",
                "p_id": ente_id,
                "descripcion": ente.descripcion,
                "siglas": ente.siglas,
                "clasificacion": ente.clasificacion,
                "id_ente_tipo": ente.id_ente_tipo,
                "activo": ente.activo,
            },
        )
        out = result.scalar()
        db.commit()  # ✅ CONFIRMAR
        return out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# DELETE → Eliminar (desactivar)
@router.delete("/{ente_id}", response_model=int)
def delete_ente(ente_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, NULL, NULL, NULL, NULL, NULL
                ) AS result
            """),
            {"accion": "ELIMINAR", "p_id": ente_id},
        )
        out = result.scalar()
        db.commit()  # ✅ CONFIRMAR
        return out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))