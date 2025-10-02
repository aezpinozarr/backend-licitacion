# app/routers/servidor_publico.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.db import get_db
from app.schemas import (
    ServidorPublicoOut,
    ServidorPublicoCreate,
    ServidorPublicoUpdate,
)

router = APIRouter(prefix="/catalogos/servidores-publicos", tags=["Servidores Públicos"])


# ==============================
# GET -> Consultar servidores
# ==============================
@router.get("/", response_model=List[ServidorPublicoOut])
def get_servidores(p_id: int = -99, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_servidor_publico(:p_id)"),
            {"p_id": p_id},
        ).fetchall()

        return [dict(row._mapping) for row in result]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# POST -> Crear servidor
# ==============================
@router.post("/", response_model=int)
def create_servidor(data: ServidorPublicoCreate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text(
                "SELECT catalogos.sp_cat_servidor_publico_gestionar(:accion, NULL, :nombre, :cargo, :activo)"
            ),
            {
                "accion": "NUEVO",
                "nombre": data.nombre,
                "cargo": data.cargo,
                "activo": data.activo,
            },
        ).scalar()
        db.commit()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# PUT -> Editar servidor
# ==============================
@router.put("/", response_model=int)
def update_servidor(data: ServidorPublicoUpdate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text(
                "SELECT catalogos.sp_cat_servidor_publico_gestionar(:accion, :id, :nombre, :cargo, :activo)"
            ),
            {
                "accion": "EDITAR",
                "id": data.id,
                "nombre": data.nombre,
                "cargo": data.cargo,
                "activo": data.activo,
            },
        ).scalar()
        db.commit()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# DELETE -> Eliminar servidor (soft delete → activo=false)
# ==============================
@router.delete("/{servidor_id}", response_model=int)
def delete_servidor(servidor_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text(
                "SELECT catalogos.sp_cat_servidor_publico_gestionar(:accion, :id, NULL, NULL, false)"
            ),
            {"accion": "ELIMINAR", "id": servidor_id},
        ).scalar()
        db.commit()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))