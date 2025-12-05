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
def deshacer_adjudicacion(payload: DeshacerAdjudicacionRequest, db: Session = Depends(get_db)):

    try:
        query = text("""
            SELECT * 
            FROM procesos.sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer(
                :p_id_seguimiento_partida_rubro,
                :p_id_proveedor
            )
        """)

        result = db.execute(query, {
            "p_id_seguimiento_partida_rubro": payload.p_id_seguimiento_partida_rubro,
            "p_id_proveedor": payload.p_id_proveedor
        }).mappings().all()

        db.commit()

        if result and len(result) > 0:
            return DeshacerAdjudicacionResponse(resultado=1)
        else:
            return DeshacerAdjudicacionResponse(resultado=0)

    except Exception as e:
        print("❌ Error en deshacer adjudicacion:", str(e))
        raise HTTPException(status_code=500, detail=str(e))