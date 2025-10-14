# app/routers/proceso_detalle.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/seguimiento",
    tags=["Procesos - Seguimiento"]
)

@router.get("/detalle/")
def obtener_detalle_seguimiento(
    p_id: int = Query(..., description="ID del proceso de seguimiento"),
    db: Session = Depends(get_db)
):
    try:
        query = text("""
            SELECT *
            FROM procesos.v_seguimiento_y_presupuesto_y_rubro_y_proveedor
            WHERE id = :p_id
        """)
        result = db.execute(query, {"p_id": p_id}).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron registros para ese proceso.")

        data = [dict(row._mapping) for row in result]

        return {
            "status": "ok",
            "total": len(data),
            "datos": data  # 👈 devolvemos TODAS las filas
        }

    except Exception as e:
        print("❌ Error al obtener detalle de proceso:", e)
        raise HTTPException(status_code=500, detail=str(e))