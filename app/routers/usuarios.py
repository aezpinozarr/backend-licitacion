from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app import schemas

router = APIRouter(
    prefix="/seguridad/usuarios",
    tags=["Usuarios"]
)

# ===========================================
# 🔹 Crear usuario
# ===========================================
@router.post("/", response_model=dict)
def crear_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario usando el SP seguridad.sp_usuarios_gestionar()
    """
    try:
        query = text("""
            SELECT seguridad.sp_usuarios_gestionar(
                'NUEVO', NULL, :p_username, :p_nombre,
                NULL, :p_pass_hash, 0, NULL,
                :p_id_ente, :p_tipo, TRUE
            )
        """)
        result = db.execute(query, data.dict()).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=400, detail="No se pudo crear el usuario")

        return {"resultado": result, "mensaje": "✅ Usuario creado correctamente"}
    except Exception as e:
        print("❌ Error al crear usuario:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# 🔹 Editar usuario
# ===========================================
@router.put("/", response_model=dict)
def editar_usuario(data: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    """
    Edita un usuario existente usando el SP seguridad.sp_usuarios_gestionar()
    """
    try:
        query = text("""
            SELECT seguridad.sp_usuarios_gestionar(
                'EDITAR', :p_id, :p_username, :p_nombre,
                NULL, :p_pass_hash, 0, NULL,
                :p_id_ente, :p_tipo, TRUE
            )
        """)
        result = db.execute(query, data.dict()).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"resultado": result, "mensaje": "✏️ Usuario actualizado correctamente"}
    except Exception as e:
        print("❌ Error al editar usuario:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# 🔹 Eliminar usuario (marcar como inactivo)
# ===========================================
@router.delete("/{id}", response_model=dict)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    """
    Marca un usuario como inactivo usando 'ELIMINAR'
    """
    try:
        query = text("""
            SELECT seguridad.sp_usuarios_gestionar(
                'ELIMINAR', :p_id, NULL, NULL,
                NULL, NULL, 0, NULL,
                '0', 'ENTE', FALSE
            )
        """)
        result = db.execute(query, {"p_id": id}).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"resultado": result, "mensaje": "🗑️ Usuario eliminado correctamente"}
    except Exception as e:
        print("❌ Error al eliminar usuario:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# 🔹 Recuperar usuario eliminado
# ===========================================
@router.put("/recuperar/{id}", response_model=dict)
def recuperar_usuario(id: int, db: Session = Depends(get_db)):
    """
    Reactiva un usuario eliminado previamente
    """
    try:
        query = text("""
            SELECT seguridad.sp_usuarios_gestionar(
                'RECUPERAR', :p_id, NULL, NULL,
                NULL, NULL, 0, NULL,
                '0', 'ENTE', TRUE
            )
        """)
        result = db.execute(query, {"p_id": id}).scalar()
        db.commit()

        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"resultado": result, "mensaje": "✅ Usuario recuperado correctamente"}
    except Exception as e:
        print("❌ Error al recuperar usuario:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================
# 🔹 Login (autenticación)
# ===========================================
@router.post("/login", response_model=dict)
def autenticar_usuario(data: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    """
    Autentica un usuario usando seguridad.sp_usuarios_autenticar()
    """
    try:
        query = text("""
            SELECT seguridad.sp_usuarios_autenticar(:p_username, :p_password)
        """)
        result = db.execute(query, {
            "p_username": data.p_username,
            "p_password": data.p_password
        }).scalar()  # ✅ Se usa scalar() para leer JSON correctamente

        print("✅ Resultado autenticación:", result)

        if not result:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        return result  # ✅ Devuelve directamente el JSON del SP

    except Exception as e:
        print("❌ Error al autenticar usuario:", e)
        raise HTTPException(status_code=500, detail="Error de autenticación")


# ===========================================
# 🔹 Obtener tipos de usuario
# ===========================================
@router.get("/tipos", response_model=list[str])
def obtener_tipos_usuario(db: Session = Depends(get_db)):
    """
    Llama al SP seguridad.sp_enum_usuarios_tipo()
    """
    try:
        rows = db.execute(text("SELECT * FROM seguridad.sp_enum_usuarios_tipo()")).mappings().all()
        return [r["usuarios_tipo"] for r in rows]
    except Exception as e:
        print("❌ Error al obtener tipos:", e)
        raise HTTPException(status_code=500, detail="Error al obtener tipos de usuario")


# ===========================================
# 🔹 Listar usuarios activos
# ===========================================
@router.get("/", response_model=list[schemas.UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Consulta directa a seguridad.usuarios (solo activos)
    """
    try:
        rows = db.execute(text("""
            SELECT id, username, nombre, tipo, COALESCE(activo, true) AS activo
            FROM seguridad.usuarios
            WHERE activo IS TRUE
            ORDER BY id
        """)).mappings().all()
        return [schemas.UsuarioOut(**r) for r in rows]
    except Exception as e:
        print("❌ Error al obtener usuarios:", e)
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")
    

# ===========================================
# 🔹 Obtener usuario por ID
# ===========================================
@router.get("/{id}", response_model=schemas.UsuarioOut)
def obtener_usuario_por_id(id: int, db: Session = Depends(get_db)):
    """
    Retorna un usuario específico según su ID
    """
    try:
        row = db.execute(text("""
            SELECT id, username, nombre, tipo, activo, id_ente
            FROM seguridad.usuarios
            WHERE id = :id
        """), {"id": id}).mappings().first()

        if not row:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return schemas.UsuarioOut(**row)

    except Exception as e:
        print("❌ Error al obtener usuario:", e)
        raise HTTPException(status_code=500, detail="Error al obtener usuario")