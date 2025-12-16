from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/calendario/fechas",
    tags=["Procesos - Calendario - Fechas"]
)

# ===========================================================
# 🔹 Agregar o eliminar fechas del calendario
# ===========================================================
@router.post("/")
def gestionar_fecha_calendario(
    data: schemas.CalendarioFechaIn,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_calendario_fechas_gestionar
    para insertar o eliminar fechas del calendario.
    """
    try:
        query = text("""
            SELECT procesos.sp_calendario_fechas_gestionar(
                :p_accion,
                CAST(:p_id_calendario AS INTEGER),
                CAST(:p_fecha AS DATE),
                CAST(:p_hora AS TIMESTAMP),
                CAST(:p_id_usuario_registra AS INTEGER)
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_calendario": data.p_id_calendario,
            "p_fecha": data.p_fecha,
            "p_hora": data.p_hora or None,
            "p_id_usuario_registra": data.p_id_usuario_registra or 0,
        }

        result = db.execute(query, params).fetchone()
        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No hubo respuesta del SP")

        return {
            "resultado": int(result[0]),
            "mensaje": "✅ Operación realizada correctamente"
        }

    except Exception as e:
        print("❌ Error en gestionar_fecha_calendario:", e)
        raise HTTPException(status_code=500, detail=str(e))