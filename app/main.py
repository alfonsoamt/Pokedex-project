from  fastapi import FastAPI
from .api.routers import pokemon_endpoints

app = FastAPI()

app.include_router(pokemon_endpoints.router)

@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    Returns:
        dict: A message indicating that the API is running.
    """
    return {"message": "PokeAPI is running!"}