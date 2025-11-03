from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/ente-seguimiento",
    tags=["sp_ente_seguimiento"]
)

@router.get("/")
def ejecutar_sp_ente_seguimiento(
    p_id: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db)
):
    """
    🔹 Ejecuta el SP procesos.sp_ente_seguimiento para obtener los seguimientos de un ENTE.

    Parámetros:
    - p_id: ID específico del seguimiento (o -99 para traer todos)
    - p_id_ente: ID del ente (o -99 para traer todos)

    Ejemplos:
    - /procesos/ente-seguimiento?p_id_ente=1103
    - /procesos/ente-seguimiento?p_id=245
    """
    try:
        query = text("""
            SELECT * FROM procesos.sp_ente_seguimiento(:p_id, :p_id_ente);
        """)

        result = db.execute(query, {
            "p_id": p_id,
            "p_id_ente": p_id_ente
        }).mappings().all()

        if not result:
            return []

        # Convertimos a lista de dicts (para serializar correctamente en JSON)
        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error al ejecutar SP procesos.sp_ente_seguimiento:", str(e))
        raise HTTPException(status_code=500, detail=f"Error al obtener seguimientos: {str(e)}")