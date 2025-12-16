from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

# ===========================================================
# Consultar fechas del calendario
# SP: procesos.sp_calendario_fechas
# ===========================================================
@router.get("/fechas")
def consultar_fechas_calendario(
    p_id_calendario: int = -99,
    p_fecha1: str = "-99",
    p_fecha2: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Consulta las fechas asociadas a un calendario.
    Llama al SP procesos.sp_calendario_fechas.
    """

    try:
        sql = text("""
            SELECT * FROM procesos.sp_calendario_fechas(
                CAST(:p_id_calendario AS BIGINT),
                CAST(:p_fecha1 AS VARCHAR),
                CAST(:p_fecha2 AS VARCHAR)
            );
        """)

        result = db.execute(sql, {
            "p_id_calendario": p_id_calendario,
            "p_fecha1": p_fecha1,
            "p_fecha2": p_fecha2
        }).fetchall()

        fechas = [
            {
                "id_calendario": r[0],
                "fecha": r[1],
                "hora": r[2],
                "fecha_y_hora_sistema": r[3],
                "id_usuario_registra": r[4],
            }
            for r in result
        ]

        return {
            "cantidad": len(fechas),
            "fechas": fechas
        }

    except Exception as e:
        print("❌ Error en consultar_fechas_calendario:", e)
        raise HTTPException(status_code=500, detail=str(e))