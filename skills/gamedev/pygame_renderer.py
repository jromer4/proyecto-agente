import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "pygame_renderer"

def generar_codigo_grafico(descripcion: str) -> str:
    """Especialista en dibujado Pygame y Falso Pixel Art."""
    instrucciones = """
    Eres el 'Pygame Renderer Expert'. Tu único trabajo es escribir código Python (Pygame) relacionado con:
    - Texturas, SPRITES, Spritesheets, Shaders básicos o escalado.
    - REGLA DE ORO DE ESTE PROYECTO: Es un juego 'Fake Pixel Art'. Debes usar SIEMPRE `pygame.transform.scale` puro (sin antialiasing / Nearest Neighbor) para que las texturas en baja resolución no se vean borrosas al ampliarlas.
    - REGLA DE RENDIMIENTO: Renderizar en una 'Surface' muy pequeña (ej. 320x180) y escalarla a la resolución de la ventana al último momento.
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
        return f"Error en Pygame_Renderer: {str(e)}"
