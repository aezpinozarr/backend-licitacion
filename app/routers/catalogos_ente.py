from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/entes",
    tags=["Catálogos - Entes"]
)

# ===========================================================
# 🔹 Consultar ente (solo el del usuario logeado)
# ===========================================================
@router.get("/", response_model=list[dict])
def obtener_ente_por_usuario(id_ente: str, db: Session = Depends(get_db)):
    """
    Llama al SP catalogos.sp_cat_ente para obtener la información
    del ente asociado al usuario logeado.
    """
    try:
        query = text("SELECT * FROM catalogos.sp_cat_ente(:p_id_ente)")
        rows = db.execute(query, {"p_id_ente": id_ente}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("❌ Error al obtener ente:", e)
        raise HTTPException(status_code=500, detail="Error al obtener ente")