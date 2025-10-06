# app/routers/servidores_publicos.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/servidores-publicos-ente",
    tags=["Servidores Públicos por Ente"]
)

@router.get("/", response_model=List[Dict[str, Any]])
def get_servidores_publicos(
    p_id: int = Query(-99, description="ID del servidor (-99 para todos)"),
    p_id_ente: str = Query("-99", description="ID del ente (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Consulta servidores públicos asociados a un ente específico.
    - p_id = id del servidor (si quieres filtrar por uno en particular)
    - p_id_ente = id del ente (para obtener los servidores de un ente)
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM catalogos.sp_ente_servidor_publico(:p_id, :p_id_ente)
            """),
            {"p_id": p_id, "p_id_ente": p_id_ente}
        ).fetchall()

        return [dict(row._mapping) for row in result]

    except Exception as e:
        print("❌ Error en /servidores-publicos-ente:", repr(e))
        raise HTTPException(status_code=500, detail="Error interno al obtener servidores públicos por ente")