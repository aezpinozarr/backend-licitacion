from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from app.db import get_db

router = APIRouter(prefix="/procesos/editar", tags=["Editar - Seguimiento Partida"])

@router.get("/seguimiento-partida", response_model=List[dict])
def get_seguimiento_partida(
    p_id: Optional[int] = Query(-99, description="ID de la partida (-99 para todas)"),
    p_id_seguimiento: Optional[int] = Query(-99, description="ID del seguimiento (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_seguimiento_partida para obtener las partidas
    relacionadas con un seguimiento. (Usado en el Paso 2 del formulario de edición)
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM procesos.sp_seguimiento_partida(:p_id, :p_id_seguimiento)
            """),
            {"p_id": p_id, "p_id_seguimiento": p_id_seguimiento}
        ).mappings().all()

        return [dict(row) for row in result]
    except Exception as e:
        print("❌ Error en /procesos/editar/seguimiento-partida:", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")