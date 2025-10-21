from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/rector/seguimiento-gestion-proveedor-adjudicado",
    tags=["sp_rector_seguimiento_gestion_proveedor_adjudicado"]
)

@router.post("/", response_model=int)
def ejecutar_sp_rector_seguimiento_gestion_proveedor_adjudicado(
    data: schemas.SpRectorSeguimientoGestionProveedorAdjudicado,
    db: Session = Depends(get_db)
):
    """
    Ejecuta el SP procesos.sp_rector_seguimiento_gestion_proveedor_adjudicadov2
    para adjudicar o actualizar un proveedor en función del estatus.
    """
    try:
        query = text("""
            SELECT procesos.sp_rector_seguimiento_gestion_proveedor_adjudicadov2(
                :p_estatus,
                :p_id_seguimiento_partida_rubro,
                :p_id_seguimiento_partida_rubro_proveedor,
                :p_id,
                :p_importe_ajustado_sin_iva,
                :p_importe_ajustado_total,
                :p_id_fundamento
            )
        """)

        result = db.execute(query, {
            "p_estatus": data.p_estatus,
            "p_id_seguimiento_partida_rubro": data.p_id_seguimiento_partida_rubro,
            "p_id_seguimiento_partida_rubro_proveedor": data.p_id_seguimiento_partida_rubro_proveedor,
            "p_id": data.p_id,
            "p_importe_ajustado_sin_iva": data.p_importe_ajustado_sin_iva,
            "p_importe_ajustado_total": data.p_importe_ajustado_total,
            "p_id_fundamento": data.p_id_fundamento
        }).scalar()

        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No se insertó ni actualizó ningún registro")

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error al ejecutar SP:", str(e))
        raise HTTPException(status_code=500, detail=str(e))