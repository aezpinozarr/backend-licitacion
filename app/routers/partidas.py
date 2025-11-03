# app/routers/partidas.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/partidas",
    tags=["Catálogo Partidas"]
)

# ============================================================
# 🔹 Obtener partidas (usa el SP catalogos.sp_cat_partida)
# ============================================================
@router.get("/", response_model=List[Dict[str, Any]])
def obtener_partidas(
    p_id: str = Query("-99", description="ID de la partida (-99 para todas)"),
    p_id_capitulo: str = Query("-99", description="ID del capítulo (-99 para todas)"),
    p_tipo: str = Query("-99", description="Tipo de partida (ej. 'PROVEEDURIA', 'SERVICIO', etc.)"),
    db: Session = Depends(get_db)
):
    """
    Llama al SP catalogos.sp_cat_partida() para obtener las partidas registradas.
    Si no se especifican parámetros, devuelve todas.
    """
    try:
        sql = text("""
            SELECT 
                id, 
                descripcion, 
                id_capitulo, 
                capitulo, 
                clasificacion, 
                tipo_gasto, 
                observaciones
            FROM catalogos.sp_cat_partida(:p_id, :p_id_capitulo, :p_tipo)
        """)

        result = db.execute(sql, {
            "p_id": p_id,
            "p_id_capitulo": p_id_capitulo,
            "p_tipo": p_tipo
        }).mappings().all()

        partidas = [dict(row) for row in result]

        if not partidas:
            return []  # ⚠️ Devuelve lista vacía (no error)

        return partidas

    except Exception as e:
        print("❌ Error al obtener partidas:", repr(e))
        raise HTTPException(status_code=500, detail="Error interno al obtener partidas")