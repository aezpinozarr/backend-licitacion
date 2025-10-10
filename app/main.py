from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import os

from app.routers import (
    clientes, catalogos, sesiones, sesiones_fuentes, sesiones_fechas,
    sesiones_entregables, entes, ente_tipo, servidores_publicos, servidor_publico,
    sesiones_fechas_pivot, ente_servidor_publico, rubro, proveedor, entidad_federativa, usuarios,
    proceso_seguimiento_ente, proceso_seguimiento_presupuesto_ente, proceso_seguimiento_presupuesto_proveedor_ente,
    catalogos_ente, catalogos_servidor_publico,catalogos_sesion_numero,proceso_enum_tipo_licitacion, partidas,
    fuentes_financiamiento, presupuesto_proveedor
)

app = FastAPI(title="Backend Licitación", version="1.0")

# =======================================================
# ⚙️ Middleware de seguridad
# =======================================================
# ❌ No forzamos redirecciones, Railway ya usa HTTPS a nivel de proxy.
# Pero sí agregamos cabeceras para evitar que el navegador lo trate como inseguro.
@app.middleware("http")
async def enforce_https_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# =======================================================
# 🌐 CORS
# =======================================================
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://my-dashboard-production-ecd1.up.railway.app",
    "https://my-dashboard-production-cd1a.up.railway.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =======================================================
# 📦 Rutas
# =======================================================
app.include_router(clientes.router)
app.include_router(catalogos.router)
app.include_router(sesiones.router)
app.include_router(sesiones_fuentes.router)
app.include_router(sesiones_fechas.router)
app.include_router(sesiones_entregables.router)
app.include_router(entes.router)
app.include_router(ente_tipo.router)
app.include_router(servidores_publicos.router)
app.include_router(servidor_publico.router)
app.include_router(sesiones_fechas_pivot.router)
app.include_router(ente_servidor_publico.router)
app.include_router(rubro.router)
app.include_router(proveedor.router)
app.include_router(entidad_federativa.router)
app.include_router(usuarios.router)
app.include_router(proceso_seguimiento_ente.router)
app.include_router(proceso_seguimiento_presupuesto_ente.router)
app.include_router(proceso_seguimiento_presupuesto_proveedor_ente.router)
app.include_router(catalogos_ente.router)
app.include_router(catalogos_servidor_publico.router)
app.include_router(catalogos_sesion_numero.router)
app.include_router(proceso_enum_tipo_licitacion.router)
app.include_router(partidas.router)
app.include_router(fuentes_financiamiento.router)
app.include_router(presupuesto_proveedor.router)
# =======================================================
# 🔍 Verificación
# =======================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "🚀 Backend activo con HTTPS estable y CORS configurado correctamente",
    }