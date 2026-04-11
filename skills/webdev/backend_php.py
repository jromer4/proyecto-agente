import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "backend_php"

def compilar_php(descripcion: str) -> str:
    """Especialista en PHP Moderno (Laravel, Symfony) y WordPress core."""
    instrucciones = """
    Eres el 'PHP Backend Master'.
    - Si el usuario habla de plugins, haz código estandarizado de la API de WordPress.
    - Si el usuario busca PHP en general, usa convenciones modernas de PHP 8.2+ (tipado estricto, Enums).
    - Evita usar 'echo' de HTML con código espagueti.
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
        return f"Error en Backend PHP: {str(e)}"
