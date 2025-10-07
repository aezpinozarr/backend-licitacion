from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import os

from app.routers import (
    clientes, catalogos, sesiones, sesiones_fuentes, sesiones_fechas,
    sesiones_entregables, entes, ente_tipo, servidores_publicos, servidor_publico,
    sesiones_fechas_pivot, ente_servidor_publico, rubro, proveedor, entidad_federativa
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

# =======================================================
# 🔍 Verificación
# =======================================================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "🚀 Backend activo con HTTPS estable y CORS configurado correctamente",
    }