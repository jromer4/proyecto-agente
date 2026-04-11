import os
import litellm
from pathlib import Path
from skills import engram
from dotenv import load_dotenv

load_dotenv()

GROQ_MODEL = "groq/llama-3.1-8b-instant"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LM_STUDIO_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "")


def _detectar_skill(mensaje: str) -> str:
    """Usa gemma (LM Studio) para decidir qué skill usar."""
    if not LM_STUDIO_MODEL:
        return "auto"

    prompt = f"""
Analiza esta peticion y determina que skill usar. Solo una palabra.

Skills: react_expert, css_ninja, backend_python, backend_php, pygame_renderer, pygame_combat, pygame_entities, github_master, general

Peticion: {mensaje}
"""
    try:
        response = litellm.completion(
            model=f"openai/{LM_STUDIO_MODEL}",
            messages=[{"role": "user", "content": prompt}],
            base_url=LM_STUDIO_URL,
            api_key="dummy-key",
            max_tokens=15,
            temperature=0.1,
        )
        skill = response.choices[0].message.content.strip().lower()
        return skill if skill else "general"
    except:
        return "general"


def _preparar_contexto(skill: str, proyecto: str) -> str:
    """Usa gemma para preparar contexto ultra-eficiente para Groq."""
    if not LM_STUDIO_MODEL:
        return ""

    try:
        memorias = engram.recuperar_engramas()
        procedimientos = engram.recuperar_procedimientos()
        proyecto_actual = Path.cwd().name

        prompt = f"""
Resumidor eficiente. Resume solo datos relevantes (max 100 palabras).

Mensaje actual: {skill} / {proyecto_actual}

Memorias: {memorias}
Procedimientos: {procedimientos}

Responde "NINGUNO" si no hay datos relevantes, o resume lo importante.
"""
        response = litellm.completion(
            model=f"openai/{LM_STUDIO_MODEL}",
            messages=[{"role": "user", "content": prompt}],
            base_url=LM_STUDIO_URL,
            api_key="dummy-key",
            max_tokens=120,
            temperature=0.1,
        )
        contexto = response.choices[0].message.content.strip()

        if "NINGUNO" in contexto:
            return ""
        return contexto
    except Exception as e:
        return ""


def _evaluar_necesidad_aprender(resultado: str, mensaje: str) -> bool:
    """Usa gemma para detectar si el resultado merece ser aprendido."""
    if not LM_STUDIO_MODEL:
        return False

    prompt = f"""
Analiza si este resultado contiene algo que deberia aprenderse para futuras ocasiones.
Responde SOLO con "SI" o "NO".

Resultado: {resultado[:200]}
"""
    try:
        response = litellm.completion(
            model=f"openai/{LM_STUDIO_MODEL}",
            messages=[{"role": "user", "content": prompt}],
            base_url=LM_STUDIO_URL,
            api_key="dummy-key",
            max_tokens=5,
            temperature=0.1,
        )
        return "SI" in response.choices[0].message.content.upper()
    except:
        return False


def orquestar(mensaje: str) -> str:
    """
    Orquestador optimizado:
    1. Gemma detecta skill
    2. Gemma prepara contexto resumido (economiza tokens de Groq)
    3. Groq hace el trabajo pesado
    4. Gemma evalua si hay que aprender algo
    """
    if not LM_STUDIO_MODEL:
        return "Error: No hay modelo LM Studio configurado"

    skill = _detectar_skill(mensaje)
    contexto = _preparar_contexto(skill, Path.cwd().name)

    system_prompt = f"""
Eres parte del enjambre Súper Agente MCP. Completa la tarea del usuario.

{contexto}

Instrucciones:
- Genera solo el codigo necesario
- Explica brevemente
- Usa español de España
- Llama al usuario por su nombre (Jose)
"""

    try:
        response = litellm.completion(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje},
            ],
            max_tokens=1000,
            temperature=0.2,
        )
        resultado = response.choices[0].message.content

        # Evaluar si hay que aprender algo (opcional - puede comentarse si slow)
        # if _evaluar_necesidad_aprender(resultado, mensaje):
        #     print(f"  [INFO] La skill {skill} podria beneficiarse de un engrama")

        return resultado
    except Exception as e:
        return f"Error: {e}"


def get_model():
    if LM_STUDIO_MODEL:
        return f"openai/{LM_STUDIO_MODEL}"
    return GROQ_MODEL


def get_config():
    if LM_STUDIO_MODEL:
        return {"base_url": LM_STUDIO_URL, "api_key": "dummy-key"}
    return {}


def complete(messages, **kwargs):
    model = get_model()
    extra_config = get_config()
    return litellm.completion(model=model, messages=messages, **extra_config, **kwargs)
