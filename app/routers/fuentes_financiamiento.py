from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/fuentes-financiamiento",
    tags=["Catálogo Fuentes de Financiamiento"]
)

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
            SELECT id_fuente AS id,
                   descripcion,
                   etiquetado,
                   fondo,
                   id_ramo,
                   ramo,
                   clasificacion
            FROM catalogos.sp_cat_fuente_financiamiento(:p_id, :p_id_ramo)
        """)
        result = db.execute(query, {"p_id": p_id, "p_id_ramo": p_id_ramo}).fetchall()

        # Convertimos las filas en diccionarios manualmente
        fuentes = [
            {
                "id": row[0],
                "descripcion": row[1],
                "etiquetado": row[2],
                "fondo": row[3],
                "id_ramo": row[4],
                "ramo": row[5],
                "clasificacion": row[6],
            }
            for row in result
        ]

        return fuentes

    except Exception as e:
        print("❌ Error al obtener fuentes de financiamiento:", e)
        raise HTTPException(status_code=500, detail=str(e))