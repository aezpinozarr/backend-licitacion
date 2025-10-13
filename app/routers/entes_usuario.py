from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/ente-usuario",
    tags=["Catálogos - Ente del Usuario"]
)

# ===========================================================
# 🔹 Obtener la descripción del ente de un usuario logeado
# ===========================================================
@router.get("/", response_model=dict)
def obtener_ente_usuario(
    p_id_ente: str = Query(..., description="ID del ente del usuario logeado"),
    db: Session = Depends(get_db)
):
    """
    Devuelve la descripción del ente asociado al usuario logeado.
    Llama al SP catalogos.sp_cat_ente(p_id_ente)
    """
    try:
        query = text("SELECT * FROM catalogos.sp_cat_ente(:p_id)")
        result = db.execute(query, {"p_id": p_id_ente}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="No se encontró el ente")

        # Mapea columnas: (id, descripcion)
        return {"id_ente": result[0], "descripcion": result[1]}

    except Exception as e:
        print("❌ Error obteniendo ente del usuario:", e)
        raise HTTPException(status_code=500, detail=str(e))