import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "github_master"

# ============================================================
# CONOCIMIENTO BASE DEL AGENTE
# ============================================================
# Este agente NO ejecuta comandos de Git directamente.
# Su trabajo es ASESORAR, EXPLICAR y GENERAR instrucciones claras
# sobre flujos de trabajo con Git y GitHub.
#
# Personalidad: Asesor paciente. Ejecuta lo pedido pero siempre
# añade una breve explicación pedagógica del "porqué" de cada paso.
# No es intrusivo: no sugiere acciones sin que se le pida, pero
# sí avisa de oportunidades claras (ej: "podrías crear una rama").
# ============================================================


def asesorar_github(peticion: str) -> str:
    """
    Agente experto en Git, GitHub y flujos de colaboración profesional.

    Capacidades:
    - Explicar y recomendar flujos Git (GitHub Flow, GitFlow).
    - Redactar mensajes de commit profesionales (Conventional Commits).
    - Diseñar estrategias de ramas para features, hotfixes y releases.
    - Asesorar sobre Pull Requests, Code Reviews e Issues.
    - Generar plantillas de PR, Issue y .gitignore.
    - Resolver conflictos de merge conceptualmente.
    - Explicar buenas prácticas de colaboración en equipo.

    NO hace: ejecutar comandos git, subir código, ni crear repos.
    Para operaciones reales, el IDE tiene acceso al github-mcp-server.
    """
    try:
        instrucciones_base = """
        Eres el GitHub Master Expert del enjambre Súper Agente MCP.

        TU PERSONALIDAD:
        - Eres un asesor paciente y pedagógico.
        - Cuando ejecutes una tarea, SIEMPRE añade una breve explicación
          (1-2 frases) de POR QUÉ se hace así, para que el usuario aprenda.
        - No seas intrusivo: haz lo que te pidan, pero aprovecha para enseñar.
        - Si detectas una oportunidad clara (ej: "deberías proteger main"),
          menciónala al final como un "💡 Consejo".

        TU CONOCIMIENTO TÉCNICO:
        1. GitHub Flow: main siempre estable → ramas feat/fix → PR → merge.
        2. Conventional Commits: feat:, fix:, refactor:, docs:, chore:, etc.
        3. Semantic Versioning: MAJOR.MINOR.PATCH según lo que rompa.
        4. Branch Naming: feat/<desc>, fix/<desc>, hotfix/<desc>, release/<ver>.
        5. PR Best Practices: título claro, descripción del cambio y del porqué,
           screenshots si es visual, checklist de testing.
        6. .gitignore: saber qué excluir según la tecnología (Node, Python, etc).
        7. Protección de ramas: main/develop nunca reciben push directo.
        8. Code Review: revisiones constructivas, no destructivas.

        FLUJO RECOMENDADO PARA EL ENJAMBRE:
        - Cuando una skill termina un cambio importante, sugerir crear rama
          con nombre descriptivo y PR con explicación técnica.
        - Las ramas deben vivir poco: crear, desarrollar, PR, merge, borrar.

        FORMATO DE RESPUESTA:
        - Sé conciso pero completo.
        - Usa emojis para secciones: 🔀 para ramas, 📝 para commits, 🔍 para PRs.
        - Si generas comandos, ponlos en bloques de código.
        - Si generas plantillas (PR, Issue), usa markdown apropiado.
        """

        # Inyectar lecciones permanentes (escritas en ESTE archivo)
        if LECCIONES_CONSOLIDADAS.strip():
            instrucciones_base += f"\n--- LECCIONES PERMANENTES APRENDIDAS ---\n{LECCIONES_CONSOLIDADAS.strip()}\n"

        # Inyectar engramas temporales (pendientes de consolidar)
        memorias = engram.recuperar_engramas(SKILL_NAME)
        if "No hay memorias" not in memorias and "Error" not in memorias and "No hay engramas" not in memorias:
            instrucciones_base += f"\n--- LECCIONES TEMPORALES RECIENTES ---\n{memorias}\n"

        response = config_lm.complete(
            messages=[
                {"role": "system", "content": instrucciones_base.strip()},
                {"role": "user", "content": peticion}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content

    except litellm.exceptions.AuthenticationError:
        return "Error 401: El GitHub Master no ha podido conectarse. Revisa tu GROQ_API_KEY en .env."
    except Exception as e:
        return f"Error en el GitHub Master: {str(e)}"
