from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/sesiones-numeros",
    tags=["Catálogos - Números de Sesión"]
)

# ===========================================================
# 🔹 Consultar números de sesión
# ===========================================================
@router.get("/", response_model=list[dict])
def obtener_numeros_sesion(db: Session = Depends(get_db)):
    """
    Llama al SP catalogos.sp_cat_sesion_numero()
    para obtener los números de sesión disponibles.
    """
    try:
        rows = db.execute(text("SELECT * FROM catalogos.sp_cat_sesion_numero()")).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("❌ Error al obtener números de sesión:", e)
        raise HTTPException(status_code=500, detail="Error al obtener números de sesión")