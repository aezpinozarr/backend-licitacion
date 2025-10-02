# Ente - Servidor - Público
# app/routers/servidores_publicos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/servidores-publicos-ente",
    tags=["Servidores Públicos por Ente"]
)

@router.get("/", response_model=List[Dict[str, Any]])
def get_servidores_publicos(
    p_id: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Consulta servidores públicos asociados a un ente específico.
    - p_id = id del servidor (si quieres filtrar por uno en particular)
    - p_id_ente = id del ente (para obtener los servidores de un ente)
    """
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_servidor_publico_ente(:p_id, :p_id_ente)"),
            {"p_id": p_id, "p_id_ente": p_id_ente}
        ).fetchall()

        # Convertir cada fila en dict
        return [dict(row._mapping) for row in result]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))