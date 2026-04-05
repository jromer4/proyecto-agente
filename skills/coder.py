import litellm

def generar_componente_react(nombre: str, descripcion: str, usar_tailwind: bool = True) -> str:
    """
    Skill experta en crear Componentes de React súper profesionales (TSX).
    Aplica las mejores prácticas (hooks funcionales, sin clases, código modular).
    """
    try:
        instrucciones_base = """
        Eres un Ingeniero Frontend Principal Web (React Expert).
        Reglas estrictas para el código que vas a generar:
        1. Escribe componentes funcionales en TypeScript (TSX).
        2. Usa hooks modernos (useState, useEffect) correctamente.
        3. Nunca uses código Legacy ni clases.
        4. Haz que la estructura HTML sea muy semántica.
        5. IMPORTANTE: Devuelve EXCLUSIVAMENTE el bloque de código final. Sin explicaciones previas ni posteriores, listo para integrarse.
        """
        
        if usar_tailwind:
            instrucciones_base += "6. Utiliza clases modernas de Tailwind CSS en las capas de estilo (className) para hacerlo hermoso.\n"
            
        from skills import engram
        memorias_activas = engram.recuperar_engramas()
        if "No hay memorias" not in memorias_activas and "Error" not in memorias_activas:
            instrucciones_base += f"\n--- RECUERDA TUS ENGRAMAS (LECCIONES PASADAS) ---\nEl usuario te ha corregido y enseñado en el pasado. Debes cumplir STRICTAMENTE estas reglas que tiene registradas a fuego en tu memoria:\n{memorias_activas}\n"
            
        prompt = f"Tu tarea urgente: Crea el componente React llamado '{nombre}'.\nEsto es lo que necesito: {descripcion}"
        
        response = litellm.completion(
            model="groq/llama3-8b-8192", 
            messages=[
                {"role": "system", "content": instrucciones_base.strip()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600 
        )
        return response.choices[0].message.content
        
    except litellm.exceptions.AuthenticationError:
        return "Error 401: El Especialista en React no ha podido conectarse a la nube. Recuerda conseguir una clave gratis en Groq y ponerla en tu archivo .env como GROQ_API_KEY."
    except Exception as e:
        return f"Error en el React Expert: {str(e)}"
