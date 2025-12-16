from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

# ===========================================================
# 🔹 Crear, editar o eliminar un registro del calendario
# ===========================================================
@router.post("/")
def gestionar_calendario(data: schemas.CalendarioGestionarIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_calendario_gestionar
    para crear, editar o eliminar un registro del calendario.
    """
    try:
        query = text("""
            SELECT procesos.sp_calendario_gestionar(
                CAST(:p_accion AS TEXT),
                CAST(:p_id AS INTEGER),
                CAST(:p_acuerdo_o_numero_licitacion AS TEXT),
                CAST(:p_id_ente AS TEXT),
                CAST(:p_id_servidor_publico AS INTEGER),
                CAST(:p_servidor_publico_cargo AS TEXT),
                CAST(:p_tipo_licitacion AS TEXT),
                CAST(:p_tipo_licitacion_no_veces AS INTEGER),
                CAST(:p_tipo_evento AS TEXT),
                CAST(:p_id_usuario_registra AS INTEGER)
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id": data.p_id or 0,
            "p_acuerdo_o_numero_licitacion": data.p_acuerdo_o_numero_licitacion or "",
            "p_id_ente": data.p_id_ente or 0,
            "p_id_servidor_publico": data.p_id_servidor_publico or 0,
            "p_servidor_publico_cargo": data.p_servidor_publico_cargo or "",
            "p_tipo_licitacion": data.p_tipo_licitacion or "",
            "p_tipo_licitacion_no_veces": data.p_tipo_licitacion_no_veces or 0,
            "p_tipo_evento": data.p_tipo_evento or "",
            "p_id_usuario_registra": data.p_id_usuario_registra or 0,
        }

        # Ejecutar SP
        result = db.execute(query, params).fetchone()
        db.commit()

        if not result or not result[0]:
            raise HTTPException(status_code=400, detail="No se pudo procesar la acción solicitada")

        # ✅ El SP YA devuelve JSON, NO convertir a string
        sp_json = result[0]

        # Retornar EL JSON EXACTO DEL SP
        return sp_json

    except Exception as e:
        print("❌ Error en gestionar_calendario:", e)
        raise HTTPException(status_code=500, detail=str(e))