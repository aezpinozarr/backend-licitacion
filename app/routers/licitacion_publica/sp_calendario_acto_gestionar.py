from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

@router.post("/acto/gestionar")
def calendario_acto_gestionar(
    request: dict,  
    db: Session = Depends(get_db)
):
    try:
        fecha_hora = f"{request['p_fecha']} {request['p_hora']}"

        sql = text("""
            SELECT procesos.sp_calendario_acto_gestionar(
                CAST(:p_accion AS TEXT),
                CAST(:p_id_calendario AS BIGINT),
                CAST(:p_id_listado_entregables AS INTEGER),
                CAST(:p_fecha AS DATE),
                CAST(:p_hora AS TIMESTAMP),
                CAST(:p_id_usuario_registra AS INTEGER)
            );
        """)

        result = db.execute(sql, {
            "p_accion": request["p_accion"],
            "p_id_calendario": request["p_id_calendario"],
            "p_id_listado_entregables": request["p_id_listado_entregables"],
            "p_fecha": request["p_fecha"],
            "p_hora": fecha_hora,
            "p_id_usuario_registra": request["p_id_usuario_registra"]
        })

        row = result.fetchone()

        db.commit()  # OBLIGATORIO PARA QUE SE GUARDE EN BD

        return row[0]

    except Exception as e:
        db.rollback()  # Limpia transacción en caso de error
        print("❌ Error en calendario_acto_gestionar:", e)
        raise HTTPException(status_code=500, detail=str(e))