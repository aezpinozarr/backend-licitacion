from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import EnteSeguimientoPartidaUpdate

router = APIRouter(
    prefix="/procesos/editar",
    tags=["Editar - Seguimiento (Paso 2)"]
)

@router.put("/ente-seguimiento-partida-captura", response_model=int)
def update_ente_seguimiento_partida_captura(
    payload: EnteSeguimientoPartidaUpdate,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_captura_v2 con acción 'NUEVO' o 'EDITAR'
    según corresponda, para insertar o actualizar una partida asociada a un seguimiento (Paso 2).
    """
    try:
        # 📋 Log de lo que realmente llega al backend
        print("📥 Payload recibido:", payload.dict())

        # Determina si es una edición o una nueva inserción
        accion = "EDITAR" if payload.p_id and payload.p_id > 0 else "NUEVO"

        sql = text("""
            SELECT procesos.sp_ente_seguimiento_partida_captura_v2(
                :p_accion,
                :p_id_seguimiento,
                :p_id,
                :p_e_no_requisicion,
                :p_e_id_partida,
                :p_e_id_fuente_financiamiento
            ) AS result
        """)

        result = db.execute(sql, {
            "p_accion": accion,
            "p_id_seguimiento": payload.p_id_seguimiento,
            "p_id": payload.p_id,
            "p_e_no_requisicion": payload.p_e_no_requisicion,
            "p_e_id_partida": payload.p_e_id_partida,
            "p_e_id_fuente_financiamiento": payload.p_e_id_fuente_financiamiento
        }).scalar()

        db.commit()

        if result is None or result == 0:
            print(f"⚠️ SP devolvió {result}. No se realizó actualización/inserción.")
            raise HTTPException(status_code=400, detail="No se realizaron cambios (puede que ya exista o el ID sea inválido).")

        print(f"✅ Operación {accion} completada con ID resultado: {result}")
        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en /procesos/editar/ente-seguimiento-partida-captura:", str(e))
        raise HTTPException(status_code=500, detail=str(e))