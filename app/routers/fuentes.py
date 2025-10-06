from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.db import get_db
from app.schemas import FuenteFinanciamiento

router = APIRouter(
    prefix="/catalogos/fuentes-financiamiento",
    tags=["Fuentes de financiamiento"]
)

@router.get("/", response_model=List[FuenteFinanciamiento])
def list_fuentes(db: Session = Depends(get_db)):
    """
    Devuelve todas las fuentes de financiamiento con su estado de etiquetado
    """
    try:
        result = db.execute(
            text("""
                SELECT id, descripcion, etiquetado
                FROM catalogos.cat_fuente_financiamiento
                ORDER BY id
            """)
        ).mappings().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando fuentes: {str(e)}")