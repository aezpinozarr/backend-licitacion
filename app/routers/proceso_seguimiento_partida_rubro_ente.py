from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/partida-rubro-ente",
    tags=["Proceso Seguimiento - Partida Rubro Ente"]
)

# ===========================================================
# 🔹 Crear o editar rubro asociado a la partida
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_partida_rubro_ente(data: schemas.ProcesoPartidaRubroEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_rubro_captura
    para crear o editar el rubro de una partida.
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

        params = {
            "p_accion": data.p_accion,
            "p_id_seguimiento_partida": data.p_id_seguimiento_partida,
            "p_id": int(data.p_id) if data.p_id is not None else 0,
            "p_e_id_rubro": str(data.p_e_id_rubro),
            "p_e_monto_presupuesto_suficiencia": float(data.p_e_monto_presupuesto_suficiencia) if data.p_e_monto_presupuesto_suficiencia is not None else 0.0
        }

        print("Executing stored procedure with params:", params)

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el rubro")

        return {"resultado": result, "mensaje": "✅ Rubro registrado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar rubro del ente:", e)
        raise HTTPException(status_code=500, detail=str(e))