import asyncio
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from skills import coder, architect

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
def generar_codigo(descripcion: str) -> str:
    """Pídele a nuestro empleado programador que escriba código."""
    return coder.generar_codigo(descripcion)

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

import sys
if __name__ == "__main__":
    print("Iniciando el Servidor Súper Agente MCP...", file=sys.stderr)
    # FastMCP facilita muchísimo ejecutar el servidor listo para que el IDE lo lea.
    # El transporte 'stdio' es la forma en la que los IDEs se comunican con MCP.
    mcp.run(transport='stdio')
