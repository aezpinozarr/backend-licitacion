from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import (
    clientes, catalogos, sesiones, sesiones_fuentes, sesiones_fechas,
    sesiones_entregables, entes, ente_tipo, servidores_publicos, servidor_publico,
    sesiones_fechas_pivot, ente_servidor_publico, rubro, proveedor, entidad_federativa
)

# ======================================
# 🌐 Middleware personalizado HTTPS
# ======================================
class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Si la conexión viene por HTTP, redirigir a HTTPS manualmente
        if request.url.scheme == "http":
            https_url = request.url.replace(scheme="https")
            return RedirectResponse(url=str(https_url))
        return await call_next(request)

# ======================================
# 🚀 Inicialización de la app
# ======================================
app = FastAPI(title="Backend Licitación", version="1.0.0")

# ✅ Añadir middleware para forzar HTTPS
app.add_middleware(ForceHTTPSMiddleware)

# ======================================
# 🌍 Configuración de CORS
# ======================================
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

# ======================================
# 🧩 Rutas
# ======================================
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

# ======================================
# 🩵 Ruta raíz
# ======================================
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend conectado correctamente 🚀 (con HTTPS forzado)"}