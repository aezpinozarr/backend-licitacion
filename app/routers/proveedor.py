from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/catalogos/proveedor",
    tags=["Catálogo Proveedor"]
)

# ===============================
# Obtener proveedores
# ===============================
@router.get("/", response_model=List[schemas.ProveedorOut])
def get_proveedores(
    p_rfc: Optional[str] = Query("-99", description="RFC del proveedor (-99 para todos)"),
    db: Session = Depends(get_db)
):
    """Obtiene los proveedores registrados"""
    try:
        rows = db.execute(
            text("SELECT * FROM catalogos.sp_cat_proveedor(:p_rfc)"),
            {"p_rfc": p_rfc}
        ).mappings().all()

        return [schemas.ProveedorOut(**row) for row in rows]
    except Exception as e:
        print("❌ Error en /proveedor:", repr(e))
        raise HTTPException(status_code=500, detail="Error al obtener proveedores")


# ===============================
# Crear proveedor
# ===============================
@router.post("/", response_model=int)
def crear_proveedor(data: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proveedor mediante el procedimiento almacenado"""
    try:
        print(f"🟢 Creando proveedor RFC={data.rfc}")
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_proveedor_gestionar(
                    'NUEVO',
                    CAST(:p_rfc AS varchar),
                    CAST(:p_razon_social AS varchar),
                    CAST(:p_nombre_comercial AS varchar),
                    CAST(:p_persona_juridica AS varchar),
                    CAST(:p_correo_electronico AS varchar),
                    CAST(:p_id_entidad_federativa AS smallint),
                    CAST(:p_entidad_federativa AS varchar)
                )
            """),
            {
                "p_rfc": data.rfc,
                "p_razon_social": data.razon_social,
                "p_nombre_comercial": data.nombre_comercial,
                "p_persona_juridica": data.persona_juridica,
                "p_correo_electronico": data.correo_electronico,
                "p_id_entidad_federativa": data.id_entidad_federativa,
                "p_entidad_federativa": data.entidad_federativa
            }
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al crear proveedor:", repr(e))
        raise HTTPException(status_code=500, detail=f"Error al crear proveedor: {str(e)}")


# ===============================
# Editar proveedor
# ===============================
@router.put("/", response_model=int)
def editar_proveedor(data: schemas.ProveedorUpdate, db: Session = Depends(get_db)):
    """Actualiza un proveedor existente"""
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_proveedor_gestionar(
                    'EDITAR',
                    CAST(:p_rfc AS varchar),
                    CAST(:p_razon_social AS varchar),
                    CAST(:p_nombre_comercial AS varchar),
                    CAST(:p_persona_juridica AS varchar),
                    CAST(:p_correo_electronico AS varchar),
                    CAST(:p_id_entidad_federativa AS smallint),
                    CAST(:p_entidad_federativa AS varchar)
                )
            """),
            {
                "p_rfc": data.rfc,
                "p_razon_social": data.razon_social,
                "p_nombre_comercial": data.nombre_comercial,
                "p_persona_juridica": data.persona_juridica,
                "p_correo_electronico": data.correo_electronico,
                "p_id_entidad_federativa": data.id_entidad_federativa,
                "p_entidad_federativa": data.entidad_federativa
            }
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al editar proveedor:", repr(e))
        raise HTTPException(status_code=500, detail=f"Error al editar proveedor: {str(e)}")


# ===============================
# Eliminar proveedor
# ===============================
@router.delete("/", response_model=int)
def eliminar_proveedor(data: schemas.ProveedorDelete, db: Session = Depends(get_db)):
    """Inactiva (ELIMINA) un proveedor"""
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_proveedor_gestionar(
                    'ELIMINAR',
                    CAST(:p_rfc AS varchar)
                )
            """),
            {"p_rfc": data.rfc}
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al eliminar proveedor:", repr(e))
        raise HTTPException(status_code=500, detail=f"Error al eliminar proveedor: {str(e)}")


# ===============================
# Recuperar proveedor
# ===============================
@router.put("/recuperar", response_model=int)
def recuperar_proveedor(data: schemas.ProveedorDelete, db: Session = Depends(get_db)):
    """Reactiva un proveedor previamente eliminado"""
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_proveedor_gestionar(
                    'RECUPERAR',
                    CAST(:p_rfc AS varchar)
                )
            """),
            {"p_rfc": data.rfc}
        ).scalar()
        db.commit()
        return result
    except Exception as e:
        print("❌ Error al recuperar proveedor:", repr(e))
        raise HTTPException(status_code=500, detail=f"Error al recuperar proveedor: {str(e)}")