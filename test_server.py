# En test_server.py (en la raíz del proyecto)

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. Crea la instancia de la aplicación
app = FastAPI()

# 2. Monta los archivos estáticos.
#    Como este script está en la raíz, la ruta "static" es directa.
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Configura las plantillas.
#    Como este script está en la raíz, la ruta "templates" es directa.
templates = Jinja2Templates(directory="templates")

# 4. Define el endpoint raíz.
@app.get("/")
def serve_home(request: Request):
    print("¡Endpoint raíz de test_server.py alcanzado!")
    return templates.TemplateResponse("index.html", {"request": request})