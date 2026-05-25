import subprocess
from pathlib import Path
import webbrowser
import time

PORT = 8000

BASE = Path(__file__).parent.resolve()
RUTA = BASE / "data/2026-1/"
print("Iniciando servidor en:", RUTA)

# levantar servidor en esa carpeta
server = subprocess.Popen(
    ["python3", "-m", "http.server", str(PORT)],
    cwd=RUTA
)

# esperar un momento
time.sleep(2)

# abrir navegador en index.html
# url = f"http://localhost:{PORT}/index.html"
url = f"http://localhost:{PORT}/index.html?t={time.time()}"
print(f"Servidor corriendo en: {url}")

webbrowser.open(url)

try:
    input("Presiona Enter para detener...\n")
finally:
    server.terminate()
    print("Servidor detenido")
