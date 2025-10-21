from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/cat-fundamiento",
    tags=["sp_cat_fundamiento"]
)

@router.get("/", response_model=list[dict])
def listar_fundamento(p_id: str = "-99", db: Session = Depends(get_db)):
    """
    Llama al SP catalogos.sp_cat_fundamiento para listar los fundamentos
    disponibles. Si se pasa un p_id, devuelve solo el registro correspondiente.
    """
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_fundamiento(:p_id)"),
            {"p_id": p_id}
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en sp_cat_fundamiento:", str(e))
        raise HTTPException(status_code=500, detail=str(e))