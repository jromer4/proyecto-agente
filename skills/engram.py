import json
import os
from datetime import datetime

MEMORIA_FILE = "engramas_agente.json"

def inicializar_memoria():
    """Se asegura de que el archivo del cerebro exista."""
    if not os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
            json.dump({"engramas": []}, f)

def guardar_engrama(categoria: str, aprendizaje: str) -> str:
    """
    Guarda una lección importante para siempre en la memoria del agente.
    """
    try:
        inicializar_memoria()
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        nuevo_engrama = {
            "id": len(db["engramas"]) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "categoria": categoria,
            "aprendizaje": aprendizaje
        }
        db["engramas"].append(nuevo_engrama)
        
        with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
            
        return f"Engrama '{categoria}' guardado con éxito. Nunca lo olvidaré."
    except Exception as e:
        return f"Error guardando engrama: {str(e)}"

def recuperar_engramas(categoria_filtro: str | None = None) -> str:
    """
    Devuelve todos los aprendizajes guardados por el agente.
    """
    try:
        inicializar_memoria()
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            
        si_hay = db["engramas"]
        if not si_hay:
            return "No hay memorias almacenadas todavía."
            
        resultados = []
        for e in si_hay:
            if categoria_filtro and categoria_filtro.lower() not in e["categoria"].lower():
                continue
            resultados.append(f"- [{e['fecha']}] {e['categoria']}: {e['aprendizaje']}")
            
        if not resultados:
            return f"No hay engramas para la categoría '{categoria_filtro}'."
            
        return "Memorias base del usuario:\n" + "\n".join(resultados)
    except Exception as e:
        return f"Error recuperando engramas: {str(e)}"
