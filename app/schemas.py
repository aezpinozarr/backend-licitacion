from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date, time
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union
from datetime import datetime, date, time

# ===========================
# Clientes
# ===========================
class ClienteBase(BaseModel):
    nombre: str
    edad: int


class ClienteCreate(ClienteBase):
    pass


class ClienteOut(ClienteBase):
    id: int
    fecha_creacion: Optional[datetime] = None


# ===========================
# Catálogos
# ===========================
class ClasificacionLicitacion(BaseModel):
    id: int
    descripcion: str
    tipo_licitacion: str


class Ente(BaseModel):
    id: str
    descripcion: str
    siglas: str
    clasificacion: str
    id_ente_tipo: str
    ente_tipo_descripcion: str


class ServidorPublico(BaseModel):
    id: int
    nombre: str
    cargo: str
    activo: bool


class ServidorPublicoEnte(BaseModel):
    id: int
    nombre: str
    cargo: str
    activo: bool
    id_ente: str
    ente_publico: str
    ente_siglas: str
    ente_clasificacion: str


class EnumComite(BaseModel):
    comite_sesion: str


class EnumModoSesion(BaseModel):
    modo_sesion: str


# ===========================
# Sesiones
# ===========================
class SesionBase(BaseModel):
    id_ente: str
    id_usuario: int
    oficio_o_acta_numero: str
    asunto: str
    fecha: date
    id_servidor_publico: Optional[int] = None
    modo_sesion: Optional[str] = None
    comite: Optional[str] = None
    id_clasificacion_licitacion: Optional[int] = None
    activo: Optional[bool] = True


class SesionCreate(SesionBase):
    pass


class SesionUpdate(SesionBase):
    pass


class SesionOut(SesionBase):
    id: int
    creado_en: Optional[datetime] = None


# ===========================
# Ente
# ===========================
class EnteOut(BaseModel):
    id: str
    descripcion: str
    siglas: Optional[str]
    clasificacion: Optional[str]
    id_ente_tipo: Optional[str]
    ente_tipo_descripcion: Optional[str]

    class Config:
        from_attributes = True


class ClasificacionLicitacionOut(BaseModel):
    id: int
    descripcion: str
    tipo_licitacion: str

    class Config:
        from_attributes = True  


class ServidorPublicoOut(BaseModel):
    id: int
    nombre: str
    cargo: str
    activo: bool
    id_ente: str
    ente_publico: str
    ente_siglas: str
    ente_clasificacion: str

    class Config:
        from_attributes = True


class ComiteOut(BaseModel):
    comite_sesion: str

    class Config:
        from_attributes = True


class ModoSesionOut(BaseModel):
    modo_sesion: str

    class Config:
        from_attributes = True


# ===========================
# Fuentes de financiamiento (catálogo)
# ===========================
class FuenteFinanciamiento(BaseModel):
    id: Union[int, str]
    descripcion: str
    etiquetado: str
    fondo: Optional[str] = None  # ✅ agregado para traer columna "fondo"

    class Config:
        from_attributes = True


# ===========================
# Sesiones - Fuentes de financiamiento
# ===========================
class SesionFuenteBase(BaseModel):
    id_calendario_sesiones: int
    id_fuente_financiamiento: int


class SesionFuenteCreate(SesionFuenteBase):
    pass


class SesionFuenteOut(BaseModel):
    id_calendario_sesiones: int
    id_fuente_financiamiento: int
    fuente_descripcion: str

    class Config:
        from_attributes = True


# ========= Fechas de sesiones =========
class SesionFechaCreate(BaseModel):
    id_calendario_sesiones: int
    fecha: date
    hora: time   # 👈 sin tz
    activo: bool = True


class SesionFechaUpdate(BaseModel):
    id: int
    fecha: date
    hora: time   # 👈 sin tz


class SesionFechaOut(BaseModel):
    id: int
    id_calendario_sesiones: int
    fecha: date
    hora: time
    activo: bool


