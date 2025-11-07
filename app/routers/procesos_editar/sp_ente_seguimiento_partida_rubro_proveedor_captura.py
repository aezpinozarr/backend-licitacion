from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import EnteSeguimientoPartidaRubroProveedorUpdate

router = APIRouter(
    prefix="/procesos/editar",
    tags=["Editar - Seguimiento (Paso 4)"]
)

@router.put("/ente-seguimiento-partida-rubro-proveedor-captura", response_model=int)
def update_ente_seguimiento_partida_rubro_proveedor_captura(
    payload: EnteSeguimientoPartidaRubroProveedorUpdate,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_rubro_proveedor_captura
    para agregar o eliminar proveedores (Paso 4 del proceso).
    """
    try:
        sql = text("""
            SELECT procesos.sp_ente_seguimiento_partida_rubro_proveedor_captura(
                :p_accion,
                :p_id_seguimiento_partida_rubro,
                :p_id,
                :p_e_rfc_proveedor,
                :p_e_importe_sin_iva,
                :p_e_importe_total
            ) AS result
        """)

        result = db.execute(sql, {
            "p_accion": payload.p_accion.upper(),
            "p_id_seguimiento_partida_rubro": payload.p_id_seguimiento_partida_rubro,
            "p_id": payload.p_id,
            "p_e_rfc_proveedor": payload.p_e_rfc_proveedor,
            "p_e_importe_sin_iva": payload.p_e_importe_sin_iva,
            "p_e_importe_total": payload.p_e_importe_total
        }).scalar()

        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No se pudo realizar la operación sobre el proveedor.")

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en /procesos/editar/ente-seguimiento-partida-rubro-proveedor-captura:", str(e))
        raise HTTPException(status_code=500, detail=str(e))