from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

# ===========================================================
# Consultar calendario (SP: procesos.sp_calendario)
# ===========================================================
@router.get("/consultar")
def consultar_calendario(
    p_id: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Consulta el calendario llamando al SP procesos.sp_calendario.
    Filtra por id y/o id_ente.
    """

    try:
        sql = text("""
            SELECT * FROM procesos.sp_calendario(
                CAST(:p_id AS INTEGER),
                CAST(:p_id_ente AS VARCHAR)
            );
        """)

        result = db.execute(sql, {"p_id": p_id, "p_id_ente": p_id_ente})
        rows = result.fetchall()

        # Convertir filas en diccionarios
        calendario = [
            {
                "id": r[0],
                "acuerdo_o_numero_licitacion": r[1],
                "fecha_y_hora_sistema": r[2],
                "id_ente": r[3],
                "ente": r[4],
                "ente_siglas": r[5],
                "ente_clasificacion": r[6],
                "id_ente_tipo": r[7],
                "ente_tipo": r[8],
                "id_servidor_publico": r[9],
                "servidor_publico": r[10],
                "servidor_publico_cargo": r[11],
                "tipo_licitacion": r[12],
                "tipo_licitacion_no_veces": r[13],
                "tipo_evento": r[14],
                "estatus": r[15],
                "id_usuario_registra": r[16],
                "r_id_servidor_publico_asiste": r[17],
                "rector_asiste": r[18],
                "r_observaciones": r[19],
            }
            for r in rows
        ]

        return {
            "cantidad": len(calendario),
            "calendario": calendario
        }

    except Exception as e:
        print("❌ Error en consultar_calendario:", e)
        raise HTTPException(status_code=500, detail=str(e))