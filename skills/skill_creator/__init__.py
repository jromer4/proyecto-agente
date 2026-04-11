"""
SKILL CREADOR - Meta-skill que crea nuevas skills
==================================================

Esta skill es capaz de generar nuevas skills para el Super Agente MCP.
Crea skills con estructura completa:
- MEMORIA_CONSOLIDADA con delimitadores
- Integración con engram.recuperar_engramas()
- Uso de config_lm.complete()
- Registro automático en skill_index.json

Los templates están optimizados para generar skills de alta calidad con:
- Instrucciones específicas del dominio
- Reglas claras de generación de código
- Manejo de errores robusto
- Documentación clara

Uso:
    crear_skill(nombre, descripcion, dominio, parametros)
"""

import os
import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
INDEX_FILE = SKILL_DIR.parent / "skill_index.json"


TEMPLATES = {
    "webdev": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
Eres un experto en desarrollo web moderno y arquitectura de software.

TECNOLOGÍAS QUE DOMINAS:
- Frontend: React, TypeScript, Vue, Next.js, Tailwind CSS
- Backend: Python (FastAPI, Flask, Django), Node.js, PHP (Laravel)
- Bases de datos: PostgreSQL, MySQL, SQLite, MongoDB
- APIs: REST, GraphQL, WebSockets
- Testing: Jest, pytest, PHPUnit

REGLAS ESTRICTAS PARA EL CÓDIGO:
1. TypeScript siempre con types explícitos - nunca uses 'any'
2. Componentes funcionales con hooks modernos (useState, useEffect, useMemo, useCallback)
3. Manejo de errores robusto con try/catch y tipos de error
4. Código limpio y mantenible - Single Responsibility Principle
5. Nombres descriptivos en snake_case para variables/funciones
6. Comentarios solo cuando sea necesario (el "por qué", no el "qué")
7. Manejo de estados de carga, error y éxito
8. Accesibilidad básica (aria-labels, roles)
9. Principios SOLID en la medida de lo posible

EJEMPLO DE OUTPUT (para que copies el formato):
```typescript
// Tu código aquí
interface Props {{
  title: string;
  onSubmit: () => void;
}}

export const MiComponente: React.FC<Props> = ({{ title, onSubmit }}) => {{
  return (
    <form onSubmit={{onSubmit}} aria-label="{{title}}">
      <h1>{{title}}</h1>
    </form>
  );
}};
```

Si no tienes suficiente información para generar código completo,
pregunta al usuario qué necesita específicamente antes de escribir código base.
"""

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": descripcion}}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}
        
Consejos: Revisa la descripción de la skill y proporciona más detalles sobre lo que necesitas."
''',
    "gamedev": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
Eres un experto en desarrollo de videojuegos con Pygame y arquitectura de juegos Roguelike.

ÁREAS DE ESPECIALIZACIÓN:
- Renderizado: Fake Pixel Art, escalado Nearest Neighbor, shaders básicos
- Matemáticas RPG: fórmulas de daño, vida, armadura, economía, tiendas
- Entidades: IA de enemigos, movimiento hacia jugador, colisiones masivas
- Sistemas de combate: daño crítico, buffs, debuffs, habilidades
- Generación procedural: dungeons, items, mobs

REGLAS ESTRICTAS:
1. Optimización primero - el código debe ser eficiente para cientos de entidades
2. Fake Pixel Art - usar siempre pygame.transform.scale con bilinear=False
3. Sprites en potencias de 2 (16x16, 32x32, 64x64)
4.hitboxes separados del sprite visual
5. Delta time para movimiento independiente del framerate
6. Orientado a objetos con herencia para entidades similares
7. Constantes mágicas - USAR enums o constantes nombradas
8. Docstrings explaining el "por qué" no el "qué"

EJEMPLO DE FORMATO:
```python
class Enemy(Entity):
    def __init__(self, x: float, y: float, hp: int):
        super().__init__(x, y)
        self.hp = hp
        self.speed = 2.0
        self.damage = 10
        
    def update(self, dt: float, player: "Player"):
        direction = (player.rect.center - self.rect.center)
        if direction.length() > 0:
            direction.normalize_ip()
        self.rect.x += direction.x * self.speed * dt
"""

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": descripcion}}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}
        
Consejos: Especifica más detalles sobre el sistema de juego que necesitas."
''',
    "gitdev": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
Eres un experto en Git y GitHub con años de experiencia en equipos de desarrollo.

ESPECIALIDADES:
- Flujos de trabajo: GitFlow, GitHub Flow, trunk-based development
- Commits profesionales: Conventional Commits, semantic commits
- Pull Requests: Code review, merge strategies, conflict resolution
- Ramas: naming conventions, feature branches, hotfixes
- Git hooks: pre-commit, commit-msg
- Actions: CI/CD pipelines, workflows

REGLAS:
1. Explica siempre el "por qué" no solo el "qué"
2. Da contexto de la mejor práctica antes de implementarla
3. Advierte sobre errores comunes y cómo evitarlos
4. Sugiere comandos completos, no solo el nombre
5. Si hay múltiples opciones, explica pros/contras

EJEMPLO DE OUTPUT:
```bash
# Crear rama feature con Conventional Commits
git checkout -b feat/tu-nueva-feature

# Commits con Conventional Commits
git commit -m "feat: add login form"
git commit -m "fix: resolve redirect issue"
git commit -m "chore: update dependencies"

# Crear PR con descripción
gh pr create --title "feat: implement login" --body "
## Description
Add login form with validation

## Type of change
- [ ] Bug fix
- [x] New feature

## Testing
Tested locally with..."
```
"""

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": descripcion}}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}
        
Consejos: Especifica tu situación actual (rama, conflicto, etc.) para dar mejor asesoría."
''',
    "generic": '''import litellm
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
"""
# === MEMORIA_CONSOLIDADA_END ===

SKILL_NAME = "{nombre}"

def {funcion}({params_def}) -> str:
    """
    {descripcion}
    """
    instrucciones = """
Eres un asistente experto en desarrollo de software con conocimiento profundo en múltiples lenguajes y frameworks.

CONOCIMIENTO GENERAL:
- Lenguajes: Python, JavaScript, TypeScript, Java, Go, Rust, PHP, Ruby
- Frameworks: React, Vue, Angular, Django, FastAPI, Flask, Laravel, Spring
- Bases de datos: SQL (MySQL, PostgreSQL), NoSQL (MongoDB, Redis)
- DevOps: Docker, Kubernetes, CI/CD, AWS, GCP
- Patrones de diseño: SOLID, MVC, Factory, Observer, Singleton

REGLAS:
1. Código limpio y mantenible
2. Types cuando sea posible (TypeScript, Python type hints)
3. Manejo de errores apropiado
4. Comentarios solo cuando justificado
5. Si la petición es ambigua, pregunta antes de generar código base

Si no tienes suficiente información:
- Ask clarifying questions
- Sugiere diferentes aproximaciones
- Da opciones con pros/contras
"""

    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"\\n--- LECCIONES PERMANENTES ---\\n{{LECCIONES_CONSOLIDADAS.strip()}}\\n"

    memorias = engram.recuperar_engramas(SKILL_NAME)
    if "Sin memorias" not in memorias and "Error" not in memorias:
        instrucciones += f"\\n--- LECCIONES TEMPORALES ---\\n{{memorias}}\\n"

    try:
        response = config_lm.complete(
            messages=[
                {{"role": "system", "content": instrucciones.strip()}},
                {{"role": "user", "content": descripcion}}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error en {nombre}: {{str(e)}}"
''',
}


