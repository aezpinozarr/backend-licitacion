from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.db import get_db

router = APIRouter(
    prefix="/seguridad/notificaciones",
    tags=["Seguridad - Notificaciones"]
)

@router.post("/", response_model=dict)
def gestionar_notificaciones(
    p_accion: str = Query(..., description="Acción a ejecutar: CREAR, CONSULTAR, LEER o ELIMINAR"),
    p_id_usuario_origen: Optional[int] = Query(None, description="ID del usuario que origina la acción"),
    p_id_usuario_destinatario: Optional[int] = Query(None, description="ID del usuario que recibirá la notificación"),
    p_id_notificacion: Optional[int] = Query(None, description="ID de la notificación (para LEER o ELIMINAR)"),
    p_id_ente: Optional[int] = Query(None, description="ID del ente asociado (si aplica)"),
    p_mensaje_extra: Optional[str] = Query(None, description="Mensaje adicional o personalizado"),
    p_estatus: Optional[str] = Query(None, description="Estatus asociado (REVISADO, CANCELADO, etc.)"),
    db: Session = Depends(get_db)
):
    try:
        accion = p_accion.strip().upper()
        if accion not in ("CREAR", "CONSULTAR", "LEER", "ELIMINAR"):
            raise HTTPException(status_code=400, detail="Acción inválida. Usa CREAR, CONSULTAR, LEER o ELIMINAR.")

        sp_query = text("""
            SELECT seguridad.sp_notificaciones_gestionar(
                :p_accion,
                :p_id_usuario_origen,
                :p_id_usuario_destinatario,
                :p_id_notificacion,
                :p_id_ente,
                :p_mensaje_extra,
                :p_estatus
            )
        """)

        result = db.execute(sp_query, {
            "p_accion": accion,
            "p_id_usuario_origen": p_id_usuario_origen,
            "p_id_usuario_destinatario": p_id_usuario_destinatario,
            "p_id_notificacion": p_id_notificacion,
            "p_id_ente": p_id_ente,
            "p_mensaje_extra": p_mensaje_extra,
            "p_estatus": p_estatus
        }).scalar()

        # 🔹 Muy importante: confirmar la transacción
        db.commit()

        # 🧩 Log visible en la terminal
        print(f"✅ Notificación registrada correctamente para el usuario {p_id_usuario_origen} (ente {p_id_ente})")

        return result

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en /seguridad/notificaciones:", e)
        db.rollback()  # 🧯 Por seguridad si algo falla
        raise HTTPException(status_code=500, detail="Error al gestionar notificaciones")