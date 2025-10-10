# app/routers/presupuesto_proveedor.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/seguimiento",
    tags=["Procesos Seguimiento"]
)

# ===========================
# ✅ Obtener datos de la vista v_proceso_seguimiento_presupuesto_proveedor
# ===========================
@router.get("/presupuesto-proveedor/")
def get_presupuesto_proveedor(
    p_id_proceso: int = Query(..., description="ID del proceso seguimiento"),
    db: Session = Depends(get_db)
):
    """
    Devuelve información consolidada de la vista v_proceso_seguimiento_presupuesto_proveedor.
    Incluye datos del ente, presupuesto y proveedor asociados al proceso.
    """
    try:
        # ✅ CORREGIDO: usamos "id" en lugar de "id_proceso_seguimiento"
        query = text("""
            SELECT *
            FROM procesos.v_proceso_seguimiento_presupuesto_proveedor
            WHERE id = :p_id_proceso
            ORDER BY pp_id;
        """)

        result = db.execute(query, {"p_id_proceso": p_id_proceso}).fetchall()

        # ✅ Si no hay datos, devolvemos lista vacía (no error)
        if not result:
            return {
                "status": "ok",
                "resultado": []
            }

        return {
            "status": "ok",
            "resultado": [dict(row._mapping) for row in result],
        }

    except Exception as e:
        print(f"❌ Error en get_presupuesto_proveedor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# 🧾 Listar todos los registros (para reportes o debugging)
# ===========================
@router.get("/presupuesto-proveedor/all")
def list_presupuestos_proveedor(db: Session = Depends(get_db)):
    """
    Devuelve todos los registros disponibles en la vista
    v_proceso_seguimiento_presupuesto_proveedor.
    Ideal para listados generales o reportes.
    """
    try:
        query = text("""
            SELECT *
            FROM procesos.v_proceso_seguimiento_presupuesto_proveedor
            ORDER BY id DESC;
        """)
        result = db.execute(query).fetchall()

        return {
            "status": "ok",
            "total": len(result),
            "resultado": [dict(row._mapping) for row in result],
        }

    except Exception as e:
        print(f"❌ Error en list_presupuestos_proveedor: {e}")
        raise HTTPException(status_code=500, detail=str(e))