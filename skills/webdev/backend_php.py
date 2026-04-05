import litellm
from skills import engram

def compilar_php(descripcion: str) -> str:
    """Especialista en PHP Moderno (Laravel, Symfony) y WordPress core."""
    instrucciones = """
    Eres el 'PHP Backend Master'.
    - Si el usuario habla de plugins, haz código estandarizado de la API de WordPress.
    - Si el usuario busca PHP en general, usa convenciones modernas de PHP 8.2+ (tipado estricto, Enums).
    - Evita usar 'echo' de HTML con código espagueti.
    Devuelve solo el código PHP rodeado de los tags correspondientes.
    """
    
    memorias = engram.recuperar_engramas("php")
    if "No hay memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\nPreferencias PHP del usuario:\n{memorias}"
        
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en Backend PHP: {str(e)}"
