# ============================================================
# 📦 ENDPOINT: sp_add_remove_rubro_v2
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import RubroRequest

router = APIRouter(
    prefix="/procesos/seguimiento/partida-rubro-ente-v2",
    tags=["Proceso Seguimiento - Partida Rubro v2"]
)

# ============================================================
# 🔹 Ejecutar SP procesos.sp_seguimiento_partida_rubro_ente_captura_v2
# ============================================================
@router.post("/")
def ejecutar_sp_rubro_v2(req: RubroRequest, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_rubro_captura
    para crear o eliminar un rubro dentro de una partida.
    """
    try:
        query = text("""
            SELECT procesos.sp_ente_seguimiento_partida_rubro_captura(
                :p_accion,
                :p_id_seguimiento_partida,
                :p_id,
                :p_e_id_rubro,
                :p_e_monto_presupuesto_suficiencia
            )
        """)

        result = db.execute(query, {
            "p_accion": req.p_accion.upper(),
            "p_id_seguimiento_partida": req.p_id_seguimiento_partida,
            "p_id": req.p_id,
            "p_e_id_rubro": req.p_e_id_rubro,
            "p_e_monto_presupuesto_suficiencia": req.p_e_monto_presupuesto_suficiencia
        }).scalar()

        db.commit()

        return {"resultado": result}

    except Exception as e:
        print("❌ Error ejecutando SP:", e)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))