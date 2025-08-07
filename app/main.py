# En app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

# Importa tu router de la API
from app.api.routers import pokemon_endpoints

# --- CONFIGURACIÓN ---
app = FastAPI()

# Montamos archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Definimos templates
templates = Jinja2Templates(directory="templates")

# Incluimos el router
app.include_router(pokemon_endpoints.router)

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})