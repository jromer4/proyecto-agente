# Guía de Instalación del Súper Agente MCP

> **PÚBLICO OBJETIVO:** Esta guía está escrita para que cualquier IA o persona pueda instalar el servidor sin errores siguiendo los pasos literalmente. No omitas ningún paso.

---

## Requisitos previos

Antes de empezar, asegúrate de tener instalado:

- **Python 3.10 o superior.** Verificar con: `python --version`
- **pip** (viene incluido con Python). Verificar con: `pip --version`
- **Git** (opcional, solo para clonar). Verificar con: `git --version`

---

## Paso 1: Obtener el código fuente

### Opción A: Clonar con Git
```bash
git clone https://github.com/jromer4/proyecto-agente.git
cd proyecto-agente
```

### Opción B: Descargar manualmente
Descarga el ZIP desde GitHub y descomprímelo. Abre una terminal dentro de la carpeta resultante.

---

## Paso 2: Crear el entorno virtual

Ejecuta **desde dentro de la carpeta del proyecto**:

```bash
python -m venv .venv
```

Esto crea una carpeta `.venv/` con un Python aislado.

---

## Paso 3: Activar el entorno virtual

### Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows (CMD):
```cmd
.\.venv\Scripts\activate.bat
```

### Linux / macOS:
```bash
source .venv/bin/activate
```

> **Comprobación:** Si se activó correctamente, verás `(.venv)` al inicio de la línea en tu terminal.

---

## Paso 4: Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias son:
- `mcp` — Protocolo de comunicación con el IDE.
- `litellm` — Interfaz unificada para modelos de IA.
- `python-dotenv` — Lectura del archivo `.env`.

---

## Paso 5: Configurar claves API (opcional)

El archivo `.env` en la raíz del proyecto contiene las claves API. Edítalo con tus claves reales si deseas usar la función de consolidación con IA:

```env
GROQ_API_KEY=gsk_tu_clave_real_aqui
```

> **NOTA:** Si no configuras la clave de Groq, el servidor funcionará pero las herramientas `consolidar_skill` y `consolidar_proyecto` fallarán al intentar llamar al modelo de IA. El resto de herramientas funcionará con normalidad.

---

## Paso 6: Verificar que el servidor arranca

Ejecuta esto **con el entorno virtual activado**:

```bash
python server.py
```

- Si ves `Iniciando el Servidor Súper Agente MCP...` en la salida, el servidor funciona.
- Ciérralo con `Ctrl+C`. No necesitas dejarlo corriendo manualmente; OpenCode lo arrancará automáticamente.

---

## Paso 7: Conectar con OpenCode

### ⚠️ INFORMACIÓN CRÍTICA SOBRE EL FORMATO

OpenCode tiene **DOS archivos de configuración** con **formatos DIFERENTES**. **NO los confundas:**

| Archivo | Ubicación | Clave raíz |
|---------|-----------|------------|
| **Global** | `C:/Users/TU_USUARIO/.opencode.json` | `"mcpServers"` |
| **Proyecto** | `tu-proyecto/opencode.json` | `"mcp"` |

### Opción A: Configuración global (recomendada)

Edita el archivo `C:/Users/TU_USUARIO/.opencode.json` y añade esta entrada **dentro del objeto `mcpServers` ya existente**:

```json
"super-agente": {
  "command": "RUTA_ABSOLUTA_AL_PYTHON_DEL_VENV",
  "args": ["RUTA_ABSOLUTA_A_SERVER_PY"],
  "type": "stdio"
}
```

**Ejemplo real en Windows:**
```json
"super-agente": {
  "command": "D:/josemi/proyecto-agente/.venv/Scripts/python.exe",
  "args": ["D:/josemi/proyecto-agente/server.py"],
  "type": "stdio"
}
```

**Ejemplo real en Linux/macOS:**
```json
"super-agente": {
  "command": "/home/usuario/proyecto-agente/.venv/bin/python",
  "args": ["/home/usuario/proyecto-agente/server.py"],
  "type": "stdio"
}
```

### Opción B: Configuración por proyecto

Crea un archivo llamado `opencode.json` (sin punto al inicio) en la raíz de tu proyecto de trabajo con este contenido:

```json
{
  "mcp": {
    "super-agente": {
      "command": "RUTA_ABSOLUTA_AL_PYTHON_DEL_VENV",
      "args": ["RUTA_ABSOLUTA_A_SERVER_PY"],
      "type": "stdio"
    }
  }
}
```

### ❌ Errores comunes que DEBES evitar

| Error | Causa | Solución |
|-------|-------|----------|
| `Unrecognized key: "mcpServers"` | Usaste `"mcpServers"` en el archivo **del proyecto** | Cambia a `"mcp"` |
| `Invalid input` | Añadiste campos no soportados como `"enabled"`, `"$schema"`, o `"env"` como objeto `{}` | Usa SOLO `command`, `args` y `type` |
| `Invalid input` (env) | Pusiste `"env": {"KEY": "value"}` (objeto) | En global usa `"env": ["KEY=value"]` (array de strings). En proyecto, omite `env` |
| El servidor no aparece en `/mcp` | OpenCode no recargó la configuración | Cierra OpenCode completamente y vuelve a abrirlo |
| `No module named 'mcp'` | No activaste el entorno virtual, o OpenCode apunta al Python del sistema | Asegúrate de que `command` apunta al python **dentro de `.venv/`** |

### Campos permitidos por servidor MCP

Usa **SOLO** estos campos en cada entrada de servidor:

```
command  → (string, obligatorio) Ruta al ejecutable
args     → (array de strings, obligatorio) Argumentos del comando
type     → (string, obligatorio) Siempre "stdio" para servidores locales
env      → (array de strings, opcional, SOLO en global) Variables de entorno
```

**NO uses:** `enabled`, `environment`, `$schema`, `description`, `version`, ni ningún otro campo inventado.

---

## Paso 8: Verificar la conexión desde OpenCode

1. Abre OpenCode.
2. Escribe `/mcp` en el chat.
3. Deberías ver `super-agente` en la lista de servidores activos.
4. Prueba escribiendo: `Usa la herramienta hello_world con mi nombre`

Si ves la respuesta `¡Hola [tu nombre]! El Súper Agente está en línea y funcionando.`, la instalación está completa.

---

## Resumen de rutas importantes

| Elemento | Ruta |
|----------|------|
| Python del entorno virtual (Windows) | `<proyecto>/.venv/Scripts/python.exe` |
| Python del entorno virtual (Linux/Mac) | `<proyecto>/.venv/bin/python` |
| Servidor MCP | `<proyecto>/server.py` |
| Base de datos de memoria | `<proyecto>/engramas_agente.json` |
| Claves API | `<proyecto>/.env` |
| Config global OpenCode (Windows) | `C:/Users/<USUARIO>/.opencode.json` |
| Config proyecto OpenCode | `<proyecto>/opencode.json` |
