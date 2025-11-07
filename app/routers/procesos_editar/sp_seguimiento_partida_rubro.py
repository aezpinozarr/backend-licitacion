from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from app.db import get_db

router = APIRouter(prefix="/procesos/editar", tags=["Editar - Seguimiento Partida Rubro"])

@router.get("/seguimiento-partida-rubro", response_model=List[dict])
def get_seguimiento_partida_rubro(
    p_id: Optional[int] = Query(-99, description="ID del rubro (-99 para todos)"),
    p_id_seguimiento_partida: Optional[int] = Query(-99, description="ID de la partida (-99 para todas)"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_seguimiento_partida_rubro para obtener los rubros
    asociados a una partida. (Usado en el Paso 3 del formulario de edición)
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM procesos.sp_seguimiento_partida_rubro(:p_id, :p_id_seguimiento_partida)
            """),
            {"p_id": p_id, "p_id_seguimiento_partida": p_id_seguimiento_partida}
        ).mappings().all()

        return [dict(row) for row in result]
    except Exception as e:
        print("❌ Error en /procesos/editar/seguimiento-partida-rubro:", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")