from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/rector/seguimiento-preregistrados",
    tags=["sp_rector_seguimiento_preregistrados"]
)

@router.get("/", response_model=list[dict])
def listar_preregistrados(p_id: int = -99, p_id_ente: str = "-99", db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_rector_seguimiento_preregistrados para listar
    los seguimientos en estado PREREGISTRADO.
    """
    try:
        result = db.execute(
            text("SELECT * FROM procesos.sp_rector_seguimiento_preregistrados(:p_id, :p_id_ente)"),
            {"p_id": p_id, "p_id_ente": p_id_ente}
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en sp_rector_seguimiento_preregistrados:", str(e))
        raise HTTPException(status_code=500, detail=str(e))