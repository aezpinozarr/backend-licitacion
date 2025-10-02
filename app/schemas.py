# app/schemas.py
from pydantic import BaseModel
from typing import Optional
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
        from_attributes = True  # En Pydantic v2 sustituye a orm_mode


class ClasificacionLicitacionOut(BaseModel):
    id: int
    descripcion: str

    class Config:
        from_attributes = True  # reemplaza orm_mode


class EnteOut(BaseModel):
    id: str
    descripcion: str
    siglas: Optional[str]
    clasificacion: Optional[str]
    id_ente_tipo: Optional[str]
    ente_tipo_descripcion: Optional[str]

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

class ClasificacionLicitacionOut(BaseModel):
    id: int
    descripcion: str
    tipo_licitacion: str

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

# ===========================
# Fuentes de financiamiento
# ===========================
class FuenteFinanciamiento(BaseModel):
    id: int
    descripcion: str

class SesionFuenteBase(BaseModel):
    id_calendario_sesiones: int
    id_fuente_financiamiento: int

class SesionFuenteCreate(SesionFuenteBase):
    pass

class SesionFuenteOut(BaseModel):
    id_calendario_sesiones: int
    id_fuente_financiamiento: int
    fuente_descripcion: str


# ========= Fechas de sesiones =========

class SesionFechaCreate(BaseModel):
    id_calendario_sesiones: int
    fecha: date
    hora: time   # 👈 antes era datetime con tz
    activo: bool = True

class SesionFechaUpdate(BaseModel):
    id: int
    fecha: date
    hora: time   # 👈 igual aquí, sin tz

class SesionFechaOut(BaseModel):
    id: int
    id_calendario_sesiones: int
    fecha: date
    hora: time
    activo: bool


class EntregableOut(BaseModel):
    id: int
    descripcion: str
    id_calendario_sesiones: int
    estatus: bool

    class Config:
        from_attributes = True


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
        orm_mode = True


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