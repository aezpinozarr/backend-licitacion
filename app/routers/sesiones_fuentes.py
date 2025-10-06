from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/sesiones-fuentes",
    tags=["Sesiones – Fuentes de financiamiento"]
)

# ===========================
# Crear nueva relación fuente ↔ sesión
# ===========================
@router.post("/", response_model=int)
def add_fuente_sesion(
    data: schemas.SesionFuenteCreate,
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("""
                SELECT procesos.sp_calendario_sesiones_fuentes_financiamiento_gestionarv2(
                    'NUEVO',
                    :p_id_calendario_sesiones,
                    :p_id_fuente_financiamiento
                )
            """),
            {
                "p_id_calendario_sesiones": data.id_calendario_sesiones,
                "p_id_fuente_financiamiento": data.id_fuente_financiamiento
            }
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error agregando fuente a sesión: {str(e)}")


# ===========================
# Eliminar relación fuente ↔ sesión
# ===========================
@router.delete("/", response_model=int)
def remove_fuente_sesion(
    data: schemas.SesionFuenteCreate,
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("""
                SELECT procesos.sp_calendario_sesiones_fuentes_financiamiento_gestionarv2(
                    'ELIMINAR',
                    :p_id_calendario_sesiones,
                    :p_id_fuente_financiamiento
                )
            """),
            {
                "p_id_calendario_sesiones": data.id_calendario_sesiones,
                "p_id_fuente_financiamiento": data.id_fuente_financiamiento
            }
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando fuente de sesión: {str(e)}")


# ===========================
# Listar fuentes de una sesión
# ===========================
@router.get("/{id_calendario_sesion}", response_model=List[schemas.SesionFuenteOut])
def get_fuentes_by_sesion(id_calendario_sesion: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT * 
                FROM procesos.sp_calendario_sesiones_fuentes_financiamiento(
                    :p_id_calendario_sesiones, -99
                )
            """),
            {"p_id_calendario_sesiones": id_calendario_sesion}
        ).mappings().all()

        return [schemas.SesionFuenteOut(**row) for row in result]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo fuentes de la sesión: {str(e)}"
        )