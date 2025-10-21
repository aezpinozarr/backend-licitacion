from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/enum-seguimiento-partida-rubro-estatus",
    tags=["sp_enum_seguimiento_partida_rubro_estatus"]
)

@router.get("/", response_model=list[dict])
def listar_estatus(db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_enum_seguimiento_partida_rubro_estatus
    para obtener la lista de estatus definidos en el ENUM
    procesos.enum_seguimiento_partida_rubro_estatus.
    """
    try:
        result = db.execute(
            text("SELECT * FROM procesos.sp_enum_seguimiento_partida_rubro_estatus()")
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en sp_enum_seguimiento_partida_rubro_estatus:", str(e))
        raise HTTPException(status_code=500, detail=str(e))