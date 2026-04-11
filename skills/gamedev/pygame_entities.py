import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "pygame_entities"

def generar_logica_entidades(descripcion: str) -> str:
    """Especialista en Enemigos, IA Flocking y Colisiones Pygame."""
    instrucciones = """
    Eres el 'Pygame Entities Expert'. Tu único trabajo es escribir lógica sobre clases de entidades.
    - REGLA DE RENDIMIENTO PARA ROGUELIKES: Como puede haber 400 enemigos en pantalla simultáneos, NUNCA uses cálculos matemáticos complejos O(N^2) para moverlos.
    - Usa 'pygame.sprite.Group' y optimización de colisiones usando Quadtrees o Hash Grids espaciales si el usuario te pide manejo masivo.
    - Los enemigos siempre persiguen al jugador de la forma más barata para el procesador (vectores simples).
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
        return f"Error en Pygame_Entities: {str(e)}"
