import sys
import json

def main():
    # Un servidor MCP mínimo que responde a listTools
    # (Simulado para ver si OpenCode lo detecta)
    print("Iniciando test MCP...", file=sys.stderr)
    # Aquí iría la lógica de stdio, pero solo queremos ver si arranca
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            # Responder algo básico para no colgarse
            res = {"jsonrpc": "2.0", "id": req.get("id"), "result": {"tools": []}}
            print(json.dumps(res), flush=True)
        except:
            pass

if __name__ == "__main__":
    main()
