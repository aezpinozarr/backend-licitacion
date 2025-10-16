from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/ente",
    tags=["Proceso Seguimiento - Ente"]
)

# ===========================================================
# 🔹 Crear o editar proceso del ente
# ===========================================================
@router.post("/")
def gestionar_proceso_ente(data: schemas.ProcesoSeguimientoEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_ente_captura
    para crear o editar el proceso del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_ente_captura(
                :p_accion,
                CAST(:p_id AS INTEGER),
                CAST(:p_e_id_ente AS TEXT),
                CAST(:p_e_oficio_invitacion AS TEXT),
                CAST(:p_e_id_servidor_publico_emite AS INTEGER),
                CAST(:p_e_servidor_publico_cargo AS TEXT),
                CAST(:p_e_tipo_licitacion AS TEXT),
                CAST(:p_e_tipo_licitacion_no_veces AS INTEGER),
                CAST(:p_e_tipo_licitacion_notas AS TEXT),
                CAST(:p_e_fecha_y_hora_reunion AS TIMESTAMP),
                CAST(:p_e_id_usuario_registra AS INTEGER)
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id": data.p_id or 0,
            "p_e_id_ente": str(data.p_e_id_ente),
            "p_e_oficio_invitacion": data.p_e_oficio_invitacion or "",
            "p_e_id_servidor_publico_emite": data.p_e_id_servidor_publico_emite,
            "p_e_servidor_publico_cargo": data.p_e_servidor_publico_cargo or "",
            "p_e_tipo_licitacion": data.p_e_tipo_licitacion or "",
            "p_e_tipo_licitacion_no_veces": data.p_e_tipo_licitacion_no_veces or 0,
            "p_e_tipo_licitacion_notas": data.p_e_tipo_licitacion_notas or "",
            "p_e_fecha_y_hora_reunion": data.p_e_fecha_y_hora_reunion,
            "p_e_id_usuario_registra": data.p_e_id_usuario_registra,
        }

        result = db.execute(query, params).fetchone()
        db.commit()

        if not result or not result[0]:
            raise HTTPException(status_code=400, detail="No se pudo registrar el proceso del ente")

        return {"resultado": str(result[0]), "mensaje": "✅ Proceso del ente registrado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar proceso de ente:", e)
        raise HTTPException(status_code=500, detail=str(e))