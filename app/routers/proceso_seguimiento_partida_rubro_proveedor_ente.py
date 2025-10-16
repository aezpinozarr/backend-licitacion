from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/partida-rubro-proveedor-ente",
    tags=["Proceso Seguimiento - Partida Rubro Proveedor Ente"]
)

# ===========================================================
# 🔹 Crear o editar proveedor asociado a rubro de partida
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_partida_rubro_proveedor(data: schemas.ProcesoPartidaRubroProveedorEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_partida_rubro_proveedor_ente_captura
    para crear o editar un proveedor asociado a un rubro dentro de una partida.
    """
    try:
        if not data.p_id_seguimiento_partida:
            raise HTTPException(status_code=400, detail="Debe enviarse un ID de rubro válido")

        query = text("""
            SELECT procesos.sp_seguimiento_partida_rubro_proveedor_ente_captura(
                :p_accion,
                :p_id_seguimiento_partida,
                :p_id,
                :p_e_rfc_proveedor,
                :p_e_importe_sin_iva,
                :p_e_importe_total
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_seguimiento_partida": data.p_id_seguimiento_partida,
            "p_id": getattr(data, "p_id", 0),
            "p_e_rfc_proveedor": data.p_e_rfc_proveedor,
            "p_e_importe_sin_iva": data.p_e_importe_sin_iva,
            "p_e_importe_total": data.p_e_importe_total
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el proveedor del rubro")

        return {"resultado": result, "mensaje": "✅ Proveedor asociado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar proveedor del rubro:", e)
        raise HTTPException(status_code=500, detail=str(e))