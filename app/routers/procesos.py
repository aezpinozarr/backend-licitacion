# app/routers/proceso_detalle.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/seguimiento",
    tags=["Procesos - Seguimiento"],
)

@router.get("/detalle/")
def obtener_detalle_seguimiento(
    p_id: int = Query(..., description="ID del proceso de seguimiento"),
    db: Session = Depends(get_db)
):
    """
    🔹 Devuelve toda la información de un proceso (de los 4 pasos)
    a partir de la vista unificada v_seguimiento_y_partida_y_rubro_y_proveedor.
    """
    try:
        query = text("""
            SELECT *
            FROM procesos.v_seguimiento_y_partida_y_rubro_y_proveedor
            WHERE id = :p_id
        """)

        result = db.execute(query, {"p_id": p_id}).fetchall()

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron registros para el proceso con id {p_id}"
            )

        data = [dict(row._mapping) for row in result]

        return {
            "status": "ok",
            "total": len(data),
            "datos": data
        }

    except Exception as e:
        print("❌ Error al obtener detalle de proceso:", e)
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el detalle del proceso: {str(e)}"
        )