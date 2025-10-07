from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# ❌ Quitamos HTTPSRedirectMiddleware porque Railway ya fuerza HTTPS automáticamente
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.routers import (
    clientes,
    catalogos,
    sesiones,
    sesiones_fuentes,
    sesiones_fechas,
    sesiones_entregables,
    entes,
    ente_tipo,
    servidores_publicos,
    servidor_publico,
    sesiones_fechas_pivot,
    ente_servidor_publico,
    rubro,
    proveedor,
    entidad_federativa,
)
from app.config import settings

app = FastAPI()

# ================================
# ✅ Configuración de CORS
# ================================
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

# ================================
# 📦 Rutas principales
# ================================
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

# ================================
# 🔍 Verificación rápida
# ================================
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend conectado correctamente 🚀"}