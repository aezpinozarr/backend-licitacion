from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/catalogos/entidad-federativa",
    tags=["Catálogo Entidad Federativa"]
)

# ===============================
# Obtener entidades federativas
# ===============================
@router.get("/", response_model=List[schemas.EntidadFederativaOut])
def get_entidades(
    p_id: Optional[str] = Query("-99", description="ID de la entidad federativa (-99 para todas)"),
    db: Session = Depends(get_db)
):
    """
    Devuelve todas las entidades federativas (o una específica por ID)
    """
    try:
        rows = db.execute(
            text("SELECT * FROM catalogos.sp_cat_entidad_federativa(:p_id)"),
            {"p_id": p_id}
        ).mappings().all()

        return [schemas.EntidadFederativaOut(**row) for row in rows]
    except Exception as e:
        print("❌ Error en /entidad-federativa:", repr(e))
        raise HTTPException(status_code=500, detail="Error al obtener las entidades federativas")