# ========= Entregables =========
class EntregableOut(BaseModel):
    id: int
    descripcion: str
    id_calendario_sesiones: int
    estatus: bool

    class Config:
        from_attributes = True


# ==========================
# Schemas para Entes
# ==========================
class EnteBase(BaseModel):
    descripcion: str
    siglas: str
    clasificacion: str
    id_ente_tipo: str
    activo: Optional[bool] = True


class EnteCreate(EnteBase):
    pass


class EnteUpdate(EnteBase):
    pass


class EnteOut(EnteBase):
    id: str
    ente_tipo_descripcion: str


# ==========================
# Schemas para Tipo de Ente
# ==========================
class EnteTipoOut(BaseModel):
    id: str
    descripcion: str


# ==========================
# Schemas para Servidores Públicos
# ==========================
class ServidorPublicoBase(BaseModel):
    nombre: str
    cargo: str
    activo: bool = True


class ServidorPublicoCreate(ServidorPublicoBase):
    pass


class ServidorPublicoUpdate(ServidorPublicoBase):
    id: int


class ServidorPublicoOut(ServidorPublicoBase):
    id: int

    class Config:
        from_attributes = True


# ==========================
# Calendario Sesiones Pivot
# ==========================
class SesionFechaPivotOut(BaseModel):
    id: int
    id_calendario_sesiones: int
    id_ente: str
    descripcion: str
    licitacion_clasificacion: str
    licitacion_tipo: str
    ENE: Optional[str] = None
    FEB: Optional[str] = None
    MAR: Optional[str] = None
    ABR: Optional[str] = None
    MAY: Optional[str] = None
    JUN: Optional[str] = None
    JUL: Optional[str] = None
    AGO: Optional[str] = None
    SEP: Optional[str] = None
    OCT: Optional[str] = None
    NOV: Optional[str] = None
    DIC: Optional[str] = None

# ===============================
# Ente - Servidor Público (relación)
# ===============================
class EnteServidorPublicoCreate(BaseModel):
    id_ente: str
    id_servidor_publico: int

# ===============================
# Rubros
# ===============================
class RubroOut(BaseModel):
    id: str
    descripcion: str
    activo: bool

    class Config:
        from_attributes = True


class RubroCreate(BaseModel):
    id: str
    descripcion: str


class RubroUpdate(BaseModel):
    id: str
    descripcion: str


class RubroDelete(BaseModel):
    id: str


# ===============================
# Proveedor
# ===============================
from pydantic import BaseModel, EmailStr
from typing import Optional

class ProveedorOut(BaseModel):
    rfc: str
    razon_social: str
    nombre_comercial: Optional[str]
    persona_juridica: Optional[str]
    correo_electronico: Optional[EmailStr]
    activo: bool
    id_entidad_federativa: int
    entidad_federativa: str

    class Config:
        from_attributes = True


class ProveedorCreate(BaseModel):
    rfc: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    persona_juridica: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    id_entidad_federativa: int
    entidad_federativa: Optional[str] = None


class ProveedorUpdate(BaseModel):
    rfc: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    persona_juridica: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    id_entidad_federativa: int
    entidad_federativa: Optional[str] = None


class ProveedorDelete(BaseModel):
    rfc: str


# ===============================
# Entidades Federativas
# ===============================
from pydantic import BaseModel

class EntidadFederativaOut(BaseModel):
    id: int
    descripcion: str

    class Config:
        from_attributes = True


# ===========================================
# 🧱 USUARIOS
# ===========================================

# =======================
# 🔹 Crear usuario
# =======================
class UsuarioCreate(BaseModel):
    p_username: str
    p_nombre: str
    p_pass_hash: str
    p_id_ente: str
    p_tipo: str


# =======================
# 🔹 Editar usuario
# =======================
class UsuarioUpdate(BaseModel):
    username: str
    nombre: str
    tipo: str
    activo: bool = True
    p_id_ente: Optional[str] = None
    p_pass_hash: Optional[str] = None


