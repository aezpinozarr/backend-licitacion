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
# 🔹 Crear o editar proceso de seguimiento del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_proceso_ente(data: schemas.ProcesoSeguimientoEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_ente_captura
    para crear o editar un registro de seguimiento del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_ente_captura(
                :p_accion,
                :p_id,
                :p_e_id_ente,
                :p_e_oficio_invitacion,
                :p_e_id_servidor_publico_emite,
                :p_e_servidor_publico_cargo,
                :p_e_tipo_licitacion,
                :p_e_tipo_licitacion_no_veces,
                :p_e_tipo_licitacion_notas,
                :p_e_fecha_y_hora_reunion,
                :p_e_id_usuario_registra
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id": data.p_id,
            "p_e_id_ente": data.p_e_id_ente,
            "p_e_oficio_invitacion": data.p_e_oficio_invitacion,
            "p_e_id_servidor_publico_emite": data.p_e_id_servidor_publico_emite,
            "p_e_servidor_publico_cargo": data.p_e_servidor_publico_cargo,
            "p_e_tipo_licitacion": data.p_e_tipo_licitacion,
            "p_e_tipo_licitacion_no_veces": data.p_e_tipo_licitacion_no_veces,
            "p_e_tipo_licitacion_notas": data.p_e_tipo_licitacion_notas,
            "p_e_fecha_y_hora_reunion": data.p_e_fecha_y_hora_reunion,
            "p_e_id_usuario_registra": data.p_e_id_usuario_registra
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el proceso")

        return {"resultado": result, "mensaje": "✅ Registro guardado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar proceso de ente:", e)
        raise HTTPException(status_code=500, detail=str(e))