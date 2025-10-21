from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/rector/seguimiento-gestion",
    tags=["sp_rector_seguimiento_gestion"]
)

@router.put("/{id}", response_model=int)
def update_rector(id: int, data: schemas.RectorGestionIn, db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_rector_seguimiento_gestion para actualizar
    los datos del seguimiento del rector, incluyendo observaciones.
    """
    try:
        result = db.execute(text("""
            SELECT procesos.sp_rector_seguimiento_gestion(
                :p_accion, :p_id, :p_r_suplencia_oficio_no, :p_r_fecha_emision, :p_r_asunto,
                :p_r_fecha_y_hora_reunion, :p_r_estatus, :p_r_id_usuario_registra,
                CAST(:p_r_id_servidor_publico_asiste AS smallint),
                :p_r_observaciones, :p_r_con_observaciones
            )
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
                "p_r_observaciones": data.p_r_observaciones,
                "p_r_con_observaciones": data.p_r_con_observaciones
            }
        ).scalar()

        db.commit()

        if result is None:
            raise HTTPException(status_code=400, detail="No se pudo ejecutar el procedimiento correctamente")

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en sp_rector_seguimiento_gestion:", str(e))
        raise HTTPException(status_code=500, detail=str(e))