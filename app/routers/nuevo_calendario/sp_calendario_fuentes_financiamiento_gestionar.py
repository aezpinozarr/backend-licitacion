from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/calendario/fuentes",
    tags=["Procesos - Calendario - Fuentes Financiamiento"]
)

# ===========================================================
# 🔹 Crear o eliminar fuente de financiamiento del calendario
# ===========================================================
@router.post("/")
def gestionar_fuente_calendario(
    data: schemas.CalendarioFuenteIn,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_calendario_fuentes_financiamiento_gestionar
    para agregar o eliminar fuentes de financiamiento del calendario.
    """
    try:
        query = text("""
            SELECT procesos.sp_calendario_fuentes_financiamiento_gestionar(
                :p_accion,
                CAST(:p_id_calendario AS INTEGER),
                :p_id_fuente_financiamiento,   -- YA NO SE CASTEA A INTEGER
                CAST(:p_id_usuario_registra AS INTEGER)
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_calendario": data.p_id_calendario,
            "p_id_fuente_financiamiento": data.p_id_fuente_financiamiento,  # SE ENVÍA COMO STRING
            "p_id_usuario_registra": data.p_id_usuario_registra or 0,
        }

        result = db.execute(query, params).fetchone()
        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No se recibió respuesta del servidor")

        return {
            "resultado": int(result[0]),
            "mensaje": "✅ Operación realizada correctamente"
        }

    except Exception as e:
        print("❌ Error en gestionar_fuente_calendario:", e)
        raise HTTPException(status_code=500, detail=str(e))