# =======================
# 🔹 Login
# =======================
class UsuarioLogin(BaseModel):
    p_username: str
    p_password: str


# =======================
# 🔹 Salida
# =======================
class UsuarioOut(BaseModel):
    id: int
    username: str
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    activo: bool
    id_ente: Optional[str] = None  # ✅ agregado
# =========================
# Seguimiento de procesos
# =========================


# ===========================================================
# 🟢 Proceso Seguimiento - Ente
# ===========================================================
class ProcesoSeguimientoEnteIn(BaseModel):
    p_accion: str = Field(..., description="'NUEVO' o 'EDITAR'")
    p_id: Optional[int] = None
    p_e_id_ente: str  # ✅ debe ser texto
    p_e_oficio_invitacion: str
    p_e_id_servidor_publico_emite: int
    p_e_servidor_publico_cargo: str
    p_e_tipo_licitacion: str
    p_e_tipo_licitacion_no_veces: int
    p_e_tipo_licitacion_notas: Optional[str] = ""
    p_e_fecha_y_hora_reunion: Union[datetime, str]
    p_e_id_usuario_registra: int

    class Config:
        from_attributes = True


# ===========================================================
# 🟡 Proceso Seguimiento - Partida Ente
# ===========================================================
class ProcesoPartidaEnteIn(BaseModel):
    p_accion: str
    p_id_seguimiento: int
    p_id: Optional[int] = None
    p_e_no_requisicion: Optional[str] = None
    p_e_id_partida: Optional[str] = None
    p_e_id_fuente_financiamiento: Optional[str] = None



# ===========================================================
# 🟠 Proceso Seguimiento - Partida Rubro Ente
# ===========================================================
class ProcesoPartidaRubroEnteIn(BaseModel):
    p_accion: str
    p_id_seguimiento_partida: int  # ✅ nombre correcto según el SP
    p_id: Optional[int] = 0
    p_e_id_rubro: str
    p_e_monto_presupuesto_suficiencia: float


# ===========================================================
# 🔴 Proceso Seguimiento - Partida Rubro Proveedor Ente
# ===========================================================
class ProcesoPartidaRubroProveedorEnteIn(BaseModel):
    p_accion: str
    p_id_seguimiento_partida: int  # 👈 nombre corregido
    p_id: Optional[int] = 0
    p_e_rfc_proveedor: str
    p_e_importe_sin_iva: float
    p_e_importe_total: float


# ============================
# 📘 SCHEMA: sp_add_remove_rubro
# ============================

class RubroRequest(BaseModel):
    p_accion: str                 # "NUEVO" o "ELIMINAR"
    p_id_seguimiento_partida: int
    p_id: Optional[int] = None    # Solo se usa en ELIMINAR
    p_e_id_rubro: Optional[str] = "0"
    p_e_monto_presupuesto_suficiencia: Optional[float] = 0.0



# ============================
# 📘 SCHEMA: SP V2 PROVEEDOR
# ============================


class ProveedorRubroRequest(BaseModel):
    p_accion: str
    p_id_seguimiento_partida_rubro: int
    p_id: Optional[int] = None
    p_e_rfc_proveedor: Optional[str] = None
    p_e_importe_sin_iva: Optional[float] = None
    p_e_importe_total: Optional[float] = None



# ============================
# 📘 CAPTURA RECTOR 
# ============================

class RectorGestionIn(BaseModel):
    p_accion: str
    p_r_suplencia_oficio_no: str
    p_r_fecha_emision: date
    p_r_asunto: str
    p_r_fecha_y_hora_reunion: datetime
    p_r_estatus: str
    p_r_id_usuario_registra: int
    p_r_id_servidor_publico_asiste: int
    p_r_observaciones: Optional[str] = None
    p_r_con_observaciones: Optional[bool] = False



# ============================
# PROVEEDOR ADJUDICADO 
# ============================


