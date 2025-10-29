from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import DeshacerAdjudicacionRequest, DeshacerAdjudicacionResponse

router = APIRouter(
    prefix="/rector/seg-partida-rubro-proveedor-deshacer",
    tags=["sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer"]
)

@router.post("/", response_model=DeshacerAdjudicacionResponse)
def deshacer_adjudicacion(
    payload: DeshacerAdjudicacionRequest,
    db: Session = Depends(get_db),
):
    """
    Llama al SP procesos.sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer(p_id)
    para revertir una adjudicación de proveedor.
    Retorna 1 si se deshizo correctamente, 0 si no se quitó nada.
    """
    try:
        query = text("SELECT * FROM procesos.sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer(:p_id)")
        result = db.execute(query, {"p_id": payload.p_id}).mappings().all()
        db.commit()

        # Si el SP devolvió registros, consideramos éxito (1)
        if result and len(result) > 0:
            return DeshacerAdjudicacionResponse(resultado=1)
        else:
            return DeshacerAdjudicacionResponse(resultado=0)

    except Exception as e:
        print("❌ Error en sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer:", str(e))
        raise HTTPException(status_code=500, detail=str(e))