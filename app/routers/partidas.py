from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/partidas",
    tags=["Catálogo Partidas"]
)

# ============================================================
# 🔹 Obtener partidas (usa el SP catalogos.sp_cat_partida)
# ============================================================
@router.get("/")
def obtener_partidas(
    p_id: str = Query("-99", description="ID de la partida (-99 para todas)"),
    p_id_capitulo: str = Query("-99", description="ID del capítulo (-99 para todas)"),
    p_tipo: str = Query("-99", description="Tipo de partida (ej. 'PROVEEDURIA')"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP catalogos.sp_cat_partida() para obtener las partidas registradas.
    Si p_id = -99 devuelve todas.
    """
    try:
        query = text("""
            SELECT * FROM catalogos.sp_cat_partida(:p_id, :p_id_capitulo, :p_tipo)
        """)
        result = db.execute(
            query,
            {"p_id": p_id, "p_id_capitulo": p_id_capitulo, "p_tipo": p_tipo}
        ).mappings().all()

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error al obtener partidas:", e)
        raise HTTPException(status_code=500, detail=str(e))