# 🤖 Súper Agente MCP

> Servidor MCP modular con **memoria evolutiva por skill y proyecto** — un enjambre de agentes especializados que aprenden de cada interacción.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![MCP Protocol](https://img.shields.io/badge/Protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)

---

## 📋 Índice

- [¿Qué es?](#-qué-es)
- [Arquitectura](#-arquitectura)
- [Instalación rápida](#-instalación-rápida)
- [Configuración en OpenCode](#-configuración-en-opencode)
- [Catálogo de herramientas](#-catálogo-de-herramientas)
- [Sistema de memoria evolutiva](#-sistema-de-memoria-evolutiva)
- [Crear una nueva skill](#-crear-una-nueva-skill)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué es?

El Súper Agente es un **servidor MCP** (Model Context Protocol) que actúa como orquestador de un enjambre de agentes especializados en distintos dominios del desarrollo de software:

- 🌐 **WebDev** — React, CSS, Python y PHP backends.
- 🎮 **GameDev** — Renderizado pixel-art, combate RPG y entidades masivas en Pygame.
- 🐙 **GitDev** — Asesoría experta en flujos Git, PRs y Conventional Commits.
- 🏗️ **Arquitecto** — Mapeo de proyectos, análisis de dependencias y resúmenes con IA.

Su diferenciador principal es el **sistema de memoria evolutiva (Engramas)**: cada agente aprende lecciones de sus interacciones y las consolida como conocimiento permanente, adaptándose al contexto de cada proyecto.

---

## 🏗️ Arquitectura

```
proyecto-agente/
├── server.py                  ← Orquestador MCP (registro de tools)
├── opencode.json              ← Configuración para OpenCode
├── pyproject.toml             ← Manifiesto estándar de Python
├── engramas_agente.json       ← Base de datos temporal de engramas
├── requirements.txt           ← Dependencias
├── .env                       ← Claves API (Groq)
└── skills/
    ├── engram.py              ← 🧠 Cerebro (memoria evolutiva)
    ├── architect.py           ← 🏗️ Mapeo, dependencias, resumidor
    ├── webdev/
    │   ├── react_expert.py    ← Componentes React/TSX
    │   ├── css_ninja.py       ← Maquetación y animaciones CSS
    │   ├── backend_python.py  ← APIs con FastAPI/Flask
    │   └── backend_php.py     ← PHP, WordPress, Symfony
    ├── gamedev/
    │   ├── pygame_renderer.py ← Renderizado pixel-art en Pygame
    │   ├── pygame_combat.py   ← Fórmulas matemáticas de combate RPG
    │   └── pygame_entities.py ← Entidades masivas y colisiones
    └── gitdev/
        └── github_master.py   ← Asesor Git y GitHub
```

---

## ⚡ Instalación rápida

```bash
git clone https://github.com/jromer4/proyecto-agente.git
cd proyecto-agente
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1   |   Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

> 📖 **Guía completa paso a paso:** Consulta [INSTALL.md](INSTALL.md) para instrucciones detalladas, configuración de OpenCode, errores comunes y soluciones.

---

## 🔌 Configuración en OpenCode

### Archivo del proyecto (`opencode.json`)

```json
{
  "mcp": {
    "super-agente": {
      "command": "RUTA/.venv/Scripts/python.exe",
      "args": ["RUTA/server.py"],
      "type": "stdio"
    }
  }
}
```

### Archivo global (`~/.opencode.json`)

```json
"super-agente": {
  "command": "RUTA/.venv/Scripts/python.exe",
  "args": ["RUTA/server.py"],
  "type": "stdio"
}
```

> ⚠️ **IMPORTANTE:** El archivo del proyecto usa la clave `"mcp"`. El archivo global usa `"mcpServers"`. **No los confundas.** Usa SOLO los campos `command`, `args` y `type`. Ver [INSTALL.md](INSTALL.md) para detalles y errores comunes.

---

## 🛠️ Catálogo de herramientas

### Enjambre de agentes especializados

| Herramienta | Dominio | Descripción |
|-------------|---------|-------------|
| `crear_componente_react` | WebDev | Genera componentes funcionales en React/TSX |
| `generar_css_ninja` | WebDev | Maquetación CSS, flexbox, grid y animaciones |
| `programar_backend_python` | WebDev | APIs web con FastAPI/Flask y lógica de BD |
| `programar_backend_php` | WebDev | Scripts PHP, WordPress, WooCommerce, Symfony |
| `agente_render_pixelart` | GameDev | Renderizado y escalado gráfico en Pygame |
| `agente_matematico_rpg` | GameDev | Fórmulas de daño, vida, armadura, economía |
| `agente_entidades_masivas` | GameDev | Movimiento IA, colisiones y oleadas masivas |
| `agente_github_master` | GitDev | Flujos Git, PRs, Conventional Commits |

### Herramientas de arquitectura

| Herramienta | Descripción |
|-------------|-------------|
| `mapear_estructura` | Genera un árbol visual de carpetas del proyecto |
| `buscar_dependencias` | Extrae imports/requires de un archivo |
| `resumir_codigo_con_ia` | Resume un archivo largo usando Groq/Llama3 |

### Sistema de memoria

| Herramienta | Descripción |
|-------------|-------------|
| `memorizar` | Guarda una lección para un agente específico |
| `recordar_memorias` | Recupera engramas filtrados jerárquicamente |
| `ver_contexto` | Muestra el proyecto detectado y estado de memoria |
| `consolidar_skill` | Comprime engramas → lecciones permanentes en `.py` |
| `consolidar_proyecto` | Comprime engramas generales de un proyecto |
| `quien_eres` | Devuelve la identidad y mapa del enjambre |
| `hello_world` | Test de conectividad del servidor |

---

## 🧠 Sistema de memoria evolutiva

El sistema de **Engramas** organiza el conocimiento en una jerarquía de 4 niveles, de lo más general a lo más específico:

| Nivel | Skill | Proyecto | Alcance |
|-------|-------|----------|---------|
| 🌍 Global | `global` | `global` | Personalidad y reglas universales eternas |
| 🔧 Skill | — | — | Lecciones consolidadas en el `.py` de cada skill |
| 📂 Proyecto | `global` | `mi-app` | Reglas generales del proyecto activo |
| 🎯 Skill+Proyecto | `react_expert` | `mi-app` | Reglas de una skill exclusivas para ese proyecto |

### ¿Cómo funciona?

1. **Memorizar:** Cada vez que un agente corrige un patrón o aprende algo nuevo, se guarda como engrama temporal en `engramas_agente.json`.
2. **Consolidar:** Cuando se acumulan varios engramas de una skill, se comprimen usando Groq/Llama3 y se inyectan como lecciones permanentes dentro del archivo `.py` de la skill.
3. **Recordar:** Al invocar un agente, este consulta automáticamente su conocimiento consolidado para dar respuestas más precisas.
4. **Detección automática:** El proyecto se identifica por el nombre de la carpeta de trabajo — no requiere configuración manual.

---

## 🧩 Crear una nueva skill

1. Crea un archivo `.py` dentro del directorio `skills/` correspondiente.
2. Incluye los marcadores de memoria obligatorios:
   ```python
   # === MEMORIA_CONSOLIDADA_START ===
   LECCIONES_CONSOLIDADAS = """"""
   # === MEMORIA_CONSOLIDADA_END ===
   ```
3. Registra la función en `server.py` con el decorador `@mcp.tool()`.
4. Escribe un docstring descriptivo — OpenCode lo utiliza para decidir cuándo activar tu herramienta.

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Lee la [guía de contribución](CONTRIBUTING.md) para conocer:
- El flujo de trabajo con ramas y PRs.
- Las convenciones de commits y código.
- La plantilla para crear nuevas skills.

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más información.