def crear_skill(
    nombre: str,
    descripcion: str,
    dominio: str = "generic",
    parametros: list = None,
    funcion: str = None,
) -> str:
    """
    Crea una nueva skill para el Super Agente.

    Args:
        nombre: Nombre de la skill (snake_case, ej: "mi_skill")
        descripcion: Descripción de qué hace la skill
        dominio: "webdev", "gamedev", "gitdev", "estructura", "generic"
        parametros: Lista de parámetros de la función principal
        funcion: Nombre de la función principal (opcional, deduce de nombre)

    Returns:
        Mensaje con el resultado de la creación
    """
    try:
        nombre = nombre.lower().strip().replace(" ", "_")

        if funcion is None:
            funcion = nombre.replace("-", "_")

        if parametros is None:
            parametros = ["descripcion: str"]

        # Determinar dominio y carpeta
        dominio = dominio.lower().strip()
        if dominio in ["web", "frontend", "backend"]:
            dominio = "webdev"
        elif dominio in ["game", "juego", "pygame"]:
            dominio = "gamedev"
        elif dominio in ["git", "github"]:
            dominio = "gitdev"

        carpeta_dominio = {
            "webdev": "webdev",
            "gamedev": "gamedev",
            "gitdev": "gitdev",
            "estructura": ".",
            "generic": "webdev",
        }.get(dominio, "webdev")

        if carpeta_dominio == ".":
            archivo_skill = SKILL_DIR / f"{nombre}.py"
        else:
            archivo_skill = SKILL_DIR / carpeta_dominio / f"{nombre}.py"

        if archivo_skill.exists():
            return f"Ya existe una skill con ese nombre: {archivo_skill}"

        # Obtener template
        template = TEMPLATES.get(dominio, TEMPLATES["generic"])

        # Preparar parámetros
        params_def = ", ".join(parametros)

        # Generar código
        codigo = template.format(
            nombre=nombre,
            funcion=funcion,
            descripcion=descripcion,
            dominio=dominio,
            params_def=params_def,
        )

        # Escribir archivo
        with open(archivo_skill, "w", encoding="utf-8") as f:
            f.write(codigo)

        # Actualizar índice
        _actualizar_indice(
            nombre, descripcion, dominio, str(archivo_skill), funcion, parametros
        )

        return f"Skill '{nombre}' creada exitosamente en {archivo_skill}\nRegistrada en skill_index.json"

    except Exception as e:
        return f"Error al crear skill: {str(e)}"


def _actualizar_indice(
    nombre: str,
    descripcion: str,
    dominio: str,
    archivo: str,
    funcion: str,
    parametros: list,
):
    """Actualiza el índice de skills."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        index["skills"].append(
            {
                "name": nombre,
                "description": descripcion,
                "dominio": dominio,
                "archivo": archivo,
                "funcion": funcion,
                "parametros": parametros,
            }
        )

        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error actualizando índice: {e}")


def listar_skills() -> str:
    """Lista todas las skills disponibles."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        resultado = ["Skills disponibles:"]
        for skill in index["skills"]:
            resultado.append(f"- {skill['name']}: {skill['description']}")

        return "\n".join(resultado)
    except Exception as e:
        return f"Error: {str(e)}"


def buscar_skill(query: str) -> str:
    """Busca skills que coincidan con la query."""
    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        query = query.lower()
        resultados = []

        for skill in index["skills"]:
            if query in skill["name"].lower() or query in skill["description"].lower():
                resultados.append(
                    f"- {skill['name']} ({skill['dominio']}): {skill['description']}"
                )

        if resultados:
            return "Skills encontradas:\n" + "\n".join(resultados)
        return "No se encontraron skills que coincidan"
    except Exception as e:
        return f"Error: {str(e)}"
