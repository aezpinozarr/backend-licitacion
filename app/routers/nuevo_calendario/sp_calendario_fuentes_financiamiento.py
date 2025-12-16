from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

# ===========================================================
# Consultar fuentes de financiamiento del calendario
# SP: procesos.sp_calendario_fuentes_financiamiento
# ===========================================================
@router.get("/fuentes-financiamiento")
def consultar_fuentes_financiamiento(
    p_id_calendario: int = -99,
    p_id_fuente_financiamiento: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Consulta las fuentes de financiamiento de un calendario.
    Llama al SP procesos.sp_calendario_fuentes_financiamiento.
    """

    try:
        sql = text("""
            SELECT * FROM procesos.sp_calendario_fuentes_financiamiento(
                CAST(:p_id_calendario AS BIGINT),
                CAST(:p_id_fuente_financiamiento AS VARCHAR)
            );
        """)

        result = db.execute(sql, {
            "p_id_calendario": p_id_calendario,
            "p_id_fuente_financiamiento": p_id_fuente_financiamiento
        }).fetchall()

        fuentes = [
            {
                "id_calendario": r[0],
                "id_fuente_financiamiento": r[1],
                "fuente_descripcion": r[2],
                "fecha_y_hora_sistema": r[3],
                "id_usuario_registra": r[4],
            }
            for r in result
        ]

        return {
            "cantidad": len(fuentes),
            "fuentes": fuentes
        }

    except Exception as e:
        print("❌ Error en consultar_fuentes_financiamiento:", e)
        raise HTTPException(status_code=500, detail=str(e))