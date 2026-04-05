import litellm
from skills import engram

def generar_codigo_grafico(descripcion: str) -> str:
    """Especialista en dibujado Pygame y Falso Pixel Art."""
    instrucciones = """
    Eres el 'Pygame Renderer Expert'. Tu único trabajo es escribir código Python (Pygame) relacionado con:
    - Texturas, SPRITES, Spritesheets, Shaders básicos o escalado.
    - REGLA DE ORO DE ESTE PROYECTO: Es un juego 'Fake Pixel Art'. Debes usar SIEMPRE `pygame.transform.scale` puro (sin antialiasing / Nearest Neighbor) para que las texturas en baja resolución no se vean borrosas al ampliarlas.
    - REGLA DE RENDIMIENTO: Renderizar en una 'Surface' muy pequeña (ej. 320x180) y escalarla a la resolución de la ventana al último momento.
    Devuelve solo código puro, sin explicaciones.
    """
    
    memorias = engram.recuperar_engramas("graficos")
    if "No hay memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\nLecciones previas del usuario:\n{memorias}"
        
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en Pygame_Renderer: {str(e)}"
