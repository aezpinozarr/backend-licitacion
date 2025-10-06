# app/routers/ente_servidor_publico.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/catalogos/ente-servidor-publico",
    tags=["Relación Ente - Servidor Público"]
)

# ===============================
# Crear nueva relación
# ===============================
@router.post("/", response_model=int)
def add_ente_servidor_publico(
    data: schemas.EnteServidorPublicoCreate,
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_ente_servidor_publico_gestionar(
                    'NUEVO',
                    CAST(:p_id_ente AS varchar),
                    CAST(:p_id_servidor_publico AS smallint)
                )
            """),
            {
                "p_id_ente": data.id_ente,
                "p_id_servidor_publico": data.id_servidor_publico
            }
        ).scalar()

        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando relación ente-servidor: {str(e)}")


# ===============================
# Eliminar relación
# ===============================
@router.delete("/", response_model=int)
def delete_ente_servidor_publico(
    data: schemas.EnteServidorPublicoCreate,
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_ente_servidor_publico_gestionar(
                    'ELIMINAR',
                    CAST(:p_id_ente AS varchar),
                    CAST(:p_id_servidor_publico AS smallint)
                )
            """),
            {
                "p_id_ente": data.id_ente,
                "p_id_servidor_publico": data.id_servidor_publico
            }
        ).scalar()

        db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando relación ente-servidor: {str(e)}")