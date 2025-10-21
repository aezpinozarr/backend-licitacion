from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/partida-ente",
    tags=["Proceso Seguimiento - Partida Ente"]
)

# ===========================================================
# 🔹 Crear o editar partida del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_partida_ente(data: schemas.ProcesoPartidaEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_captura
    para crear o editar la información de la partida del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_ente_seguimiento_partida_captura(
                :p_accion,
                :p_id_seguimiento,
                :p_id,
                :p_e_no_requisicion,
                :p_e_id_partida,
                :p_e_id_fuente_financiamiento
            )
        """)

        params = {
        "p_accion": data.p_accion,
            "p_id_seguimiento": data.p_id_seguimiento,  # 👈 campo correcto según schemas.py
            "p_id": data.p_id,
            "p_e_no_requisicion": data.p_e_no_requisicion,
            "p_e_id_partida": data.p_e_id_partida,
            "p_e_id_fuente_financiamiento": data.p_e_id_fuente_financiamiento,
        }

        result = db.execute(query, params).scalar()
        db.commit()

        print("🧩 Resultado SP Partida Ente:", result)

        if not result or result == 0:
            raise HTTPException(status_code=400, detail="No se pudo registrar la partida del ente")

        return {"resultado": result, "mensaje": "✅ Partida registrada correctamente"}

    except Exception as e:
        print("❌ Error al gestionar partida del ente:", e)
        raise HTTPException(status_code=500, detail=str(e))