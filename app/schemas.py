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
    p_id: int
    p_username: str
    p_nombre: str
    p_pass_hash: Optional[str] = None
    p_id_ente: str
    p_tipo: str


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

# =========================
# Seguimiento de procesos
# =========================

class ProcesoSeguimientoEnteIn(BaseModel):
    p_accion: str = Field(..., description="'NUEVO' o 'EDITAR'")
    p_id: Optional[int] = None
    p_e_id_ente: int  # ✅ CAMBIAR de str → int
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


class ProcesoPresupuestoEnteIn(BaseModel):
    p_accion: str
    p_id_proceso_seguimiento: int
    p_id: Optional[int] = None
    p_e_no_requisicion: str
    p_e_id_partida: str
    p_e_id_fuente_financiamiento: str
    p_e_monto_presupuesto_suficiencia: float

class ProcesoPresupuestoRubroEnteIn(BaseModel):
    p_accion: str
    p_id_proceso_seguimiento_presupuesto: int
    p_id: Optional[int] = 0
    p_e_id_rubro: str
    p_e_monto_presupuesto_suficiencia: float

class ProcesoPresupuestoProveedorIn(BaseModel):
    p_accion: str
    p_id_proceso_seguimiento_presupuesto: int
    p_id_proceso_seguimiento_presupuesto_rubro: Optional[int] = None  # ✅ <-- agregar este campo
    p_id: Optional[int] = 0
    p_e_rfc_proveedor: str
    p_e_importe_sin_iva: float
    p_e_importe_total: float
    p_r_importe_ajustado_sin_iva: Optional[float] = 0.0
    p_r_importe_ajustado_total: Optional[float] = 0.0


class ProcesoPresupuestoRubroProveedorEnteIn(BaseModel):
    p_accion: str
    p_id_proceso_seguimiento_presupuesto_rubro: int
    p_id: Optional[int] = 0
    p_e_rfc_proveedor: str
    p_e_importe_sin_iva: float
    p_e_importe_total: float
    p_r_importe_ajustado_sin_iva: float
    p_r_importe_ajustado_total: float

    class Config:
        from_attributes = True