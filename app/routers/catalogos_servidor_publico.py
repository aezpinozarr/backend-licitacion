from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/servidores-publicos",
    tags=["Catálogos - Servidores Públicos"]
)

# ===========================================================
# 🔹 Consultar servidores públicos del ente actual
# ===========================================================
@router.get("/", response_model=list[dict])
def obtener_servidores_publicos(id_ente: str, db: Session = Depends(get_db)):
    """
    Llama al SP catalogos.sp_servidor_publico_ente(:p_id_ente)
    para obtener los servidores públicos asociados al ente.
    """
    try:
        query = text("SELECT * FROM catalogos.sp_servidor_publico_ente(:p_id_ente)")
        rows = db.execute(query, {"p_id_ente": id_ente}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        print("❌ Error al obtener servidores públicos:", e)
        raise HTTPException(status_code=500, detail="Error al obtener servidores públicos")