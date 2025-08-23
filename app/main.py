# En app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa tu router de la API
from app.api.routers import pokemon_endpoints

# --- CONFIGURACIÓN DE LA API ---
app = FastAPI()

# --- Configuración de CORS ---
# Lista de orígenes permitidos (tu frontend en Netlify y el entorno local)
origins = [
    "https://amt-pokedex.netlify.app",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500", # Origen para Live Server de VS Code
    "http://127.0.0.1:8081", # Origen para el servidor de Python
    "http://127.0.0.1:3000", # Origen para Live Server en puerto 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Incluimos el router de la API, que contiene todos los endpoints de Pokémon
app.include_router(pokemon_endpoints.router)
