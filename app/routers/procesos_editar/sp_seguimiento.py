from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from app.db import get_db

router = APIRouter(prefix="/procesos/editar", tags=["Editar - Seguimiento"])

@router.get("/seguimiento", response_model=List[dict])
def get_seguimiento(
    p_id: Optional[int] = Query(-99, description="ID del seguimiento (-99 para todos)"),
    p_id_ente: Optional[str] = Query("-99", description="ID del ente (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_seguimiento para obtener datos del seguimiento.
    Se usa en el paso 1 (Oficio de invitación) del formulario de edición.
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM procesos.sp_seguimiento(:p_id, :p_id_ente)
            """),
            {"p_id": p_id, "p_id_ente": p_id_ente}
        ).mappings().all()

        return [dict(row) for row in result]
    except Exception as e:
        print("❌ Error en /procesos/editar/seguimiento:", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")