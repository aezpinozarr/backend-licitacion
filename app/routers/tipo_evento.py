from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/procesos/tipos-evento",
    tags=["Procesos - Tipos de Evento"]
)

# ===========================================================
# 🔹 Obtener Tipos de Evento (desde enum)
# ===========================================================
@router.get("/", response_model=list)
def obtener_tipos_evento(db: Session = Depends(get_db)):
    """
    Llama al SP procesos.sp_enum_seguimiento_tipo_evento()
    que devuelve una lista de valores del enum 'enum_seguimiento_tipo_evento'.
    """
    try:
        query = text("SELECT * FROM procesos.sp_enum_seguimiento_tipo_evento()")
        result = db.execute(query).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron tipos de evento")

        # ✅ Convierte cada fila (solo tiene una columna tipo_evento)
        tipos = [{"id": r[0], "descripcion": r[0]} for r in result]

        return tipos

    except Exception as e:
        print("❌ Error cargando tipos de evento:", e)
        raise HTTPException(status_code=500, detail=str(e))