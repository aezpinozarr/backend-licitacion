from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import os

from app.routers import (
    clientes, catalogos, sesiones, sesiones_fuentes, sesiones_fechas,
    sesiones_entregables, ente_tipo, servidores_publicos, servidor_publico,
    sesiones_fechas_pivot, ente_servidor_publico, rubro, proveedor, entidad_federativa, usuarios,
    proceso_seguimiento_ente, proceso_seguimiento_partida_ente, proceso_seguimiento_partida_rubro_ente,
    proceso_seguimiento_partida_rubro_proveedor_ente,
    catalogos_ente, catalogos_servidor_publico, catalogos_sesion_numero, proceso_enum_tipo_licitacion, partidas,
    fuentes_financiamiento, presupuesto_proveedor, entes_usuario, tipo_evento, auxiliares, procesos, proceso_detalle,
    vista_seguimiento_partida_rubro_proveedor_ente, sp_add_remove_rubro, procesos_proveedor_rubro_v2,
    sp_rector_seguimiento_detalle,sp_rector_seguimiento_gestion,sp_rector_seguimiento_preregistrados,
    sp_cat_fundamiento, sp_enum_seguimiento_partida_rubro_estatus, sp_rector_seguimiento_gestion_proveedor_adjudicado,
    verificar_adjudicado, reporte_adjudicado, sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer,notificaciones,
    sp_ente_seguimiento, sp_rector_seguimiento_detalle_v1, sp_ente_seguimiento_partida, sp_ente_y_servidor_publico_gestionar_ambos,
    sp_rector_seguimiento_gestion_estatus, sp_cat_proveedor_gestionar_dialog
)

from app.routers.procesos_editar import ( sp_seguimiento, sp_seguimiento_partida, sp_seguimiento_partida_rubro,
sp_seguimiento_partida_rubro_proveedor, sp_ente_seguimiento_captura, sp_ente_seguimiento_partida_captura, 
sp_ente_seguimiento_partida_rubro_captura, sp_ente_seguimiento_partida_rubro_proveedor_captura)

from app.routers.nuevo_calendario import (sp_calendario_gestionar, sp_calendario_fuentes_financiamiento_gestionar, sp_calendario_fechas_gestionar, sp_calendario, sp_calendario_fuentes_financiamiento, sp_calendario_fechas)

# =======================================================
# 🚀 Configuración principal
# =======================================================
app = FastAPI(title="Backend Licitación", version="1.1")

# =======================================================
# ⚙️ Middleware de seguridad
# =======================================================
# ❌ No forzamos redirecciones (Railway/Render ya usan HTTPS a nivel proxy)
# ✅ Añadimos cabeceras de seguridad
@app.middleware("http")
async def enforce_https_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# =======================================================
# 🌐 Configuración CORS
# =======================================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://my-dashboard-production-ecd1.up.railway.app",
    "https://my-dashboard-production-cd1a.up.railway.app",
    "https://my-dashboard-db1o.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================================================
# 📦 Rutas registradas
# =======================================================
app.include_router(clientes.router)
app.include_router(catalogos.router)
app.include_router(sesiones.router)
app.include_router(sesiones_fuentes.router)
app.include_router(sesiones_fechas.router)
app.include_router(sesiones_entregables.router)
app.include_router(ente_tipo.router)
app.include_router(servidores_publicos.router)
app.include_router(servidor_publico.router)
app.include_router(sesiones_fechas_pivot.router)
app.include_router(ente_servidor_publico.router)
app.include_router(rubro.router)
app.include_router(proveedor.router)
app.include_router(entidad_federativa.router)
app.include_router(usuarios.router)

# === 🔹 Nuevos endpoints ajustados a los SP actuales ===
app.include_router(proceso_seguimiento_ente.router)
app.include_router(proceso_seguimiento_partida_ente.router)
app.include_router(proceso_seguimiento_partida_rubro_ente.router)
app.include_router(proceso_seguimiento_partida_rubro_proveedor_ente.router)
app.include_router(vista_seguimiento_partida_rubro_proveedor_ente.router)
app.include_router(sp_add_remove_rubro.router)
app.include_router(procesos_proveedor_rubro_v2.router)
app.include_router(sp_rector_seguimiento_detalle.router)
app.include_router(sp_rector_seguimiento_gestion.router)
app.include_router(sp_rector_seguimiento_preregistrados.router)
app.include_router(sp_enum_seguimiento_partida_rubro_estatus.router)
app.include_router(sp_cat_fundamiento.router)
app.include_router(sp_rector_seguimiento_gestion_proveedor_adjudicado.router)
app.include_router(verificar_adjudicado.router)
app.include_router(reporte_adjudicado.router)
app.include_router(notificaciones.router)
app.include_router(sp_ente_seguimiento.router)
app.include_router(sp_rector_seguimiento_detalle_v1.router)
app.include_router(sp_ente_y_servidor_publico_gestionar_ambos.router)
app.include_router(sp_rector_seguimiento_gestion_estatus.router)
app.include_router(sp_cat_proveedor_gestionar_dialog.router)

# === 🔹 Otros catálogos y utilidades ===
app.include_router(catalogos_ente.router)
app.include_router(catalogos_servidor_publico.router)
app.include_router(catalogos_sesion_numero.router)
app.include_router(proceso_enum_tipo_licitacion.router)
app.include_router(partidas.router)
app.include_router(fuentes_financiamiento.router)
app.include_router(presupuesto_proveedor.router)
app.include_router(entes_usuario.router)
app.include_router(tipo_evento.router)
app.include_router(auxiliares.router)
app.include_router(procesos.router)
app.include_router(proceso_detalle.router)
app.include_router(sp_rector_seg_partida_rubro_proveedor_adjudicado_deshacer.router)
app.include_router(sp_ente_seguimiento_partida.router)


# ======================================================
# EDITAR PROCESOS ---- > FORMULARIO 4 PASOS.
# ======================================================
app.include_router(sp_seguimiento.router)
app.include_router(sp_seguimiento_partida.router)
app.include_router(sp_seguimiento_partida_rubro.router)
app.include_router(sp_seguimiento_partida_rubro_proveedor.router)
app.include_router(sp_ente_seguimiento_captura.router)
app.include_router(sp_ente_seguimiento_partida_captura.router)
app.include_router(sp_ente_seguimiento_partida_rubro_captura.router)
app.include_router(sp_ente_seguimiento_partida_rubro_proveedor_captura.router)


# ======================================================
# NUEVO CALENDARIO ---- > NUEVAS SESIONES
# ======================================================
app.include_router(sp_calendario_gestionar.router)
app.include_router(sp_calendario_fuentes_financiamiento_gestionar.router)
app.include_router(sp_calendario_fechas_gestionar.router)

# ======================================================
# NUEVO CALENDARIO ---- > CONSULTA DE SESIONES
# ======================================================
app.include_router(sp_calendario.router)
app.include_router(sp_calendario_fuentes_financiamiento.router)
app.include_router(sp_calendario_fechas.router)
# =======================================================
# 🔍 Endpoint raíz para verificación
# =======================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "🚀 Backend activo con HTTPS estable y CORS configurado correctamente",
    }