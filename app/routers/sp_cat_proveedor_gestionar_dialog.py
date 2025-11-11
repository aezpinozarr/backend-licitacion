from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.schemas import ProveedorDialogCreate

router = APIRouter(
    prefix="/catalogos",
    tags=["Catálogo de Proveedores (Dialog)"]
)

@router.post("/sp_cat_proveedor_gestionar_dialog")
def sp_cat_proveedor_gestionar_dialog(
    payload: ProveedorDialogCreate,
    db: Session = Depends(get_db)
):
    """
    Llama al SP catalogos.sp_cat_proveedor_gestionar_dialog para crear
    o validar un proveedor desde el diálogo del Paso 4.
    Retorna el JSON generado por el SP.
    """
    try:
        sql = text("""
    SELECT catalogos.sp_cat_proveedor_gestionar_dialog(
        :p_rfc,
        :p_razon_social,
        :p_nombre_comercial,
        :p_persona_juridica,
        :p_correo_electronico,
        CAST(:p_id_entidad_federativa AS smallint)
    ) AS result
""")

        result = db.execute(sql, {
            "p_rfc": payload.p_rfc,
            "p_razon_social": payload.p_razon_social,
            "p_nombre_comercial": payload.p_nombre_comercial,
            "p_persona_juridica": payload.p_persona_juridica,
            "p_correo_electronico": payload.p_correo_electronico,
            "p_id_entidad_federativa": payload.p_id_entidad_federativa
        }).scalar()

        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se obtuvo respuesta del procedimiento almacenado.")

        return result  # El SP devuelve un objeto JSON

    except Exception as e:
        db.rollback()
        print("❌ Error en /catalogos/sp_cat_proveedor_gestionar_dialog:", str(e))
        raise HTTPException(status_code=500, detail=str(e))