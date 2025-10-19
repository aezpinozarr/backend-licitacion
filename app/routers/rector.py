from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(prefix="/rector", tags=["rector"])


# ===========================
# Actualizar seguimiento rector (usa el SP sp_seguimiento_rector_captura)
# ===========================
@router.put("/{id}", response_model=int)
def update_rector(id: int, data: schemas.RectorCaptura, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT procesos.sp_seguimiento_rector_captura(
                    :p_accion,
                    :p_id,
                    :p_r_suplencia_oficio_no,
                    CAST(:p_r_fecha_emision AS date),
                    :p_r_asunto,
                    CAST(:p_r_fecha_y_hora_reunion AS timestamp),
                    :p_r_estatus,
                    :p_r_id_usuario_registra,
                    CAST(:p_r_id_servidor_publico_asiste AS smallint)
                ) AS result
            """),
            {
                "p_accion": data.p_accion,
                "p_id": id,
                "p_r_suplencia_oficio_no": data.p_r_suplencia_oficio_no,
                "p_r_fecha_emision": data.p_r_fecha_emision,
                "p_r_asunto": data.p_r_asunto,
                "p_r_fecha_y_hora_reunion": data.p_r_fecha_y_hora_reunion,
                "p_r_estatus": data.p_r_estatus,
                "p_r_id_usuario_registra": data.p_r_id_usuario_registra,
                "p_r_id_servidor_publico_asiste": data.p_r_id_servidor_publico_asiste,
            }
        ).fetchone()

        db.commit()

        if not result or result.result == 0:
            raise HTTPException(
                status_code=404,
                detail="Registro no encontrado o no se actualizó correctamente."
            )

        return result.result

    except Exception as e:
        db.rollback()
        print("❌ Error en update_rector:", str(e))
        raise HTTPException(status_code=500, detail=str(e))



# ===========================
# Obtener seguimiento rector por ID (verifica los cambios)
# ===========================
@router.get("/{id}", response_model=dict)
def get_rector(id: int, db: Session = Depends(get_db)):
    """
    Retorna los datos actualizados del seguimiento rector.
    """
    try:
        result = db.execute(
            text("""
                SELECT
                    s.id,
                    s.r_suplencia_oficio_no,
                    s.r_fecha_emision,
                    s.r_asunto,
                    s.r_fecha_y_hora_reunion,
                    s.r_estatus,
                    s.r_id_usuario_registra,
                    s.r_id_servidor_publico_asiste,
                    u.nombre AS usuario_registra_nombre,
                    sp.nombre AS servidor_publico_asiste_nombre
                FROM procesos.seguimiento s
                LEFT JOIN seguridad.usuarios u ON u.id = s.r_id_usuario_registra
                LEFT JOIN catalogos.cat_servidor_publico sp ON sp.id = s.r_id_servidor_publico_asiste
                WHERE s.id = :p_id
            """),
            {"p_id": id}
        ).mappings().first()

        if not result:
            raise HTTPException(status_code=404, detail="Registro no encontrado.")

        return dict(result)

    except Exception as e:
        print("❌ Error en get_rector:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    


# ===========================
# Listar todos los seguimientos para el rector
# ===========================
@router.get("/", response_model=list[dict])
def listar_seguimientos_rector(
    p_id: int = -99,
    p_id_ente: str = "-99",
    db: Session = Depends(get_db)
):
    """
    Devuelve todos los seguimientos registrados (usa el SP sp_seguimiento_rector_listar).
    El rector puede filtrar opcionalmente por ID o por ente.
    """
    try:
        result = db.execute(
            text("""
                SELECT *
                FROM procesos.sp_seguimiento_rector_listar(:p_id, :p_id_ente)
            """),
            {"p_id": p_id, "p_id_ente": p_id_ente}
        ).mappings().all()

        if not result:
            return []

        return [dict(row) for row in result]

    except Exception as e:
        print("❌ Error en listar_seguimientos_rector:", str(e))
        raise HTTPException(status_code=500, detail=str(e))