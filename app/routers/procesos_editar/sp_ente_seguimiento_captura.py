from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.db import get_db
from app.schemas import EnteSeguimientoUpdate

router = APIRouter(
    prefix="/procesos/editar",
    tags=["Editar - Seguimiento (Paso 1)"]
)

@router.put("/ente-seguimiento-captura", response_model=int)
def update_ente_seguimiento_captura(
    payload: EnteSeguimientoUpdate,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_ente_seguimiento_captura con acción 'EDITAR'
    para actualizar la información del Paso 1 (datos generales del proceso).
    """
    try:
        sql = text("""
            SELECT procesos.sp_ente_seguimiento_captura(
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
            ) AS result
        """)

        result = db.execute(sql, {
            "p_accion": "EDITAR",
            "p_id": payload.p_id,
            "p_e_id_ente": payload.p_e_id_ente,
            "p_e_oficio_invitacion": payload.p_e_oficio_invitacion,
            "p_e_id_servidor_publico_emite": payload.p_e_id_servidor_publico_emite,
            "p_e_servidor_publico_cargo": payload.p_e_servidor_publico_cargo,
            "p_e_tipo_licitacion": payload.p_e_tipo_licitacion,
            "p_e_tipo_licitacion_no_veces": payload.p_e_tipo_licitacion_no_veces,
            "p_e_tipo_licitacion_notas": payload.p_e_tipo_licitacion_notas,
            "p_e_fecha_y_hora_reunion": payload.p_e_fecha_y_hora_reunion,
            "p_e_id_usuario_registra": payload.p_e_id_usuario_registra
        }).scalar()

        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el registro.")

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en /procesos/editar/ente-seguimiento-captura:", str(e))
        raise HTTPException(status_code=500, detail=str(e))