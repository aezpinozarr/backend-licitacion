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
    

# ===========================================================
# 🔹 Obtener TODOS los servidores públicos (asociados o no)
# ===========================================================
@router.get("/todos", response_model=List[Dict[str, Any]])
def get_servidores_todos(db: Session = Depends(get_db)):
    """
    Devuelve todos los servidores públicos, estén o no asociados a un ente.
    Usa LEFT JOIN para incluir los que no tienen relación en ente_servidor_publico.
    """
    try:
        query = text("""
            SELECT 
                s.id,
                s.nombre,
                s.cargo,
                s.activo,
                e.id AS id_ente,
                e.descripcion AS ente_publico,
                e.siglas AS ente_siglas,
                e.clasificacion AS ente_clasificacion
            FROM catalogos.cat_servidor_publico s
            LEFT JOIN catalogos.ente_servidor_publico es
                ON s.id = es.id_servidor_publico
            LEFT JOIN catalogos.cat_ente e
                ON e.id = es.id_ente
            ORDER BY s.id;
        """)
        result = db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    except Exception as e:
        print("❌ Error en /catalogos/servidores-publicos-ente/todos:", repr(e))
        raise HTTPException(status_code=500, detail="Error al obtener todos los servidores públicos")