import os
import re
import litellm
from pathlib import Path

def mapear_estructura(directorio_base: str, nivel_maximo: int = 3) -> str:
    """
    Genera un mapa visual (árbol) de un directorio.
    Ignora carpetas pesadas o inútiles como node_modules, .venv, .git, etc.
    """
    ruta_base = Path(directorio_base)
    if not ruta_base.exists() or not ruta_base.is_dir():
        return f"Error: La ruta {directorio_base} no existe."
        
    carpetas_ignoradas = {".git", "node_modules", ".venv", "__pycache__", "dist", "build", ".next"}
    
    arbol = []
    
    def construir_arbol(ruta_actual: Path, nivel: int = 0):
        if nivel >= nivel_maximo:
            return
            
        try:
            elementos = sorted(ruta_actual.iterdir(), key=lambda x: (x.is_file(), x.name))
        except PermissionError:
            return
            
        for elemento in elementos:
            if elemento.name in carpetas_ignoradas:
                continue
                
            sangria = "  " * nivel + "|-- "
            
            if elemento.is_dir():
                arbol.append(f"{sangria}📂 {elemento.name}/")
                construir_arbol(elemento, nivel + 1)
            else:
                arbol.append(f"{sangria}📄 {elemento.name}")

    arbol.append(f"📂 {ruta_base.name}/")
    construir_arbol(ruta_base)
    
    return "\n".join(arbol)

def buscar_dependencias(ruta_archivo: str) -> str:
    """
    Busca de qué otros archivos y librerías depende un archivo concreto mediante lectura rápida.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        imports_py = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_\.]+)', contenido, re.MULTILINE)
        imports_js = re.findall(r'(?:import|require)[^\'"]*[\'"]([^\'"]+)[\'"]', contenido)
        
        todas = set(imports_py + imports_js)
        if not todas:
            return f"No se encontraron dependencias explícitas en {ruta_archivo}."
            
        return f"Dependencias de {ruta_archivo}:\n- " + "\n- ".join(sorted(todas))
    except Exception as e:
        return f"Error leyendo dependencias: {str(e)}"

def resumir_codigo_con_ia(ruta_archivo: str, notas_extra: str = "") -> str:
    """
    Resumidor Mágico. Lee código extenso y llama a una API gratuita para resumirlo
    ahorrando tokens al IDE.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
            
        if not codigo.strip():
            return "Archivo vacío."
            
        prompt = f"Eres un Arquitecto de Software. Haz un resumen extremadamente breve de para qué sirve este código sin detallar paso a paso. Notas extra del usuario: {notas_extra}\n\nCódigo:\n{codigo}"
        
        response = litellm.completion(
            model="groq/llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        return response.choices[0].message.content
        
    except Exception as e:
        # Aquí capturamos si falta la clave en .env, etc.
        return f"Error del resumidor (¿Tienes tu clave GROQ_API_KEY en .env?): {str(e)}"
