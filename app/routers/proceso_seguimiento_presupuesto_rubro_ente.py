# app/routers/proceso_seguimiento_presupuesto_rubro_ente.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/presupuesto-rubro-ente",
    tags=["Proceso Seguimiento - Presupuesto Rubro Ente"]
)

# ===========================================================
# 🔹 Crear o editar presupuesto de rubro del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_presupuesto_rubro_ente(data: schemas.ProcesoPresupuestoRubroEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_presupuesto_rubro_ente_captura
    para crear o editar el presupuesto por rubro del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_presupuesto_rubro_ente_captura(
                :p_accion,
                :p_id_proceso_seguimiento_presupuesto,
                :p_id,
                :p_e_id_rubro,
                :p_e_monto_presupuesto_suficiencia
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_proceso_seguimiento_presupuesto": data.p_id_proceso_seguimiento_presupuesto,
            "p_id": data.p_id,
            "p_e_id_rubro": data.p_e_id_rubro,
            "p_e_monto_presupuesto_suficiencia": data.p_e_monto_presupuesto_suficiencia,
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el presupuesto del rubro")

        return {"resultado": result, "mensaje": "✅ Presupuesto de rubro registrado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar presupuesto de rubro:", e)
        raise HTTPException(status_code=500, detail=str(e))