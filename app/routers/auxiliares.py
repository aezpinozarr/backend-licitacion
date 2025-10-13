from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

router = APIRouter(
    prefix="/catalogos/auxiliares",
    tags=["Catálogos - Auxiliares"]
)

def _normaliza_tipo(v: str) -> str:
    # Quita espacios extras y usa mayúsculas para comparar sin problemas
    return (v or "").strip()

@router.get("/", response_model=list[dict])
def obtener_auxiliares(
    p_tipo: str = Query(..., description="Tipo de evento (ej: 'SESION ORDINARIA', 'LICITACION PUBLICA')"),
    db: Session = Depends(get_db)
):
    """
    Devuelve opciones de auxiliares filtradas por 'p_tipo'.

    Preferencia:
      1) Llama a catalogos.sp_auxiliares(:p_tipo) si existe y devuelve
         columnas: id, tipo, valor, clasificacion.
      2) Si falla, consulta directamente la tabla catalogos.auxiliares.
    """
    try:
        tipo = _normaliza_tipo(p_tipo)
        if not tipo:
            raise HTTPException(status_code=400, detail="p_tipo es requerido")

        # 1) Intento vía SP
        try:
            sp = text("SELECT * FROM catalogos.sp_auxiliares(:p_tipo)")
            rows = db.execute(sp, {"p_tipo": tipo}).mappings().all()

            if rows:
                # Normalizamos llaves esperadas
                out = []
                for r in rows:
                    # Soportar diferentes nombres que pueda devolver el SP
                    id_ = r.get("id") or r.get("p_id") or r.get("aux_id")
                    tipo_ = r.get("tipo") or r.get("p_tipo") or r.get("aux_tipo")
                    valor_ = r.get("valor") or r.get("p_valor") or r.get("aux_valor")
                    clasif_ = r.get("clasificacion") or r.get("p_clasificacion") or r.get("aux_clasificacion")

                    if id_ is None or valor_ is None:
                        # Si el SP no devuelve lo esperado, forzamos fallback
                        out = []
                        break

                    out.append({
                        "id": id_,
                        "tipo": tipo_ or tipo,
                        "valor": valor_,
                        "clasificacion": clasif_ or "",
                    })

                if out:
                    return out
            # Si no hubo filas o columnas no coinciden, cae al fallback
        except Exception:
            # Continuar al fallback sin romper
            pass

        # 2) Fallback a tabla directa
        q = text("""
            SELECT id, tipo, valor, clasificacion
            FROM catalogos.auxiliares
            WHERE UPPER(TRIM(tipo)) = UPPER(TRIM(:tipo))
            ORDER BY id
        """)
        rows = db.execute(q, {"tipo": tipo}).mappings().all()

        return [
            {
                "id": r["id"],
                "tipo": r["tipo"],
                "valor": r["valor"],
                "clasificacion": r["clasificacion"],
            }
            for r in rows
        ]

    except HTTPException:
        raise
    except Exception as e:
        print("❌ Error en /catalogos/auxiliares:", e)
        raise HTTPException(status_code=500, detail="Error al obtener auxiliares")