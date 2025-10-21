from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import ProveedorRubroRequest

router = APIRouter(
    prefix="/procesos/seguimiento/partida-rubro-proveedor-ente-v2",
    tags=["Procesos - Partida Rubro Proveedor V2"]
)

# ============================================================
# 🔹 Ejecutar SP procesos.sp_seguimiento_partida_rubro_proveedor_ente_capturav2
# ============================================================
@router.post("/")
def ejecutar_sp_proveedor_rubro_v2(req: ProveedorRubroRequest, db: Session = Depends(get_db)):
    """
    Ejecuta el SP para añadir o eliminar proveedores en la tabla seguimiento_partida_rubro_proveedor.
    Usa psycopg2 síncrono (vía Session.execute).
    """
    try:
        query = text("""
            SELECT procesos.sp_ente_seguimiento_partida_rubro_proveedor_captura(
                :p_accion,
                :p_id_seguimiento_partida_rubro,
                :p_id,
                :p_e_rfc_proveedor,
                :p_e_importe_sin_iva,
                :p_e_importe_total
            ) AS resultado
        """)
        result = db.execute(query, req.dict()).mappings().first()
        db.commit()

        return {"resultado": result["resultado"] if result else 0}

    except Exception as e:
        print("❌ Error al ejecutar SP (proveedor rubro v2):", e)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))