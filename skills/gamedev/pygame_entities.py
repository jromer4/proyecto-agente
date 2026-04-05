import litellm
from skills import engram

def generar_logica_entidades(descripcion: str) -> str:
    """Especialista en Enemigos, IA Flocking y Colisiones Pygame."""
    instrucciones = """
    Eres el 'Pygame Entities Expert'. Tu único trabajo es escribir lógica sobre clases de entidades.
    - REGLA DE RENDIMIENTO PARA ROGUELIKES: Como puede haber 400 enemigos en pantalla simultáneos, NUNCA uses cálculos matemáticos complejos O(N^2) para moverlos.
    - Usa 'pygame.sprite.Group' y optimización de colisiones usando Quadtrees o Hash Grids espaciales si el usuario te pide manejo masivo.
    - Los enemigos siempre persiguen al jugador de la forma más barata para el procesador (vectores simples).
    Devuelve solo código puro, sin explicaciones.
    """
    
    memorias = engram.recuperar_engramas("entidades")
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
        return f"Error en Pygame_Entities: {str(e)}"
