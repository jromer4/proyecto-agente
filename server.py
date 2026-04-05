import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from skills import coder, architect, engram
from skills.gamedev import pygame_renderer, pygame_combat, pygame_entities

# 1. Cargar las claves secretas del archivo .env
load_dotenv()

# 2. Crear nuestro Servidor "El Orquestador"
mcp = FastMCP("SuperAgente")

# ==========================================
# REGISTRO DE SKILLS (HERRAMIENTAS / TOOLS)
# ==========================================

@mcp.tool()
def hello_world(nombre: str) -> str:
    """Una tool de ejemplo básica para comprobar que el servidor funciona."""
    return f"¡Hola {nombre}! El Súper Agente está en línea y funcionando."

@mcp.tool()
def crear_componente_react(nombre: str, descripcion: str, usar_tailwind: bool = True) -> str:
    """Pídele a nuestro nuevo Ingeniero React Expert que programe por su cuenta un componente funcional complejo desde cero, con Tailwind y TSX, sin que tu IDE principal tenga que gastar sus tokens."""
    return coder.generar_componente_react(nombre, descripcion, usar_tailwind)

@mcp.tool()
def mapear_estructura(directorio: str, nivel_maximo: int = 3) -> str:
    """Pídele al supervisor que genere un árbol visual o mapa de carpetas de un directorio dado, para orientarte. Ignora automáticamente carpetas pesadas (.git, node_modules)."""
    return architect.mapear_estructura(directorio, nivel_maximo)

@mcp.tool()
def buscar_dependencias(ruta_archivo: str) -> str:
    """Escanea rápidamente el código para extraer qué dependencias (imports/requires) necesita, sin leer su lógica interna."""
    return architect.buscar_dependencias(ruta_archivo)

@mcp.tool()
def resumir_codigo_con_ia(ruta_archivo: str, notas_extra: str = "") -> str:
    """¡Resumidor Mágico! Envíale un archivo gigantesco y Llama3/Groq te contestarán con un párrafo de 5 líneas explicando para qué sirve, ahorrando así millas de tokens al IDE."""
    return architect.resumir_codigo_con_ia(ruta_archivo, notas_extra)

@mcp.tool()
def memorizar(categoria: str, leccion: str) -> str:
    """Invoca el sistema ENGRAM para que el agente aprenda y recuerde una regla permanente o una instrucción vital de proyecto (ej: 'Utiliza siempre variables en snake_case'). Usa esto cuando el jefe te corrija sobre algo general."""
    return engram.guardar_engrama(categoria, leccion)

@mcp.tool()
def recordar_memorias(categoria: str | None = None) -> str:
    """Revisa el sistema ENGRAM para ver las reglas pasadas enseñadas por el usuario, sus preferencias base de UI/UX, o peculiaridades arquitectónicas guardadas."""
    return engram.recuperar_engramas(categoria)

# ==========================================
# ENJAMBRE: GAME DEV (ROGUELIKE PYGAME)
# ==========================================

@mcp.tool()
def agente_render_pixelart(peticion: str) -> str:
    """USA SOLO ESTE AGENTE cuando necesites dibujar cosas en pantalla, escalar gráficos, shaders, o mantener el modo Fake Pixel Art sin antialiasing en Pygame."""
    return pygame_renderer.generar_codigo_grafico(peticion)

@mcp.tool()
def agente_matematico_rpg(peticion: str) -> str:
    """USA SOLO ESTE AGENTE cuando necesites fórmulas de daño, vida, armadura, y cálculo matemático de tiendas u oro. (No dibuja, solo hace lógica matemática pura)."""
    return pygame_combat.generar_matematicas_combate(peticion)

@mcp.tool()
def agente_entidades_masivas(peticion: str) -> str:
    """USA SOLO ESTE AGENTE cuando necesites crear la lógica básica, movimiento inteligente hacia el jugador y sistemas de colisión eficientes para cientos de oleadas de enemigos simultáneos."""
    return pygame_entities.generar_logica_entidades(peticion)

import sys
if __name__ == "__main__":
    print("Iniciando el Servidor Súper Agente MCP...", file=sys.stderr)
    # FastMCP facilita muchísimo ejecutar el servidor listo para que el IDE lo lea.
    # El transporte 'stdio' es la forma en la que los IDEs se comunican con MCP.
    mcp.run(transport='stdio')
