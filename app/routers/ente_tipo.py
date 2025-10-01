# app/routers/ente_tipo.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.db import get_db

router = APIRouter(prefix="/catalogos/ente-tipo", tags=["Ente Tipo"])

@router.get("/", response_model=List[dict])
def get_ente_tipo(p_id: str = "-99", db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_ente_tipo(:p_id)"),
            {"p_id": p_id}
        ).fetchall()

        # ✅ convertir correctamente a dict usando _mapping
        return [dict(row._mapping) for row in result]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))