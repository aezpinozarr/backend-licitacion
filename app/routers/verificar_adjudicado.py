from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/rector",
    tags=["verificar_adjudicado"]
)

@router.get("/verificar-adjudicado")
def verificar_adjudicado(p_id_rubro_proveedor: int, db: Session = Depends(get_db)):
    """
    Verifica si ya existe un registro adjudicado en la tabla
    procesos.seguimiento_partida_rubro_proveedor_adjudicado
    asociado al id del rubro_proveedor especificado.
    Devuelve el id del adjudicado si existe.
    """
    try:
        query = text("""
            SELECT id
            FROM procesos.seguimiento_partida_rubro_proveedor_adjudicado
            WHERE id_seguimiento_partida_rubro_proveedor = :p_id_rubro_proveedor
            LIMIT 1
        """)
        result = db.execute(query, {"p_id_rubro_proveedor": p_id_rubro_proveedor}).fetchone()

        if result:
            return {"id": result[0]}
        else:
            return {"id": None}

    except Exception as e:
        print("❌ Error en verificar_adjudicado:", str(e))
        raise HTTPException(status_code=500, detail=str(e))