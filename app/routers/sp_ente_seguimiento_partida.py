from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/ente-seguimiento-partida",
    tags=["Procesos - Ente Seguimiento Partida"]
)

@router.get("/")
def get_ente_seguimiento_partida(
    p_id: int = Query(-99, description="ID de la partida (-99 para todos)"),
    p_id_seguimiento: int = Query(-99, description="ID del seguimiento (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene las partidas asociadas a un seguimiento de ente
    mediante el procedimiento almacenado sp_ente_seguimiento_partida.
    """
    try:
        query = text("""
            SELECT * 
            FROM procesos.sp_ente_seguimiento_partida(:p_id, :p_id_seguimiento)
        """)

        result = db.execute(query, {
            "p_id": p_id,
            "p_id_seguimiento": p_id_seguimiento
        }).mappings().all()

        return result

    except Exception as e:
        print("❌ Error al ejecutar sp_ente_seguimiento_partida:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los datos: {str(e)}"
        )