class SpRectorSeguimientoGestionProveedorAdjudicado(BaseModel):
    p_estatus: str
    p_id_seguimiento_partida_rubro: int
    p_id_seguimiento_partida_rubro_proveedor: Optional[int] = 0
    p_id: Optional[int] = None
    p_importe_ajustado_sin_iva: Optional[float] = 0
    p_importe_ajustado_total: Optional[float] = 0
    p_id_fundamento: Optional[int] = 0



# ============================
# DESHACER PROVEEDOR ADJUDICADO 
# ============================

class DeshacerAdjudicacionRequest(BaseModel):
    p_id: int


class DeshacerAdjudicacionResponse(BaseModel):
    resultado: int


# ======================================
# CAMBIAR CONTRASEÑA USUARIO AUTENTICADO  
# ======================================

class CambiarPassword(BaseModel):
    p_password_actual: Optional[str] = None
    p_password_nueva: str


# ===========================================
# GESTIONAR SERVIDOR PÚBLICO AL ENTE, PASO 1
# ===========================================

class EnteServidorPublicoResponse(BaseModel):
    resultado: str
    id_servidor_publico: Optional[int] = None
    id_ente: Optional[int] = None
    nombre: Optional[str] = None
    cargo: Optional[str] = None
    detalle: Optional[str] = None




# ======================================
# 🔹 Schema: Editar seguimiento (Paso 1)
# ======================================
class EnteSeguimientoUpdate(BaseModel):
    p_id: int
    p_e_id_ente: str
    p_e_oficio_invitacion: Optional[str] = ""
    p_e_id_servidor_publico_emite: Optional[int] = 0
    p_e_servidor_publico_cargo: Optional[str] = ""
    p_e_tipo_licitacion: Optional[str] = ""
    p_e_tipo_licitacion_no_veces: Optional[int] = 0
    p_e_tipo_licitacion_notas: Optional[str] = ""
    p_e_fecha_y_hora_reunion: Optional[str] = None
    p_e_id_usuario_registra: Optional[int] = 0

    class Config:
         from_attributes = True



# ======================================
# 🔹 Schema: Editar Partida (Paso 2)
# ======================================

class EnteSeguimientoPartidaUpdate(BaseModel):
    p_id_seguimiento: int
    p_id: Optional[int] = None
    p_e_no_requisicion: Optional[str] = None
    p_e_id_partida: Optional[str] = None
    p_e_id_fuente_financiamiento: Optional[str] = None

    class Config:
        from_attributes = True


# ======================================
# 🔹 Schema: Editar Rubro (Paso 3)
# ======================================


class EnteSeguimientoPartidaRubroUpdate(BaseModel):
    p_id_seguimiento_partida: int
    p_id: Optional[int] = None
    p_e_id_rubro: Optional[str] = "0"
    p_e_monto_presupuesto_suficiencia: Optional[float] = 0.0
    p_accion: Optional[str] = "NUEVO"  # Puede ser NUEVO o ELIMINAR

    class Config:
        from_attributes = True


# ======================================
# 🔹 Schema: Editar Proveedor (Paso 4)
# ======================================

class EnteSeguimientoPartidaRubroProveedorUpdate(BaseModel):
    p_id_seguimiento_partida_rubro: int
    p_id: Optional[int] = None
    p_e_rfc_proveedor: Optional[str] = None
    p_e_importe_sin_iva: Optional[float] = None
    p_e_importe_total: Optional[float] = None
    p_accion: Optional[str] = "NUEVO"  # Puede ser NUEVO o ELIMINAR

    class Config:
        from_attributes = True


# ======================================
# 🔹 CREAR PROVEEDOR PASO 4: DIALOG 
# ======================================

class ProveedorDialogCreate(BaseModel):
    p_rfc: str
    p_razon_social: str
    p_nombre_comercial: Optional[str] = None
    p_persona_juridica: Optional[str] = None
    p_correo_electronico: Optional[EmailStr] = None
    p_id_entidad_federativa: Optional[int] = None