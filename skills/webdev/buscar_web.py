import litellm
from skills import engram, config_lm
from ddgs import DDGS

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "buscar_web"


def buscar_web(query: str, max_resultados: int = 5) -> str:
    """
    Busca información en la web usando múltiples motores de búsqueda.
    Retorna resultados que gemma puede resumir para el usuario.

    Args:
        query: La pregunta o tema a buscar
        max_resultados: Número de resultados a retornar (default 5)

    Returns:
        Resultados de búsqueda formateados para análisis
    """
    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(
                query, max_results=max_resultados, backend="duckduckgo"
            )

        if not resultados:
            return f"No se encontraron resultados para: {query}"

        # Formatear resultados para que gemma los resuma
        salida = []
        for i, r in enumerate(resultados, 1):
            titulo = r.get("title", "Sin título")
            cuerpo = r.get("body", "Sin descripción")
            enlace = r.get("href", "")
            salida.append(f"{i}. {titulo}\n   {cuerpo[:300]}...\n   Fuente: {enlace}")

        return "RESULTADOS DE BÚSQUEDA:\n\n" + "\n\n".join(salida)

    except Exception as e:
        return f"Error en búsqueda: {str(e)}\n\nIntenta con una consulta diferente o más específica."


def buscar_y_resumir(query: str, max_resultados: int = 5) -> str:
    """
    Busca en la web y usa gemma para resumir los resultados automáticamente.
    Útil cuando quieres una respuesta directa en lugar de los raw resultados.
    """
    resultados = buscar_web(query, max_resultados)

    if "Error" in resultados or "No se encontraron" in resultados:
        return resultados

    # Usar gemma para resumir
    prompt = f"""
Eres un asistente que resume resultados de búsqueda web.
Responde de forma clara y concisa en español de España.

Resultados de búsqueda para "{query}":
{resultados}

Proporciona un resumen de 2-3 párrafos con la información más relevante.
Si la información no es suficiente, indica que se necesita más contexto.
"""

    try:
        response = config_lm.complete(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error al resumir: {str(e)}\n\nAquí están los resultados originales:\n{resultados}"
