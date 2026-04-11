# 🤖 Súper Agente MCP

> Servidor MCP con **sistema de skills con carga bajo demanda** — un enjambre de agentes especializados que aprende de cada interacción y decide automáticamente qué skill usar.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![MCP Protocol](https://img.shields.io/badge/Protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)

---

## 📋 Índice

- [¿Qué es?](#-qué-es)
- [Arquitectura](#-arquitectura)
- [Flujo de ejecución](#-flujo-de-ejecución)
- [Instalación rápida](#-instalación-rápida)
- [Configuración](#-configuración)
- [Catálogo de herramientas](#-catálogo-de-herramientas)
- [Sistema de memoria](#-sistema-de-memoria)
- [Skill Creator](#-skill-creator)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué es?

El Súper Agente es un **servidor MCP** (Model Context Protocol) con un sistema inteligente de gestión de skills:

- **Carga bajo demanda**: Solo carga la skill necesaria, no todas
- **Detección automática**: Gemma decide qué skill usar desde el índice
- **Memoria evolutiva**: Cada skill aprende de sus interacciones
- **Proveedores múltiples**: LM Studio (gemma) + OpenRouter/Groq

### Proveedores de IA

| Proveedor | Modelo | Uso |
|-----------|--------|-----|
| **LM Studio** | gemma-4-e2b-it | Detección de skills, preparación de contexto |
| **OpenRouter** | LLaMA 3.1 8B | Trabajo pesado (código, respuestas) |
| **Groq** | LLaMA 3.1 8B | Alternativo si OpenRouter falla |

---

## 🏗️ Arquitectura

```
proyecto-agente/
├── server.py                  ← Orquestador MCP
├── opencode.json              ← Configuración OpenCode
├── skill_index.json           ← Índice de todas las skills (~50 tokens)
├── engramas_agente.json       ← Memoria temporal
├── procedimientos.json        ← Decisiones técnicas universales
├── .env                       ← Claves API (LM Studio, OpenRouter, Groq)
├── skills/
│   ├── config_lm.py           ← Cerebro: detección + orquestación
│   ├── engram.py              ← Sistema de memoria
│   ├── skill_creator/         ← Meta-skill creadora de skills
│   ├── webdev/                ← React, CSS, Python, PHP
│   ├── gamedev/               ← Pygame: renderer, combat, entities
│   ├── gitdev/                ← GitHub Master
│   └── architect.py           ← Mapear, dependencias, resumir
```

---

## ⚡ Flujo de ejecución

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PROMPT del usuario                                       │
└──────────────────────────┬──────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. gemma lee skill_index (todas las descripciones)          │
│    → Analiza: "¿Qué skill coincide?"                        │
└──────────────────────────┬──────────────────────────────────┘
             ┌─────────────┴─────────────┐
             ↓                           ↓
         COINCIDE                   NO COINCIDE
             ↓                           ↓
┌─────────────────────┐    ┌─────────────────────────┐
│ Cargar ESA skill +  │    │ OpenRouter directo      │
│ SUS engramas        │    │ (sin skill)             │
└────────┬────────────┘    └───────────┬─────────────┘
         ↓                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. OpenRouter con contexto (prompt + skill + memoria)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 Instalación rápida

```bash
# Opción 1: En un proyecto nuevo
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1   |   Linux/Mac: source .venv/bin/activate
pip install mcp litellm python-dotenv

# Opción 2: Usar el instalador automático
python D:/josemi/proyecto-agente/instalar_super_agente.py
```

> ⚠️ **Importante**: Asegúrate de que LM Studio esté corriendo con tu modelo.

---

## 📦 Configuración

### Archivo `.env`

```env
# Modelo local (LM Studio)
LM_STUDIO_BASE_URL=http://127.0.0.1:1234/v1
LM_STUDIO_MODEL=gemma-4-e2b-it

# Proveedores externos (al menos uno)
GROQ_API_KEY=tu_clave_groq
OPENROUTER_API_KEY=tu_clave_openrouter
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
```

### OpenCode (`opencode.json`)

```json
{
  "mcp": {
    "super-agente": {
      "type": "local",
      "command": ["RUTA/.venv/Scripts/python.exe", "RUTA/server.py"],
      "enabled": true,
      "environment": { "PYTHONIOENCODING": "utf-8" }
    }
  }
}
```

---

## 🛠️ Catálogo de herramientas

### Orquestador principal

| Herramienta | Descripción |
|-------------|-------------|
| `ejecutar_prompt` | Ejecuta prompt con detección automática de skills |
| `orquestar` | Alias de ejecutar_prompt |

### Memoria y procedimientos

| Herramienta | Descripción |
|-------------|-------------|
| `guardar_engrama` | Guarda aprendizaje (tipo: global/proyecto) |
| `guardar_procedimiento` | Guarda decisión técnica universal |
| `recordar_memorias` | Recupera engramas filtrados |
| `ver_procedimientos` | Lista todos los procedimientos |
| `ver_contexto` | Muestra estado de memoria |

### Skills del enjambre

| Herramienta | Dominio | Descripción |
|-------------|---------|-------------|
| `crear_componente_react` | WebDev | Componentes React/TSX |
| `generar_css_ninja` | WebDev | CSS, Tailwind, animaciones |
| `programar_backend_python` | WebDev | APIs FastAPI/Flask |
| `programar_backend_php` | WebDev | PHP, WordPress |
| `agente_render_pixelart` | GameDev | Gráficos Pygame pixel-art |
| `agente_matematico_rpg` | GameDev | Fórmulas combate RPG |
| `agente_entidades_masivas` | GameDev | Entidades y colisiones |
| `agente_github_master` | GitDev | Asesoría Git/GitHub |
| `mapear_estructura` | Estructura | Árbol de carpetas |
| `buscar_dependencias` | Estructura | Análisis de imports |
| `resumir_codigo_con_ia` | Estructura | Resumir archivos |

### Skill Creator

| Herramienta | Descripción |
|-------------|-------------|
| `crear_skill` | Crea una nueva skill automáticamente |
| `listar_skills` | Lista todas las skills del índice |
| `buscar_skill` | Busca skills por nombre/descripción |

---

## 🧠 Sistema de memoria

### Tipos de memoria

| Tipo | Alcance | Ejemplo |
|------|---------|---------|
| **Global** | Siempre | Idioma, nombre (José) |
| **Proyecto** | Solo proyecto actual | Reglas específicas de "mi-app" |
| **Procedimientos** | Todos los proyectos | Decisiones técnicas universales |

### Cómo aprenden las skills

1. **Engramas temporales**: Se guardan en `engramas_agente.json`
2. **Consolidación**: Se comprimen y escriben en el `.py` de la skill
3. **Carga automática**: La skill siempre carga sus lecciones al ejecutarse

### Estructura de una skill

```python
# skills/webdev/react_expert.py
from skills import engram, config_lm

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """
- [REGLA]: Descripción de la regla aprendida
"""
# === MEMORIA_CONSOLIDADA_END ===

def generar_componente_react(nombre: str, descripcion: str) -> str:
    # Carga lecciones consolidadas
    if LECCIONES_CONSOLIDADAS.strip():
        instrucciones += f"LECCIONES: {LECCIONES_CONSOLIDADAS}"
    
    # Carga engramas temporales
    memorias = engram.recuperar_engramas("react_expert")
    
    return config_lm.complete(messages=[...])
```

---

## 🧩 Skill Creator

El sistema incluye una **meta-skill** que puede crear nuevas skills automáticamente.

### Uso

```python
# Crear una nueva skill
crear_skill(
    nombre="mi_nueva_skill",
    descripcion="Descripción de qué hace",
    dominio="webdev",  # webdev, gamedev, gitdev, generic
    parametros=["descripcion: str"]
)
```

### Lo que hace automáticamente

1. Genera el archivo `.py` con estructura completa
2. Añade la skill al `skill_index.json`
3. Configura integración con engram y config_lm
4. La skill queda lista para usarse inmediatamente

### Índice de skills

El archivo `skill_index.json` contiene todas las skills disponibles con solo sus nombres y descripciones (~50 tokens para 50 skills), permitiendo que gemma analice siempre el índice completo sin aumentar el contexto.

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.