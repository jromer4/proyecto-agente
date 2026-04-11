"""
INSTALADOR DEL SUPER AGENTE MCP
================================
Ejecuta este script en la raíz de tu nuevo proyecto para instalar
el Súper Agente MCP con toda su configuración y memoria.

Uso:
    python D:/josemi/proyecto-agente/instalar_super_agente.py
"""

import os
import shutil
import json
import sys

PROYECTO_ORIGEN = "D:/josemi/proyecto-agente"


def instalar():
    print("=== INSTALADOR SUPER AGENTE MCP ===\n")

    proyecto_actual = os.getcwd()
    print(f"Proyecto: {proyecto_actual}\n")

    # Archivos esenciales que siempre se copian
    archivos_esenciales = [
        ".env",
        "opencode.json",
        "server.py",
        "skill_index.json",
    ]

    # Carpetas que se copian
    carpetas = [
        "skills",
    ]

    # Archivos opcionales (memoria)
    memoria_opcional = [
        "engramas_agente.json",
        "procedimientos.json",
    ]

    print("1. Copiando archivos esenciales...")
    for archivo in archivos_esenciales:
        origen = os.path.join(PROYECTO_ORIGEN, archivo)
        destino = os.path.join(proyecto_actual, archivo)
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"   - {archivo}")
        else:
            print(f"   - {archivo} (no existe)")

    print("\n2. Copiando carpeta skills...")
    origen_skills = os.path.join(PROYECTO_ORIGEN, "skills")
    destino_skills = os.path.join(proyecto_actual, "skills")
    if os.path.exists(origen_skills):
        if os.path.exists(destino_skills):
            print("   - skills/ ya existe, omitiendo")
        else:
            shutil.copytree(origen_skills, destino_skills)
            print("   - skills/")
    else:
        print("   - skills/ no existe")

    print("\n3. Copiando memoria (opcional)...")
    for archivo in memoria_opcional:
        origen = os.path.join(PROYECTO_ORIGEN, archivo)
        destino = os.path.join(proyecto_actual, archivo)
        if os.path.exists(origen):
            respuesta = input(f"   - Copiar {archivo}? (s/n): ").lower().strip()
            if respuesta in ("s", "si", "sí", "y", "yes"):
                shutil.copy2(origen, destino)
                print(f"     Copiado")
            else:
                print(f"     Omitido")
        else:
            print(f"   - {archivo} (no existe)")

    print("\n4. Actualizando rutas en opencode.json...")
    try:
        with open(
            os.path.join(proyecto_actual, "opencode.json"), "r", encoding="utf-8"
        ) as f:
            config = json.load(f)

        python_path = os.path.join(proyecto_actual, ".venv", "Scripts", "python.exe")
        server_path = os.path.join(proyecto_actual, "server.py")

        python_path = python_path.replace("\\", "/")
        server_path = server_path.replace("\\", "/")

        if "mcp" in config and "super-agente" in config["mcp"]:
            config["mcp"]["super-agente"]["command"] = [python_path, server_path]

            with open(
                os.path.join(proyecto_actual, "opencode.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            print(f"   - Python: {python_path}")
            print(f"   - Server: {server_path}")
        else:
            print("   - Estructura de opencode.json no reconocida")
    except Exception as e:
        print(f"   - Error actualizando: {e}")

    print("\n3b. Instalando dependencias del Super Agente MCP...")
    import subprocess

    venv_dir = os.path.join(proyecto_actual, ".venv")
    if not os.path.exists(venv_dir):
        print("   - Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    print("   - Instalando mcp, litellm, python-dotenv...")
    subprocess.run([pip_path, "install", "mcp", "litellm", "python-dotenv"], check=True)

    print("\n" + "=" * 50)
    print("INSTALACION COMPLETA")
    print("=" * 50)
    print("\nPasos siguientes:")
    print("1. Asegúrate de que LM Studio esté corriendo")
    print("2. Reinicia OpenCode y verifica con /mcp")


if __name__ == "__main__":
    instalar()
