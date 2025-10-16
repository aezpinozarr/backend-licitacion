from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/seguimiento/partida-rubro-proveedor-ente",
    tags=["Vista Seguimiento Partida Rubro Proveedor Ente"]
)

# ===========================================================
# 🔹 Obtener todos los registros
# ===========================================================
@router.get("/all")
def obtener_todos(db: Session = Depends(get_db)):
    """
    Devuelve todos los registros de la vista unificada que relaciona
    seguimiento, partida, rubro y proveedor.
    """
    try:
        query = text("""
            SELECT *
            FROM procesos.v_seguimiento_y_partida_y_rubro_y_proveedor
        """)
        result = db.execute(query).mappings().all()
        return {"resultado": result}
    except Exception as e:
        print("❌ Error al obtener todos:", e)
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# 🔹 Obtener registros por ente
# ===========================================================
@router.get("/by-ente")
def obtener_por_ente(p_id_ente: str, db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT *
            FROM procesos.v_seguimiento_y_partida_y_rubro_y_proveedor
            WHERE e_id_ente::text = :p_id_ente
        """)
        rows = db.execute(query, {"p_id_ente": str(p_id_ente)}).mappings().all()

        # Renombrar campos para que coincidan con el frontend
        resultado = []
        for row in rows:
            data = dict(row)
            data["id_proceso_seguimiento"] = data.get("id")
            data["estatus"] = data.get("r_estatus")
            resultado.append(data)

        return {"resultado": resultado}

    except Exception as e:
        print("❌ Error al obtener por ente:", e)
        raise HTTPException(status_code=500, detail=str(e))