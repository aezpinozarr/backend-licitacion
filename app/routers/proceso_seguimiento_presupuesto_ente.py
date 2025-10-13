# app/routers/proceso_seguimiento_presupuesto.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/presupuesto-ente",
    tags=["Proceso Seguimiento - Presupuesto Ente"]
)

# ===========================================================
# 🔹 Crear o editar presupuesto del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_presupuesto_ente(data: schemas.ProcesoPresupuestoEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_presupuesto_ente_captura
    para crear o editar la información presupuestal del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_presupuesto_ente_captura(
                :p_accion,
                :p_id_proceso_seguimiento,
                :p_id,
                :p_e_no_requisicion,
                :p_e_id_partida,
                :p_e_id_fuente_financiamiento,
                :p_e_monto_presupuesto_suficiencia
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_proceso_seguimiento": data.p_id_proceso_seguimiento,
            "p_id": data.p_id,
            "p_e_no_requisicion": data.p_e_no_requisicion,
            "p_e_id_partida": data.p_e_id_partida,
            "p_e_id_fuente_financiamiento": data.p_e_id_fuente_financiamiento,
            "p_e_monto_presupuesto_suficiencia": data.p_e_monto_presupuesto_suficiencia,
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el presupuesto del ente")

        return {"resultado": result, "mensaje": "✅ Presupuesto registrado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar presupuesto de ente:", e)
        raise HTTPException(status_code=500, detail=str(e))