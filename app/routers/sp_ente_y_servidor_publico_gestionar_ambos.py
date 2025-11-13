from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas  # ✅ importa tu schema

router = APIRouter(
    prefix="/catalogos",
    tags=["Catálogos - Ente y Servidor Público"]
)

@router.post(
    "/ente-y-servidor-publico-gestionar-ambos",
    response_model=schemas.EnteServidorPublicoResponse  # ✅ usa el schema que creaste
)
def gestionar_ente_y_servidor_publico_ambos(
    p_id_ente: str = Query(..., description="ID del ente"),
    p_nombre: str = Query(..., description="Nombre del servidor público"),
    p_cargo: str = Query(..., description="Cargo del servidor público"),
    db: Session = Depends(get_db)
):
    """
    Llama al procedimiento almacenado catalogos.sp_ente_y_servidor_publico_gestionar_ambos
    para crear o vincular servidores públicos a entes, según las reglas del SP.
    """

    try:
        query = text("""
            SELECT catalogos.sp_ente_y_servidor_publico_gestionar_dialog(
                :p_id_ente, :p_nombre, :p_cargo
            ) AS resultado;
        """)

        result = db.execute(query, {
            "p_id_ente": p_id_ente,
            "p_nombre": p_nombre,
            "p_cargo": p_cargo
        }).scalar()

        db.commit()

        if not result:
            raise HTTPException(status_code=404, detail="No se obtuvo resultado del procedimiento")

        # ✅ Aseguramos que FastAPI lo interprete como dict y valide con el schema
        if isinstance(result, str):
            import json
            result = json.loads(result)

        return result

    except Exception as e:
        db.rollback()
        print("❌ Error en sp_ente_y_servidor_publico_gestionar_ambos:", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")