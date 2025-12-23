from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/calendario",
    tags=["Procesos - Calendario"]
)

# ===========================================================
# SP: procesos.sp_calendario_acto_popular
# ===========================================================
@router.get("/acto-popular")
def calendario_acto_popular(
    p_id_calendario: int = -99,
    p_id_listado_entregables: int = -99,
    db: Session = Depends(get_db)
):
    """
    Consulta los actos del calendario junto con el catálogo de entregables,
    llamando al SP procesos.sp_calendario_acto_popular.
    """

    try:
        sql = text("""
            SELECT *
            FROM procesos.sp_calendario_acto_popular(
                CAST(:p_id_calendario AS BIGINT),
                CAST(:p_id_listado_entregables AS INTEGER)
            );
        """)

        result = db.execute(sql, {
            "p_id_calendario": p_id_calendario,
            "p_id_listado_entregables": p_id_listado_entregables
        })

        rows = result.fetchall()

        data = [
            {
                "id_calendario": r[0],
                "id_listado_entregables": r[1],
                "descripcion": r[2],
                "fecha": r[3],
                "hora": r[4],
            }
            for r in rows
        ]

        return {
            "cantidad": len(data),
            "items": data
        }

    except Exception as e:
        print("❌ Error en calendario_acto_popular:", e)
        raise HTTPException(status_code=500, detail=str(e))