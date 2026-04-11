"""
SKILL CREADOR - Meta-skill que crea nuevas skills
===================================================

Esta skill es capaz de generar nuevas skills para el Super Agente MCP.
Crea skills con estructura completa:
- MEMORIA_CONSOLIDADA con delimitadores
- Integración con engram.recuperar_engramas()
- Uso de config_lm.complete()
- Registro automático en skill_index.json

Uso:
    crear_skill(nombre, descripcion, dominio, parametros)
"""

import os
import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
INDEX_FILE = SKILL_DIR.parent / "skill_index.json"


TEMPLATES = {
    "webdev": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
    Eres un experto en {dominio}.
    Reglas:
    1. Genera codigo de alta calidad
    2. Sigue las mejores practicas del dominio
    3. Incluye comentarios explicativos
    """

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": "{prompt_template}"}}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}"
''',
    "gamedev": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
    Eres un experto en desarrollo de juegos {dominio}.
    Reglas:
    1. Optimizado para rendimiento
    2. Codigo limpio y mantenible
    3. Incluye manejo de errores
    """

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": "{prompt_template}"}}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}"
''',
    "generic": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
    Eres un asistente experto en {dominio}.
    """

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": "{prompt_template}"}}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}"
''',
}


def crear_skill(
    nombre: str,
    descripcion: str,
    dominio: str = "generic",
    parametros: list = None,
    funcion: str = None,
) -> str:
    """
    Crea una nueva skill para el Super Agente.

    Args:
        nombre: Nombre de la skill (snake_case, ej: "mi_skill")
        descripcion: Descripción de qué hace la skill
        dominio: "webdev", "gamedev", "gitdev", "estructura", "generic"
        parametros: Lista de parámetros de la función principal
        funcion: Nombre de la función principal (opcional, deduce de nombre)

    Returns:
        Mensaje con el resultado de la creación
    """
    try:
        nombre = nombre.lower().strip().replace(" ", "_")

        if funcion is None:
            funcion = nombre.replace("-", "_")

        if parametros is None:
            parametros = ["descripcion: str"]

        # Determinar dominio y carpeta
        dominio = dominio.lower().strip()
        if dominio in ["web", "frontend", "backend"]:
            dominio = "webdev"
        elif dominio in ["game", "juego", "pygame"]:
            dominio = "gamedev"
        elif dominio in ["git", "github"]:
            dominio = "gitdev"

        carpeta_dominio = {
            "webdev": "webdev",
            "gamedev": "gamedev",
            "gitdev": "gitdev",
            "estructura": ".",
            "generic": "webdev",
        }.get(dominio, "webdev")

        if carpeta_dominio == ".":
            archivo_skill = SKILL_DIR / f"{nombre}.py"
        else:
            archivo_skill = SKILL_DIR / carpeta_dominio / f"{nombre}.py"

        if archivo_skill.exists():
            return f"Ya existe una skill con ese nombre: {archivo_skill}"

        # Obtener template
        template = TEMPLATES.get(dominio, TEMPLATES["generic"])

        # Preparar parámetros
        params_def = ", ".join(parametros)
        prompt_template = "{descripcion}"

        # Generar código
        codigo = template.format(
            nombre=nombre,
            funcion=funcion,
            descripcion=descripcion,
            dominio=dominio,
            params_def=params_def,
            prompt_template=prompt_template,
        )

        # Escribir archivo
        with open(archivo_skill, "w", encoding="utf-8") as f:
            f.write(codigo)

        # Actualizar índice
        _actualizar_indice(
            nombre, descripcion, dominio, str(archivo_skill), funcion, parametros
        )

        return f"Skill '{nombre}' creada exitosamente en {archivo_skill}\nRegistrada en skill_index.json"

    except Exception as e:
        return f"Error al crear skill: {str(e)}"


def _actualizar_indice(
    nombre: str,
    descripcion: str,
    dominio: str,
    archivo: str,
    funcion: str,
    parametros: list,
):
    """Actualiza el índice de skills."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        index["skills"].append(
            {
                "name": nombre,
                "description": descripcion,
                "dominio": dominio,
                "archivo": archivo,
                "funcion": funcion,
                "parametros": parametros,
            }
        )

        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error actualizando índice: {e}")


def listar_skills() -> str:
    """Lista todas las skills disponibles."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        resultado = ["Skills disponibles:"]
        for skill in index["skills"]:
            resultado.append(f"- {skill['name']}: {skill['description']}")

        return "\n".join(resultado)
    except Exception as e:
        return f"Error: {str(e)}"


def buscar_skill(query: str) -> str:
    """Busca skills que coincidan con la query."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        query = query.lower()
        resultados = []

        for skill in index["skills"]:
            if query in skill["name"].lower() or query in skill["description"].lower():
                resultados.append(
                    f"- {skill['name']} ({skill['dominio']}): {skill['description']}"
                )

        if resultados:
            return "Skills encontradas:\n" + "\n".join(resultados)
        return "No se encontraron skills que coincidan"
    except Exception as e:
        return f"Error: {str(e)}"
