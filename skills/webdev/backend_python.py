import litellm
from skills import engram

def compilar_api_python(descripcion: str) -> str:
    """Especialista en Backend Moderno con Python (FastAPI/Flask/SQLAlchemy)."""
    instrucciones = """
    Eres el 'Backend Python Expert'.
    - Regla 1: Construyes APIs RESTFul rápidas usando FastAPI o Flask (prioriza FastAPI).
    - Regla 2: Siempre consideras la seguridad (CORS, inyección SQL).
    - Regla 3: Si se pide base de datos, usa SQLAlchemy o SQLModel puro.
    Devuelve estrictamente solo el código de la implementación, sin Markdown si no se pide explícitamente.
    """
    
    memorias = engram.recuperar_engramas("python_backend")
    if "No hay memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\nLecciones técnicas del usuario:\n{memorias}"
        
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en Backend Python: {str(e)}"
