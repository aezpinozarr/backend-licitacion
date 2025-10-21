from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/rector/seguimiento-detalle",
    tags=["sp_rector_seguimiento_detalle"]
)

@router.get("/", response_model=list[dict])
def get_rector_detalle(
    p_id: int = -99,
    p_id_proceso: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db),
):
    """
    Llama al SP procesos.sp_rector_seguimiento_detallev1 para obtener los detalles
    completos del seguimiento con sus partidas, rubros y proveedores.
    """
    try:
        # Priorizar p_id_proceso si se envía
        proceso_id = p_id_proceso if p_id_proceso != -99 else p_id

        result = db.execute(
            text("SELECT * FROM procesos.sp_rector_seguimiento_detallev1(:p_id, :p_id_ente)"),
            {"p_id": proceso_id, "p_id_ente": p_id_ente}
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en sp_rector_seguimiento_detalle:", str(e))
        raise HTTPException(status_code=500, detail=str(e))