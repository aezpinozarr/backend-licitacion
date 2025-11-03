from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/rector-seguimiento-detallev1",
    tags=["sp_rector_seguimiento_detallev1"]
)

@router.get("/", summary="Ejecutar SP Rector Seguimiento Detalle v1")
def ejecutar_sp_rector_seguimiento_detallev1(
    p_id: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db)
):
    """
    🧩 Ejecuta el SP procesos.sp_rector_seguimiento_detallev1
    Devuelve información detallada del seguimiento (ente, rector, partidas, rubros, proveedores).
    """
    try:
        query = text("""
            SELECT * FROM procesos.sp_rector_seguimiento_detallev1(:p_id, :p_id_ente);
        """)

        result = db.execute(query, {
            "p_id": p_id,
            "p_id_ente": p_id_ente
        }).mappings().all()

        # 🔹 Estandarizamos la respuesta
        data = [dict(row) for row in result]

        if not data:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron registros para los parámetros indicados."
            )

        return {
            "status": "success",
            "message": "Datos obtenidos correctamente.",
            "data": data
        }

    except Exception as e:
        print("❌ Error al ejecutar SP:", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error ejecutando SP: {str(e)}"
        )