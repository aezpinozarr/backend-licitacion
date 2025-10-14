from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/presupuesto-proveedor",
    tags=["Proceso Seguimiento - Presupuesto Proveedor"]
)

# ===========================================================
# 🔹 Crear o editar proveedor asociado al presupuesto del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_presupuesto_proveedor(data: schemas.ProcesoPresupuestoProveedorIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_proceso_seguimiento_presupuesto_proveedor_ente_captura
    para crear o editar los importes del proveedor.
    """
    try:
        # ⚙️ Actualizado: el parámetro ahora se llama p_id_proceso_seguimiento_presupuesto
        query = text("""
            SELECT procesos.sp_proceso_seguimiento_presupuesto_proveedor_ente_captura(
                :p_accion,
                :p_id_proceso_seguimiento_presupuesto,
                :p_e_rfc_proveedor,
                :p_e_importe_sin_iva,
                :p_e_importe_total
            )
        """)

        # ⚙️ Cambiado el nombre del parámetro en el dict
        params = {
            "p_accion": data.p_accion,
            "p_id_proceso_seguimiento_presupuesto": data.p_id_proceso_seguimiento_presupuesto,
            "p_e_rfc_proveedor": data.p_e_rfc_proveedor,
            "p_e_importe_sin_iva": data.p_e_importe_sin_iva,
            "p_e_importe_total": data.p_e_importe_total
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el proveedor del presupuesto")

        return {"resultado": result, "mensaje": "✅ Proveedor asociado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar proveedor del presupuesto:", e)
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/presupuesto-proveedor",
    tags=["Proceso Seguimiento - Presupuesto Proveedor"]
)

# ===========================================================
# 🔹 Crear o editar proveedor asociado al presupuesto del rubro-ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_presupuesto_proveedor(data: schemas.ProcesoPresupuestoProveedorIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_presupuesto_rubro_proveedor_ente_captura
    para crear o editar los importes del proveedor asociados a un rubro.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_presupuesto_rubro_proveedor_ente_captura(
                :p_accion,
                :p_id_proceso_seguimiento_presupuesto_rubro,
                :p_id,
                :p_e_rfc_proveedor,
                :p_e_importe_sin_iva,
                :p_e_importe_total,
                :p_r_importe_ajustado_sin_iva,
                :p_r_importe_ajustado_total
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_proceso_seguimiento_presupuesto_rubro": getattr(data, "p_id_proceso_seguimiento_presupuesto_rubro", 0),
            "p_id": getattr(data, "p_id", 0),
            "p_e_rfc_proveedor": data.p_e_rfc_proveedor,
            "p_e_importe_sin_iva": data.p_e_importe_sin_iva,
            "p_e_importe_total": data.p_e_importe_total,
            "p_r_importe_ajustado_sin_iva": getattr(data, "p_r_importe_ajustado_sin_iva", 0),
            "p_r_importe_ajustado_total": getattr(data, "p_r_importe_ajustado_total", 0),
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el proveedor del presupuesto de rubro")

        return {"resultado": result, "mensaje": "✅ Proveedor de rubro asociado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar proveedor del presupuesto de rubro:", e)
        raise HTTPException(status_code=500, detail=str(e))