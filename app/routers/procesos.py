from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/seguimiento",
    tags=["Procesos - Seguimiento"],
)

@router.get("/detalle/")
def obtener_detalle_seguimiento(p_id: int, db: Session = Depends(get_db)):
    """
    🔹 Devuelve toda la información de un proceso (de los 4 pasos)
    a partir de la vista unificada v_seguimiento_y_presupuesto_y_rubro_y_proveedor.
    """
    try:
        # ✅ Consulta envuelta con text()
        query = text("""
            SELECT *
            FROM procesos.v_seguimiento_y_presupuesto_y_rubro_y_proveedor
            WHERE id = :id
        """)

        # ✅ Ejecutar query con parámetro
        result = db.execute(query, {"id": p_id}).fetchall()

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron registros para el proceso con id {p_id}"
            )

        # ✅ Convertir resultado a lista de diccionarios (para JSON)
        data = [dict(row._mapping) for row in result]

        return {
            "status": "ok",
            "total": len(data),
            "datos": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el detalle del proceso: {str(e)}"
        )