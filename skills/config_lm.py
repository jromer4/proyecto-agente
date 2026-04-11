import os
import json
import litellm
from pathlib import Path
from skills import engram
from dotenv import load_dotenv

load_dotenv()

# Rutas
PROJECT_DIR = Path(__file__).parent.parent
SKILL_INDEX_FILE = PROJECT_DIR / "skill_index.json"

# Modelos disponibles
LM_STUDIO_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "")

GROQ_MODEL = "groq/llama-3.1-8b-instant"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

PROVEEDOR_POR_DEFECTO = "openrouter"


def _leer_skill_index():
    """Lee el índice de skills disponibles."""
    try:
        with open(SKILL_INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"skills": []}


def _detectar_skill_desde_indice(mensaje: str) -> dict:
    """
    Usa gemma con el índice completo de skills para decidir cuál usar.
    Returns: {"skill": nombre, "match": True/False}
    """
    if not LM_STUDIO_MODEL:
        return {"skill": None, "match": False, "razon": "Sin LM Studio"}

    index = _leer_skill_index()
    skills_info = "\n".join(
        [f"- {s['name']}: {s['description']}" for s in index.get("skills", [])]
    )

    prompt = f"""
Analiza esta peticion y determina si hay una skill que coincida.
Responde en formato: SKILL: nombre_o_NINGUNO

Skills disponibles:
{skills_info}

Peticion: {mensaje}
"""
    try:
        response = litellm.completion(
            model=f"openai/{LM_STUDIO_MODEL}",
            messages=[{"role": "user", "content": prompt}],
            base_url=LM_STUDIO_URL,
            api_key="dummy-key",
            max_tokens=20,
            temperature=0.1,
        )
        resultado = response.choices[0].message.content.strip().upper()

        if "NINGUNO" in resultado or "NINGUNA" in resultado:
            return {
                "skill": None,
                "match": False,
                "razon": "No coincide con ninguna skill",
            }

        # Extraer nombre de skill
        skill_name = resultado.replace("SKILL:", "").strip()

        # Verificar que existe en el índice
        for s in index.get("skills", []):
            if (
                s["name"].lower() in skill_name.lower()
                or skill_name.lower() in s["name"].lower()
            ):
                return {"skill": s["name"], "match": True, "razon": "Coincide"}

        return {"skill": None, "match": False, "razon": "Skill no encontrada en índice"}
    except Exception as e:
        return {"skill": None, "match": False, "razon": f"Error: {e}"}


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


def _get_potente_config():
    """Retorna modelo y config del proveedor potente (Groq u OpenRouter)."""
    if PROVEEDOR_POR_DEFECTO == "openrouter" and OPENROUTER_API_KEY:
        return {
            "model": f"openrouter/{OPENROUTER_MODEL}",
            "api_key": OPENROUTER_API_KEY,
            "extra": {
                "extra_headers": {
                    "HTTP-Referer": "https://github.com/jromer4/proyecto-agente"
                }
            },
        }
    elif GROQ_API_KEY:
        return {"model": GROQ_MODEL, "api_key": GROQ_API_KEY, "extra": {}}
    return None


def _cargar_skill_y_engramas(skill_name: str) -> str:
    """Carga la skill específica y recupera sus engramas."""
    # Leer índice para obtener info de la skill
    index = _leer_skill_index()
    skill_info = None
    for s in index.get("skills", []):
        if s["name"] == skill_name:
            skill_info = s
            break

    if not skill_info:
        return ""

    # Cargar engramas específicos de esta skill
    memorias = engram.recuperar_engramas(skill_name)

    return f"""
Skill: {skill_info["name"]}
Descripcion: {skill_info["description"]}

--- MEMORIA DE LA SKILL ---
{memorias}
"""


def ejecutar_con_skill(prompt_usuario: str) -> str:
    """
    Orquestador principal con detección automática de skills.

    Flujo:
    1. Gemma analiza el índice de skills
    2. Decide si hay skill que coincida
    3. Si SÍ: carga skill + engramas -> OpenRouter
    4. Si NO: delegar directamente a OpenRouter
    """
    if not LM_STUDIO_MODEL:
        return "Error: No hay modelo LM Studio configurado"

    # 1. Detectar si hay skill que coincida
    resultado = _detectar_skill_desde_indice(prompt_usuario)

    proveedor = _get_potente_config()
    if not proveedor:
        return "Error: No hay proveedor API configurado"

    # 2. Preparar contexto según corresponda
    if resultado["match"] and resultado["skill"]:
        # Hay skill que coincide - cargar contexto de esa skill
        contexto_skill = _cargar_skill_y_engramas(resultado["skill"])

        system_prompt = f"""
Eres el enjambre Súper Agente MCP. El usuario pide algo que coincide con la skill '{resultado["skill"]}'.

{contexto_skill}

Instrucciones:
- Usa la skill '{resultado["skill"]}' para completar la tarea
- Genera solo el codigo necesario
- Explica brevemente
- Usa español de España
- Llama al usuario por su nombre (Jose)
"""
    else:
        # No hay skill que coincida - delegar directamente
        system_prompt = """
Eres el Súper Agente MCP. El usuario hace una peticion que NO requiere ninguna skill especializada.
Responde directamente de forma util y clara.

Instrucciones:
- Responde de forma util
- Usa español de España
- Llama al usuario por su nombre (Jose)
"""

    # 3. Ejecutar con OpenRouter
    try:
        response = litellm.completion(
            model=proveedor["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario},
            ],
            api_key=proveedor["api_key"],
            **proveedor["extra"],
            max_tokens=1000,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


# Mantener orquestar para compatibilidad
def orquestar(mensaje: str) -> str:
    """Alias de ejecutar_con_skill para compatibilidad."""
    return ejecutar_con_skill(mensaje)


def get_model():
    """Retorna el modelo por defecto (LM Studio si está disponible)."""
    if LM_STUDIO_MODEL:
        return f"openai/{LM_STUDIO_MODEL}"
    proveedor = _get_potente_config()
    return proveedor["model"] if proveedor else GROQ_MODEL


def get_config():
    """Retorna config para completar() que usa LM Studio."""
    if LM_STUDIO_MODEL:
        return {"base_url": LM_STUDIO_URL, "api_key": "dummy-key"}
    return {}


def complete(messages, **kwargs):
    model = get_model()
    extra_config = get_config()
    return litellm.completion(model=model, messages=messages, **extra_config, **kwargs)
