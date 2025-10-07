from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from app.routers import (
    clientes, catalogos, sesiones, sesiones_fuentes, sesiones_fechas,
    sesiones_entregables, entes, ente_tipo, servidores_publicos, servidor_publico,
    sesiones_fechas_pivot, ente_servidor_publico, rubro, proveedor, entidad_federativa
)

# =======================================================
# 🚀 FastAPI app
# =======================================================
app = FastAPI(title="Backend Licitación", version="1.0")

# =======================================================
# ✅ Forzar HTTPS sin loops (manejado manualmente)
# =======================================================
class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Si llega por HTTP, redirigir a HTTPS
        if request.url.scheme == "http":
            url = request.url.replace(scheme="https")
            return RedirectResponse(url=str(url))
        return await call_next(request)

app.add_middleware(ForceHTTPSMiddleware)

# =======================================================
# 🌐 CORS seguro
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
# 📦 Rutas principales
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
# 🔍 Endpoint de prueba
# =======================================================
@app.get("/")
def root():
    return {"status": "ok", "message": "🚀 Backend activo y forzando HTTPS correctamente"}