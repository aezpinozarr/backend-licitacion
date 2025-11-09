from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/rector/seguimiento-gestion-estatus",
    tags=["sp_rector_seguimiento_gestion_estatus"]
)

@router.put("/{id}", response_model=int)
def update_rector_estatus(id: int, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_rector_seguimiento_gestion_estatus para actualizar
    el estatus del seguimiento del rector a 'REVISADO' al finalizar el proceso.
    """
    try:
        result = db.execute(text("""
            SELECT procesos.sp_rector_seguimiento_gestion_estatus(:p_id)
        """), {"p_id": id}).scalar()

        db.commit()

        if result is None:
            raise HTTPException(
                status_code=400,
                detail="No se pudo ejecutar el procedimiento correctamente"
            )

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en sp_rector_seguimiento_gestion_estatus:", str(e))
        raise HTTPException(status_code=500, detail=str(e))