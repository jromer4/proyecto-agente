import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "pygame_combat"

def generar_matematicas_combate(descripcion: str) -> str:
    """Especialista en RPG, daño, tienda y balanceo matemático."""
    instrucciones = """
    Eres el 'Pygame Combat Expert'. Tu único trabajo es escribir código de lógica pura (nada de gráficos o pygame draws) relacionado con:
    - Fórmulas de combate (DPS, vida, armadura, penetración mágica).
    - Generación aleatoria de objetos para una tienda entre oleadas y cálculo de oro.
    - Balancear la dificultad (curvas exponenciales de HP del enemigo según el minuto de la partida).
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
        return f"Error en Pygame_Combat: {str(e)}"
