# backend/app/api/endpoints/rector/seguimiento_adjudicado.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/rector/seguimiento-adjudicado",
    tags=["sp_rector_seguimiento_adjudicado"]
)

@router.get("/", response_model=list[dict])
def get_adjudicados(
    p_id_ente: str = "-99",
    p_fecha1: str = "-99",
    p_fecha2: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_seguimiento_partida_rubro_proveedor_adjudicado_reporte
    para obtener los proveedores adjudicados con filtros opcionales.
    """
    try:
        result = db.execute(
            text("SELECT * FROM procesos.sp_seguimiento_partida_rubro_proveedor_adjudicado_reporte(:p_id_ente, :p_fecha1, :p_fecha2)"),
            {"p_id_ente": p_id_ente, "p_fecha1": p_fecha1, "p_fecha2": p_fecha2}
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en sp_seguimiento_partida_rubro_proveedor_adjudicado_reporte:", str(e))
        raise HTTPException(status_code=500, detail=str(e))