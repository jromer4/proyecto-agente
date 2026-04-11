"""
============================================================
SISTEMA DE MEMORIA EVOLUTIVA V2 - José
============================================================

Tipos de memoria:
1. GLOBAL: Cosas que aplican siempre (idioma, nombre, personalidad)
2. PROYECTO: Cosas específicas de cada proyecto
3. PROCEDIMIENTOS: Decisiones técnicas que aplican a TODOS los proyectos
   (esto es clave para economizar tokens - se guarda una vez, se usa siempre)

El proyecto se detecta automáticamente por la carpeta de trabajo.
============================================================
"""

import json
import os
from datetime import datetime
from pathlib import Path

MEMORIA_FILE = os.path.join(os.path.dirname(__file__), "..", "engramas_agente.json")
PROCEDIMIENTOS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "procedimientos.json"
)


def _detectar_proyecto() -> str:
    """Detecta el proyecto actual por el nombre de la carpeta."""
    try:
        nombre = os.path.basename(os.getcwd()).strip().lower()
        if nombre and nombre not in ("", "c:", "d:", "/", "\\"):
            return nombre
    except Exception:
        pass
    return "global"


def _leer_memoria() -> dict:
    if not os.path.exists(MEMORIA_FILE):
        return {"engramas": []}
    with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _escribir_memoria(db: dict):
    with open(MEMORIA_FILE, "w", encoding="utf-8", ensure_ascii=False) as f:
        json.dump(db, f, indent=4, ensure_ascii=False)


def _leer_procedimientos() -> dict:
    if not os.path.exists(PROCEDIMIENTOS_FILE):
        return {"procedimientos": []}
    with open(PROCEDIMIENTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _escribir_procedimientos(db: dict):
    with open(PROCEDIMIENTOS_FILE, "w", encoding="utf-8", ensure_ascii=False) as f:
        json.dump(db, f, indent=4, ensure_ascii=False)


# ============================================================
# GUARDAR ENGRAMA (tipo: global | proyecto | procedimiento)
# ============================================================


def guardar_engrama(
    aprendizaje: str, tipo: str = "global", proyecto: str | None = None
) -> str:
    """
    Guarda un engrama con tipo específico.

    Tipos:
    - "global": Aplica siempre (idioma, nombre, personalidad)
    - "proyecto": Solo para el proyecto actual o especificado
    - "procedimiento": Aplica a TODOS los proyectos (decisiones técnicas)
    """
    try:
        db = _leer_memoria()
        proyecto_real = (proyecto or _detectar_proyecto()).strip().lower()

        nuevo = {
            "id": len(db["engramas"]) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "tipo": tipo,
            "proyecto": proyecto_real if tipo != "procedimiento" else "TODOS",
            "aprendizaje": aprendizaje,
        }
        db["engramas"].append(nuevo)
        _escribir_memoria(db)

        return f"Engrama guardado: tipo='{tipo}', proyecto='{proyecto_real}'"
    except Exception as e:
        return f"Error: {str(e)}"


def guardar_procedimiento(titulo: str, decision: str, contexto: str = "") -> str:
    """
    Guarda una decisión técnica que aplica a TODOS los proyectos.
    Esto es lo que más ahorra tokens a largo plazo.
    """
    try:
        db = _leer_procedimientos()
        nuevo = {
            "id": len(db["procedimientos"]) + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "titulo": titulo,
            "decision": decision,
            "contexto": contexto,
        }
        db["procedimientos"].append(nuevo)
        _escribir_procedimientos(db)

        return f"Procedimiento guardado: '{titulo}'"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================
# RECUPERAR MEMORIA (filtrado jerárquico optimizado)
# ============================================================


def recuperar_engramas(skill: str | None = None, proyecto: str | None = None) -> str:
    """
    Devuelve engramas filtrados:
    - GLOBAL (siempre)
    - PROCEDIMIENTOS (siempre - clave para economizar)
    - PROYECTO actual (si existe)
    """
    try:
        db = _leer_memoria()
        proyecto_actual = (proyecto or _detectar_proyecto()).strip().lower()

        resultados = []

        for e in db["engramas"]:
            e_tipo = e.get("tipo", "global")
            e_proy = e.get("proyecto", "global").lower()

            if e_tipo in ("global", "procedimiento"):
                etiqueta = "GLOBAL" if e_tipo == "global" else "PROC"
                resultados.append(f"[{etiqueta}] {e['aprendizaje']}")
            elif e_tipo == "proyecto" and e_proy == proyecto_actual:
                resultados.append(f"[PROY:{proyecto_actual}] {e['aprendizaje']}")

        if not resultados:
            return "Sin memorias guardadas."

        return "MEMORIA:\n" + "\n".join(resultados)

    except Exception as e:
        return f"Error: {str(e)}"


def recuperar_procedimientos() -> str:
    """Devuelve todos los procedimientos (aplican a todos los proyectos)."""
    try:
        db = _leer_procedimientos()
        if not db["procedimientos"]:
            return "Sin procedimientos guardados."

        resultados = []
        for p in db["procedimientos"]:
            resultados.append(f"- {p['titulo']}: {p['decision']}")

        return "PROCEDIMIENTOS (aplican a todos los proyectos):\n" + "\n".join(
            resultados
        )
    except Exception as e:
        return f"Error: {str(e)}"


def ver_contexto() -> str:
    """Resumen del estado de memoria."""
    proyecto = _detectar_proyecto()
    db_engramas = _leer_memoria()
    db_proc = _leer_procedimientos()

    globales = sum(1 for e in db_engramas["engramas"] if e.get("tipo") == "global")
    procedimientos = len(db_proc["procedimientos"])
    proyecto_count = sum(
        1
        for e in db_engramas["engramas"]
        if e.get("tipo") == "proyecto" and e.get("proyecto") == proyecto
    )

    return (
        f"Contexto actual:\n"
        f"  Proyecto: {proyecto}\n"
        f"  Engramas globales: {globales}\n"
        f"  Procedimientos: {procedimientos}\n"
        f"  Engramas de proyecto: {proyecto_count}"
    )


# ============================================================
# PREPARAR CONTEXTO PARA DELEGACIÓN (optimizado para Groq)
# ============================================================


def preparar_contexto_para_groq(mensaje: str) -> str:
    """
    Usa gemma para preparar contexto ultra-eficiente antes de delegar a Groq.
    El objetivo es que Groq reciba solo lo necesario - nada de texto innecesario.
    """
    try:
        memorias = recuperar_engramas()
        procedimientos = recuperar_procedimientos()

        prompt = f"""
Resumidor eficiente. Dado este mensaje, resume SOLO los datos relevantes.
Mensaje: {mensaje}
Memorias: {memorias}
Procedimientos: {procedimientos}
Responde en max 80 palabras o "NINGUNO" si no hay datos relevantes.
"""

        from skills import config_lm

        response = config_lm.complete(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.1,
        )

        contexto = response.choices[0].message.content.strip()

        if "NINGUNO" in contexto:
            return ""

        return f"Contexto: {contexto}"

    except Exception as e:
        return ""


def completar(messages, **kwargs):
    """Wrapper para config_lm que usa LM Studio por defecto."""
    from skills import config_lm as clm

    return clm.complete(messages, **kwargs)
