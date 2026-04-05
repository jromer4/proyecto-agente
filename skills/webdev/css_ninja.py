import litellm
from skills import engram

def generar_css(descripcion: str, usar_tailwind: bool = True) -> str:
    """Especialista en estilos visuales, Flexbox, Grid y Animaciones Keyframe."""
    instrucciones = "Eres el 'CSS Ninja Expert'. Tu objetivo es diseñar interfaces impresionantes y responsivas.\n"
    if usar_tailwind:
        instrucciones += "Usa exclusivamente utilidades y configuraciones de Tailwind CSS.\n"
    else:
        instrucciones += "Usa CSS puro (Vanilla), CSS Variables, Flexbox, Grid y animaciones complejas.\n"
        
    instrucciones += "Devuelve solo el código final listo para implementar, sin texto de saludo ni explicaciones."
    
    memorias = engram.recuperar_engramas("css")
    if "No hay memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\nLecciones visuales base del usuario:\n{memorias}"
        
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en CSS Ninja: {str(e)}"
