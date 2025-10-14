# app/routers/proceso_seguimiento_presupuesto.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/procesos/seguimiento/presupuesto-ente",
    tags=["Proceso Seguimiento - Presupuesto Ente"]
)

@router.get("/")
def obtener_presupuesto_ente(
    p_id_proceso_seguimiento: int,
    p_e_id_partida: str,
    db: Session = Depends(get_db)
):
    """
    Obtiene los registros existentes de la tabla procesos.seguimiento_presupuesto
    filtrando por id_proceso_seguimiento y e_id_partida.
    """
    try:
        query = text("""
            SELECT id, id_proceso_seguimiento, e_id_partida, e_monto_presupuesto_suficiencia
            FROM procesos.seguimiento_presupuesto
            WHERE id_proceso_seguimiento = :p_id_proceso_seguimiento
              AND e_id_partida = :p_e_id_partida
        """)
        result = db.execute(query, {
            "p_id_proceso_seguimiento": p_id_proceso_seguimiento,
            "p_e_id_partida": p_e_id_partida
        }).mappings().all()

        return result if result else []
    except Exception as e:
        print("❌ Error al obtener presupuesto de ente:", e)
        raise HTTPException(status_code=500, detail=str(e))

# ===========================================================
# 🔹 Crear o editar presupuesto del ente
# ===========================================================
@router.post("/", response_model=dict)
def gestionar_presupuesto_ente(data: schemas.ProcesoPresupuestoEnteIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_seguimiento_presupuesto_ente_captura
    para crear o editar la información presupuestal del ente.
    """
    try:
        query = text("""
            SELECT procesos.sp_seguimiento_presupuesto_ente_captura(
                :p_accion,
                :p_id_proceso_seguimiento,
                :p_id,
                :p_e_no_requisicion,
                :p_e_id_partida,
                :p_e_id_fuente_financiamiento,
                :p_e_monto_presupuesto_suficiencia
            )
        """)

        params = {
            "p_accion": data.p_accion,
            "p_id_proceso_seguimiento": data.p_id_proceso_seguimiento,
            "p_id": data.p_id,
            "p_e_no_requisicion": data.p_e_no_requisicion,
            "p_e_id_partida": data.p_e_id_partida,
            "p_e_id_fuente_financiamiento": data.p_e_id_fuente_financiamiento,
            "p_e_monto_presupuesto_suficiencia": data.p_e_monto_presupuesto_suficiencia,
        }

        result = db.execute(query, params).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo registrar el presupuesto del ente")

        return {"resultado": result, "mensaje": "✅ Presupuesto registrado correctamente"}

    except Exception as e:
        print("❌ Error al gestionar presupuesto de ente:", e)
        raise HTTPException(status_code=500, detail=str(e))
    

# ===========================================================
# 🔹 Obtener presupuestos registrados del ente por proceso
# ===========================================================
@router.get("/", response_model=list[dict])
def obtener_presupuestos_ente(
    p_id_proceso_seguimiento: int,
    p_e_id_partida: int = -99,
    db: Session = Depends(get_db)
):
    """
    Consulta los registros de presupuesto del ente.
    Si p_e_id_partida = -99 → devuelve todas las partidas del proceso.
    Si se especifica una partida, devuelve solo esa.
    """
    try:
        if p_e_id_partida == -99:
            query = text("""
                SELECT 
                    id,
                    id_proceso_seguimiento,
                    e_no_requisicion,
                    e_id_partida,
                    e_id_fuente_financiamiento,
                    e_monto_presupuesto_suficiencia,
                    r_estatus
                FROM procesos.seguimiento_presupuesto
                WHERE id_proceso_seguimiento = :p_id_proceso_seguimiento
            """)
            result = db.execute(query, {"p_id_proceso_seguimiento": p_id_proceso_seguimiento})
        else:
            query = text("""
                SELECT 
                    id,
                    id_proceso_seguimiento,
                    e_no_requisicion,
                    e_id_partida,
                    e_id_fuente_financiamiento,
                    e_monto_presupuesto_suficiencia,
                    r_estatus
                FROM procesos.seguimiento_presupuesto
                WHERE id_proceso_seguimiento = :p_id_proceso_seguimiento
                AND e_id_partida = :p_e_id_partida
            """)
            result = db.execute(query, {
                "p_id_proceso_seguimiento": p_id_proceso_seguimiento,
                "p_e_id_partida": p_e_id_partida
            })

        rows = [dict(row._mapping) for row in result]
        return rows

    except Exception as e:
        print("❌ Error al obtener presupuestos del ente:", e)
        raise HTTPException(status_code=500, detail=str(e))