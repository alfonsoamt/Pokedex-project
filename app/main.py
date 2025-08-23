# En app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware


# Importa tu router de la API
from app.api.routers import pokemon_endpoints



# --- CONFIGURACIÓN ---
app = FastAPI()

# --- Configuración de CORS ---
# Lista de orígenes permitidos (tu frontend en Netlify y el entorno local)
origins = [
    "https://amt-pokedex.netlify.app",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Montamos archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Definimos templates
templates = Jinja2Templates(directory="templates")

# Incluimos el router
app.include_router(pokemon_endpoints.router)

@app.get("/")
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})