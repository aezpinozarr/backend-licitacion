from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from app import schemas
from app.db import get_db
from app.schemas import (
    ClasificacionLicitacionOut,
    EnteOut,
    ServidorPublicoOut,
)

router = APIRouter(prefix="/catalogos", tags=["Catálogos"])

# ===========================
# Clasificación de licitación
# ===========================
@router.get("/clasificacion-licitacion", response_model=List[ClasificacionLicitacionOut])
def get_clasificacion_licitacion(
    p_id: Optional[int] = Query(-99, description="ID de la clasificación (-99 para todos)"),
    db: Session = Depends(get_db),
):
    try:
        rows = db.execute(
            text("SELECT * FROM catalogos.sp_cat_clasificacion_licitacion(:p_id)"),
            {"p_id": int(p_id)}
        ).mappings().all()
        return [ClasificacionLicitacionOut(**row) for row in rows]
    except Exception as e:
        print("❌ Error en /catalogos/clasificacion-licitacion:", repr(e))
        raise HTTPException(status_code=500, detail="Error interno al obtener clasificación de licitación")


# ===========================
# Entes (CRUD completo)
# ===========================

@router.get("/entes", response_model=List[schemas.EnteOut])
def get_entes(
    p_id: Optional[str] = Query("-99", description="ID del ente (-99 para todos)"),
    p_descripcion: Optional[str] = Query("-99", description="Descripción del ente (-99 para todos)"),
    p_activo: Optional[int] = Query(-99, description="Filtrar por estado del ente (-99 todos, 1 activos, 0 eliminados)"),
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_ente(:p_id, :p_descripcion, :p_activo)"),
            {"p_id": p_id, "p_descripcion": p_descripcion, "p_activo": p_activo}
        ).mappings().all()
        return [schemas.EnteOut(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /entes: {str(e)}")




@router.get("/entes/{ente_id}", response_model=schemas.EnteOut)
def get_ente_by_id(ente_id: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_ente(:p_id, :p_descripcion, :p_activo)"),
            {"p_id": ente_id, "p_descripcion": "-99", "p_activo": -99},
        ).mappings().first()
        if not result:
            raise HTTPException(status_code=404, detail="Ente no encontrado")
        return schemas.EnteOut(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entes", response_model=int)
def create_ente(ente: schemas.EnteCreate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, :descripcion, :siglas, :clasificacion, :id_ente_tipo, :activo
                ) AS result
            """),
            {
                "accion": "NUEVO",
                "p_id": None,
                "descripcion": ente.descripcion,
                "siglas": ente.siglas,
                "clasificacion": ente.clasificacion,
                "id_ente_tipo": ente.id_ente_tipo,
                "activo": ente.activo,
            },
        )
        new_id = result.scalar()
        db.commit()
        return new_id
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/entes/{ente_id}", response_model=int)
def update_ente(ente_id: str, ente: schemas.EnteUpdate, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, :descripcion, :siglas, :clasificacion, :id_ente_tipo, :activo
                ) AS result
            """),
            {
                "accion": "EDITAR",
                "p_id": ente_id,
                "descripcion": ente.descripcion,
                "siglas": ente.siglas,
                "clasificacion": ente.clasificacion,
                "id_ente_tipo": ente.id_ente_tipo,
                "activo": ente.activo,
            },
        )
        out = result.scalar()
        db.commit()
        return out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/entes/{ente_id}", response_model=int)
def delete_ente(ente_id: str, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    :accion, :p_id, NULL, NULL, NULL, NULL, NULL
                ) AS result
            """),
            {"accion": "ELIMINAR", "p_id": ente_id},
        )
        out = result.scalar()
        db.commit()
        return out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/entes/{ente_id}/reactivar", response_model=int)
def reactivar_ente(ente_id: str, db: Session = Depends(get_db)):
    try:
        # ✅ 1. Obtener los datos actuales del ente
        current = db.execute(
            text("SELECT * FROM catalogos.sp_cat_ente(:p_id, '-99', -99)"),
            {"p_id": ente_id}
        ).mappings().first()

        if not current:
            raise HTTPException(status_code=404, detail="Ente no encontrado")

        # ✅ 2. Enviar todos los datos con activo=True
        result = db.execute(
            text("""
                SELECT catalogos.sp_cat_ente_gestionar(
                    'EDITAR',
                    :p_id,
                    :p_descripcion,
                    :p_siglas,
                    :p_clasificacion,
                    :p_id_ente_tipo,
                    TRUE
                ) AS result
            """),
            {
                "p_id": ente_id,
                "p_descripcion": current["descripcion"],
                "p_siglas": current["siglas"],
                "p_clasificacion": current["clasificacion"],
                "p_id_ente_tipo": current["id_ente_tipo"]
            },
        )
        out = result.scalar()
        db.commit()
        return out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ===========================
# Servidores públicos
# ===========================
@router.get("/servidores-publicos", response_model=List[ServidorPublicoOut])
def get_servidores_publicos(
    p_id: Optional[int] = Query(-99, description="ID del servidor público (-99 para todos)"),
    db: Session = Depends(get_db)
):
    try:
        result = db.execute(
            text("SELECT * FROM catalogos.sp_cat_servidor_publico(:p_id)"),
            {"p_id": p_id}
        ).mappings().all()
        return [ServidorPublicoOut(**row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /servidores-publicos: {str(e)}")


# ===========================
# Enums (catálogos fijos desde schema procesos)
# ===========================
@router.get("/comite")
def get_enum_comite(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM procesos.sp_enum_comite()")).mappings().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /comite: {str(e)}")


@router.get("/modo-sesion")
def get_enum_modo_sesion(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT * FROM procesos.sp_enum_modo_sesion()")).mappings().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en /modo-sesion: {str(e)}")


# ===========================
# Servidores públicos por ente
# ===========================
@router.get("/servidores-publicos-ente")
def get_servidores_publicos_ente(
    p_id: Optional[int] = Query(-99, description="ID del servidor público (-99 para todos)"),
    p_id_ente: Optional[str] = Query("-99", description="ID del ente (-99 para todos)"),
    db: Session = Depends(get_db),
):
    try:
        p_id_casted = int(p_id) if p_id is not None else -99
        p_id_ente_casted = str(p_id_ente) if p_id_ente not in (None, -99) else "-99"

        sql = text("""
            SELECT *
            FROM catalogos.sp_ente_servidor_publico(
                CAST(:p_id AS smallint),
                CAST(:p_id_ente AS varchar)
            )
        """)

        rows = db.execute(sql, {"p_id": p_id_casted, "p_id_ente": p_id_ente_casted}).mappings().all()
        return [dict(r) for r in rows]

    except Exception as e:
        print("❌ Error en /servidores-publicos-ente:", repr(e))
        raise HTTPException(status_code=500, detail="Error interno al obtener servidores públicos por ente")