# Súper Agente MCP

Un Servidor MCP modular para otorgar habilidades especializadas a nuestro IDE 
(Cursor, VSCode, etc.) usando el protocolo Model Context Protocol.

## Estructura
- `server.py`: Orquestador principal.
- `skills/`: Carpeta de sub-agentes especialistas.
  - `coder.py`: Herramientas de generación de código.
  - `architect.py`: Herramientas de arquitectura.
- `.env`: (Oculto) Claves de APIS gratuitas (Groq, Gemini).

## Instalación
1. Crear entorno virtual: `python -m venv .venv`
2. Activar el entorno: `.\.venv\Scripts\activate` (Windows)
3. Instalar librerías: `pip install -r requirements.txt`
