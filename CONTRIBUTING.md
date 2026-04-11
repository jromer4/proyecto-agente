# Contribuir al Súper Agente MCP

¡Gracias por tu interés en contribuir! Este documento explica cómo puedes ayudar a mejorar el proyecto.

## 🚀 Cómo empezar

1. **Haz un fork** del repositorio en GitHub.
2. **Clona** tu fork localmente:
   ```bash
   git clone https://github.com/TU_USUARIO/proyecto-agente.git
   cd proyecto-agente
   ```
3. **Crea un entorno virtual** e instala las dependencias:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
4. **Crea una rama** para tu cambio:
   ```bash
   git checkout -b feat/mi-nueva-skill
   ```

## 📐 Estructura de una Skill

Cada skill es un archivo `.py` dentro de `skills/` organizado por dominio:

```
skills/
├── webdev/        ← Desarrollo web
├── gamedev/       ← Desarrollo de videojuegos
└── gitdev/        ← Git y colaboración
```

### Plantilla mínima para una nueva skill

```python
"""
Nombre de tu skill — Descripción breve de para qué sirve.
"""

# === MEMORIA_CONSOLIDADA_START ===
LECCIONES_CONSOLIDADAS = """"""
# === MEMORIA_CONSOLIDADA_END ===


def mi_funcion_principal(parametro: str) -> str:
    """Explicación clara de lo que hace esta función."""
    contexto = LECCIONES_CONSOLIDADAS

    # Tu lógica aquí...
    return "resultado"
```

> **Importante:** Los marcadores `MEMORIA_CONSOLIDADA_START/END` son obligatorios para que el sistema de engramas pueda consolidar aprendizajes en tu skill.

## ✅ Registrar tu skill en el servidor

Después de crear tu archivo, regístralo en `server.py`:

1. Importa tu módulo en la cabecera.
2. Añade una función decorada con `@mcp.tool()`.
3. Incluye un docstring descriptivo — OpenCode lo usa para decidir cuándo llamar a tu herramienta.

## 📝 Convenciones

- **Commits:** Usa [Conventional Commits](https://www.conventionalcommits.org/).
  - `feat: añadir skill de diseño UX`
  - `fix: corregir detección de proyecto en Linux`
  - `docs: actualizar README con nueva skill`
- **Código:** Sigue PEP 8. Usa docstrings en español.
- **Ramas:** `feat/`, `fix/`, `docs/` según el tipo de cambio.

## 🐛 Reportar bugs

Abre un **Issue** en GitHub con:
- Descripción del problema.
- Pasos para reproducirlo.
- Sistema operativo y versión de Python.

## 📄 Licencia

Al contribuir, aceptas que tu código se distribuirá bajo la [Licencia MIT](LICENSE) del proyecto.
