from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/tipo-licitacion",
    tags=["Procesos - Tipo de Licitación"]
)

# ===========================================================
# 🔹 Consultar enumeración de tipo de licitación
# ===========================================================
@router.get("/", response_model=list[str])
def obtener_tipos_licitacion(db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_enum_proceso_seguimiento_tipo_licitacion()
    para obtener los valores disponibles.
    """
    try:
        rows = db.execute(text("SELECT * FROM procesos.sp_enum_proceso_seguimiento_tipo_licitacion()")).mappings().all()
        return [r["tipo_licitacion"] for r in rows]
    except Exception as e:
        print("❌ Error al obtener tipos de licitación:", e)
        raise HTTPException(status_code=500, detail="Error al obtener tipos de licitación")