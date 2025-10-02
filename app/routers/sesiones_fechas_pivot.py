from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional

from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/sesiones-fechas-pivot",
    tags=["Sesiones Fechas Pivot"]
)

# ===========================
# GET -> Consultar pivot
# ===========================
@router.get("/", response_model=List[schemas.SesionFechaPivotOut])
def get_sesiones_fechas_pivot(
    p_id: Optional[int] = None,
    p_id_calendario: Optional[int] = None,
    p_id_ente: Optional[int] = None,
    p_id_clasificacion_licitacion: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        query = text("""
            SELECT * FROM procesos.sp_calendario_sesiones_fechas_calendario_pivot(
                :p_id, :p_id_calendario, :p_id_ente, :p_id_clasificacion_licitacion
            )
        """)
        result = db.execute(query, {
            "p_id": p_id,
            "p_id_calendario": p_id_calendario,
            "p_id_ente": p_id_ente,
            "p_id_clasificacion_licitacion": p_id_clasificacion_licitacion
        }).mappings().all()

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo pivot: {str(e)}")