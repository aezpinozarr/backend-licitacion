from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/fuentes-financiamiento",
    tags=["Catálogo Fuentes de Financiamiento"]
)

# ============================================================
# 🔹 Obtener fuentes de financiamiento (usa el SP)
# ============================================================
@router.get("/")
def obtener_fuentes_financiamiento(
    p_id: str = Query("-99", description="ID de la fuente (-99 para todas)"),
    p_id_ramo: str = Query("-99", description="ID del ramo (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP catalogos.sp_cat_fuente_financiamiento() 
    para obtener las fuentes de financiamiento disponibles.
    """
    try:
        query = text("""
            SELECT * 
            FROM catalogos.sp_cat_fuente_financiamiento(:p_id, :p_id_ramo)
        """)
        result = db.execute(query, {"p_id": p_id, "p_id_ramo": p_id_ramo}).mappings().all()
        fuentes = [dict(row) for row in result]
        return fuentes

    except Exception as e:
        print("❌ Error al obtener fuentes de financiamiento:", e)
        raise HTTPException(status_code=500, detail=str(e))