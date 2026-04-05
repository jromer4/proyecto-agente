import litellm
from skills import engram

def generar_matematicas_combate(descripcion: str) -> str:
    """Especialista en RPG, daño, tienda y balanceo matemático."""
    instrucciones = """
    Eres el 'Pygame Combat Expert'. Tu único trabajo es escribir código de lógica pura (nada de gráficos o pygame draws) relacionado con:
    - Fórmulas de combate (DPS, vida, armadura, penetración mágica).
    - Generación aleatoria de objetos para una tienda entre oleadas y cálculo de oro.
    - Balancear la dificultad (curvas exponenciales de HP del enemigo según el minuto de la partida).
    Devuelve solo código puro de Python (clases o funciones), sin texto de relleno.
    """
    
    memorias = engram.recuperar_engramas("combate")
    if "No hay memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\nLecciones base del usuario:\n{memorias}"
        
    try:
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[{"role": "system", "content": instrucciones}, {"role": "user", "content": descripcion}],
            max_tokens=600 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en Pygame_Combat: {str(e)}"
