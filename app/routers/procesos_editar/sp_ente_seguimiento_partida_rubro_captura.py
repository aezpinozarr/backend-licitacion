from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import EnteSeguimientoPartidaRubroUpdate

router = APIRouter(
    prefix="/procesos/editar",
    tags=["Editar - Seguimiento (Paso 3)"]
)

@router.put("/ente-seguimiento-partida-rubro-captura", response_model=int)
def update_ente_seguimiento_partida_rubro_captura(
    payload: EnteSeguimientoPartidaRubroUpdate,
    db: Session = Depends(get_db)
):
    """
    Llama al SP procesos.sp_ente_seguimiento_partida_rubro_captura
    para agregar o eliminar rubros (Paso 3 del proceso).
    """
    try:
        sql = text("""
            SELECT procesos.sp_ente_seguimiento_partida_rubro_captura(
                :p_accion,
                :p_id_seguimiento_partida,
                :p_id,
                :p_e_id_rubro,
                :p_e_monto_presupuesto_suficiencia
            ) AS result
        """)

        result = db.execute(sql, {
            "p_accion": payload.p_accion.upper(),
            "p_id_seguimiento_partida": payload.p_id_seguimiento_partida,
            "p_id": payload.p_id,
            "p_e_id_rubro": payload.p_e_id_rubro,
            "p_e_monto_presupuesto_suficiencia": payload.p_e_monto_presupuesto_suficiencia
        }).scalar()

        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No se pudo realizar la operación sobre el rubro.")

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en /procesos/editar/ente-seguimiento-partida-rubro-captura:", str(e))
        raise HTTPException(status_code=500, detail=str(e))