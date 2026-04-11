import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "backend_python"

def compilar_api_python(descripcion: str) -> str:
    """Especialista en Backend Moderno con Python (FastAPI/Flask/SQLAlchemy)."""
    instrucciones = """
    Eres el 'Backend Python Expert'.
    - Regla 1: Construyes APIs RESTFul rápidas usando FastAPI o Flask (prioriza FastAPI).
    - Regla 2: Siempre consideras la seguridad (CORS, inyección SQL).
    - Regla 3: Si se pide base de datos, usa SQLAlchemy o SQLModel puro.
    """

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\n--- LECCIONES PERMANENTES APRENDIDAS ---\n{LECCIONES_CONSOLIDADAS.strip()}\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "No hay memorias" not in memorias and "Error" not in memorias and "No hay engramas" not in memorias:
        instrucciones += f"\n--- LECCIONES TEMPORALES RECIENTES ---\n{memorias}\n"

    try:
        response = config_lm.complete(
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en Backend Python: {str(e)}"
