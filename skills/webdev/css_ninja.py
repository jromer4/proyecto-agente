import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "css_ninja"

def generar_css(descripcion: str, usar_tailwind: bool = True) -> str:
    """Especialista en estilos visuales, Flexbox, Grid y Animaciones Keyframe."""
    instrucciones = "Eres el 'CSS Ninja Expert'. Tu objetivo es diseñar interfaces impresionantes y responsivas.\n"
    if usar_tailwind:
        instrucciones += "Usa exclusivamente utilidades y configuraciones de Tailwind CSS.\n"
    else:
        instrucciones += "Usa CSS puro (Vanilla), CSS Variables, Flexbox, Grid y animaciones complejas.\n"

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
        return f"Error en CSS Ninja: {str(e)}"
