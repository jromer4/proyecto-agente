import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from skills import architect, engram
from skills.gamedev import pygame_renderer, pygame_combat, pygame_entities
from skills.webdev import react_expert, css_ninja, backend_python, backend_php
from skills.gitdev import github_master

# Cargar las claves secretas del archivo .env
load_dotenv()

# Crear nuestro Servidor "El Orquestador"
mcp = FastMCP("SuperAgente")

# ==========================================
# TOOLS DEL SERVIDOR MCP
# ==========================================


@mcp.tool()
def hello_world(nombre: str) -> str:
    return f"Hola {nombre}! El Super Agente esta en linea."


@mcp.tool()
def crear_componente_react(
    nombre: str, descripcion: str, usar_tailwind: bool = True
) -> str:
    return react_expert.generar_componente_react(nombre, descripcion, usar_tailwind)


@mcp.tool()
def generar_css_ninja(descripcion: str, usar_tailwind: bool = True) -> str:
    return css_ninja.generar_css(descripcion, usar_tailwind)


@mcp.tool()
def programar_backend_python(descripcion: str) -> str:
    return backend_python.compilar_api_python(descripcion)


@mcp.tool()
def programar_backend_php(descripcion: str) -> str:
    return backend_php.compilar_php(descripcion)


@mcp.tool()
def mapear_estructura(directorio: str, nivel_maximo: int = 3) -> str:
    return architect.mapear_estructura(directorio, nivel_maximo)


@mcp.tool()
def buscar_dependencias(ruta_archivo: str) -> str:
    return architect.buscar_dependencias(ruta_archivo)


@mcp.tool()
def resumir_codigo_con_ia(ruta_archivo: str, notas_extra: str = "") -> str:
    return architect.resumir_codigo_con_ia(ruta_archivo, notas_extra)


# ==========================================
# MEMORIA Y PROCEDIMIENTOS
# ==========================================


@mcp.tool()
def guardar_engrama(
    aprendizaje: str, tipo: str = "global", proyecto: str | None = None
) -> str:
    """
    Guarda un aprendizaje en la memoria.

    Tipos:
    - "global": Aplica siempre
    - "proyecto": Solo para el proyecto actual
    - "procedimiento": Decision tecnica que aplica a todos los proyectos
    """
    return engram.guardar_engrama(aprendizaje, tipo, proyecto)


@mcp.tool()
def guardar_procedimiento(titulo: str, decision: str, contexto: str = "") -> str:
    """
    Guarda una decision tecnica que aplica a TODOS los proyectos.
    Esto economiza tokens a largo plazo - se guarda una vez, se usa siempre.
    """
    return engram.guardar_procedimiento(titulo, decision, contexto)


@mcp.tool()
def recordar_memorias(skill: str | None = None, proyecto: str | None = None) -> str:
    """Devuelve engramas: globales, procedimientos y del proyecto actual."""
    return engram.recuperar_engramas(skill, proyecto)


@mcp.tool()
def ver_procedimientos() -> str:
    """Devuelve todos los procedimientos guardados."""
    return engram.recuperar_procedimientos()


@mcp.tool()
def ver_contexto() -> str:
    """Muestra el estado actual de la memoria."""
    return engram.ver_contexto()


@mcp.tool()
def quien_eres() -> str:
    return (
        "IDENTIDAD: Super Agente MCP (Orquestador de Enjambre)\n"
        "PROPOSITO: Asistencia experta en desarrollo de software.\n\n"
        "MEMORIA:\n"
        "- Engramas globales y de proyecto\n"
        "- Procedimientos (decisiones tecnicas universales)\n\n"
        "ENJAMBRE:\n"
        "- WebDev: React Expert, CSS Ninja, Backend Python/PHP\n"
        "- GameDev: Pygame Renderer, Combat, Entities\n"
        "- GitDev: GitHub Master\n"
        "- Estructura: Mapear, Dependencias, Resumir\n\n"
        "Jose: usa 'ver_contexto' para ver el estado actual."
    )


# ==========================================
# ORQUESTADOR (gemma + Groq)
# ==========================================


@mcp.tool()
def orquestar(mensaje: str) -> str:
    """
    Orquestador optimizado para economar tokens:
    1. Gemma (LM Studio) detecta la skill necesaria
    2. Gemma prepara contexto resumido
    3. Groq hace el trabajo pesado
    """
    from skills import config_lm

    return config_lm.orquestar(mensaje)


# ==========================================
# ENJAMBRE: GIT DEV & GAME DEV
# ==========================================


@mcp.tool()
def agente_github_master(peticion: str) -> str:
    return github_master.asesorar_github(peticion)


@mcp.tool()
def agente_render_pixelart(peticion: str) -> str:
    return pygame_renderer.generar_codigo_grafico(peticion)


@mcp.tool()
def agente_matematico_rpg(peticion: str) -> str:
    return pygame_combat.generar_matematicas_combate(peticion)


@mcp.tool()
def agente_entidades_masivas(peticion: str) -> str:
    return pygame_entities.generar_logica_entidades(peticion)


import sys

if __name__ == "__main__":
    print("Iniciando Super Agente MCP...", file=sys.stderr)
    mcp.run(transport="stdio")
