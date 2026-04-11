# 🛠️ Guía de Instalación: Súper Agente MCP

Sigue estos pasos para conectar tu propio Enjambre de Agentes a tu IDE (Cursor, VSCode o cualquier cliente MCP).

## 1. Requisitos Previos
Asegúrate de haber instalado las dependencias en tu entorno virtual:
```powershell
pip install -r requirements.txt
```

## 2. Configuración de API Keys
Edita el archivo `.env` en la raíz del proyecto y asegúrate de tener:
- `GROQ_API_KEY`: Para el motor de los agentes (Llama3).
- `GEMINI_API_KEY`: (Opcional) Si usas modelos de Google.

---

## 3. Instalación en Cursor (El IDE Experto)

Cursor tiene soporte nativo para MCP. Es la forma más rápida de usar el enjambre.

1.  Abre **Cursor Settings** (el icono de engranaje en la esquina superior derecha o `Ctrl + Shift + J`).
2.  Ve a la pestaña **Models** y busca la sección **MCP Servers**.
3.  Haz clic en **"+ Add New MCP Server"**.
4.  Configúralo así:
    - **Name**: `SuperAgente`
    - **Type**: `command`
    - **Command**:
      ```powershell
      python "D:/josemi/proyecto-agente/server.py"
      ```
      > [!IMPORTANT]
      > Si usas un entorno virtual (recomendado), usa la ruta completa al ejecutable de python dentro de tu `.venv`. Ejemplo: `"D:/josemi/proyecto-agente/.venv/Scripts/python.exe"`.

5.  Haz clic en **Save**. Verás que el estado cambia a **Connected** y aparecerán tus 15+ herramientas.

---

## 4. Instalación en VSCode (con Cline / Roo Code)

Si usas extensiones como **Cline** o **Roo Code**:

1.  Abre la configuración de la extensión (icono de MCP/Tools).
2.  Añade una nueva entrada en el archivo de configuración `mcpSettings.json`:
```json
{
  "mcpServers": {
    "super-agente": {
      "command": "python",
      "args": ["D:/josemi/proyecto-agente/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

---

## 5. Verificación Final ✨

Una vez instalado, abre el Chat de tu IDE y pregunta:
> *"@SuperAgente ¿quién eres?"* o *"Usa la tool quien_eres"*

Si el sistema te responde con el mapa del enjambre (4 pilares), **¡estás listo para programar a la velocidad de la luz!**

---
> [!TIP]
> **Modo Depuración**: Si el servidor no conecta, abre una terminal y ejecuta `python server.py`. Debería mostrar un mensaje indicando que está esperando conexión. Si da error de importación, es que te faltan librerías.
