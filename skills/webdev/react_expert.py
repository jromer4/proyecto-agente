import os
import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "react_expert"

def generar_componente_react(nombre: str, descripcion: str, usar_tailwind: bool = True) -> str:
    """Skill experta en crear Componentes de React súper profesionales (TSX)."""
    try:
        instrucciones_base = """
        Eres un Ingeniero Frontend Principal Web (React Expert).
        Reglas estrictas para el código que vas a generar:
        1. Escribe componentes funcionales en TypeScript (TSX).
        2. Usa hooks modernos (useState, useEffect) correctamente.
        3. Nunca uses código Legacy ni clases.
        4. Haz que la estructura HTML sea muy semántica.
        """

        if usar_tailwind:
            instrucciones_base += "5. Utiliza clases modernas de Tailwind CSS en las capas de estilo (className) para hacerlo hermoso.\n"

        # Inyectar lecciones permanentes (escritas en ESTE archivo)
        if LECCIONES_CONSOLIDADAS.strip():
            instrucciones_base += f"\n--- LECCIONES PERMANENTES APRENDIDAS ---\n{LECCIONES_CONSOLIDADAS.strip()}\n"

        # Inyectar engramas temporales (pendientes de consolidar)
        memorias = engram.recuperar_engramas(SKILL_NAME)
        if "No hay memorias" not in memorias and "Error" not in memorias and "No hay engramas" not in memorias:
            instrucciones_base += f"\n--- LECCIONES TEMPORALES RECIENTES ---\n{memorias}\n"

        prompt = f"Tu tarea urgente: Crea el componente React llamado '{nombre}'.\nEsto es lo que necesito: {descripcion}"

        response = config_lm.complete(
            messages=[
                {"role": "system", "content": instrucciones_base.strip()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600
        )
        return response.choices[0].message.content

    except litellm.exceptions.AuthenticationError:
        return "Error 401: El Especialista en React no ha podido conectarse. Revisa tu GROQ_API_KEY en .env."
    except Exception as e:
        return f"Error en el React Expert: {str(e)}"
