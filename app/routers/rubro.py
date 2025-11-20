from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.db import get_db
from app import schemas

# ======================================================
# ✅ IMPORTANTE:
# Quitamos la barra extra del prefix para evitar redirecciones 307
# ======================================================
router = APIRouter(
    prefix="/catalogos/rubro",
    tags=["Catálogo Rubro"]
)

# ===============================
# Obtener rubros
# ===============================
@router.get("", response_model=List[schemas.RubroOut])  # 👈 sin barra final
def get_rubros(
    p_id: Optional[str] = Query("-99", description="ID del rubro (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene los rubros registrados.
    Si p_id = -99, devuelve todos los rubros.
    """
    try:
        rows = db.execute(
            text("SELECT * FROM catalogos.sp_cat_rubro(:p_id)"),
            {"p_id": p_id}
        ).mappings().all()
        return [schemas.RubroOut(**row) for row in rows]
    except Exception as e:
        print("❌ Error en /rubro:", repr(e))
        raise HTTPException(status_code=500, detail="Error al obtener los rubros")

# ===============================
# Crear rubro
# ===============================
@router.post("", response_model=dict)
def crear_rubro(data: schemas.RubroCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rubro usando la versión v2 del SP.
    Genera ID automático y retorna el ID creado.
    """
    try:
        result = db.execute(
            text("""
                SELECT * FROM catalogos.sp_cat_rubro_gestionar_v2(
                    'NUEVO',
                    NULL,
                    CAST(:p_descripcion AS varchar)
                )
            """),
            {"p_descripcion": data.descripcion}
        ).mappings().first()

        if result is None:
            raise HTTPException(status_code=500, detail="Error al crear rubro")

        db.commit()

        return {
            "resultado": result["resultado"],
            "id_generado": result["nuevo_id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear rubro: {str(e)}")

# ===============================
# Editar rubro
# ===============================
@router.put("", response_model=int)  # 👈 sin barra final
def editar_rubro(data: schemas.RubroUpdate, db: Session = Depends(get_db)):
    """
    Edita un rubro existente (solo la descripción).
    Retorna 1 si se actualiza correctamente.
    """
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_rubro_gestionar(
                    'EDITAR',
                    CAST(:p_id AS varchar),
                    CAST(:p_descripcion AS varchar)
                )
            """),
            {"p_id": data.id, "p_descripcion": data.descripcion}
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al editar rubro:", repr(e))
        raise HTTPException(status_code=500, detail="Error al editar rubro")

# ===============================
# Eliminar rubro (inactivar)
# ===============================
@router.delete("", response_model=int)  # 👈 sin barra final
def eliminar_rubro(data: schemas.RubroDelete, db: Session = Depends(get_db)):
    """
    Marca un rubro como inactivo (ELIMINAR).
    Retorna 1 si se actualiza correctamente.
    """
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_rubro_gestionar(
                    'ELIMINAR',
                    CAST(:p_id AS varchar),
                    NULL
                )
            """),
            {"p_id": data.id}
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al eliminar rubro:", repr(e))
        raise HTTPException(status_code=500, detail="Error al eliminar rubro")

# ===============================
# Recuperar rubro (reactivar)
# ===============================
@router.put("/recuperar", response_model=int)
def recuperar_rubro(data: schemas.RubroDelete, db: Session = Depends(get_db)):
    """
    Reactiva un rubro previamente eliminado (RECUPERAR).
    Retorna 1 si se actualiza correctamente.
    """
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_rubro_gestionar(
                    'RECUPERAR',
                    CAST(:p_id AS varchar),
                    NULL
                )
            """),
            {"p_id": data.id}
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al recuperar rubro:", repr(e))
        raise HTTPException(status_code=500, detail="Error al recuperar rubro")