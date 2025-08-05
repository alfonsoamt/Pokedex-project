from fastapi import APIRouter
from app.api.services import pokemon_service as pokemon


router = APIRouter()
@router.get("/pokemon/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    """
    Endpoint to fetch basic information about a pokemon.
    Args:
        pokemon_name (str): The name or ID of the pokemon.
    Returns:
        dict: A dictionary containing basic information about the pokemon.
    """
    return await pokemon.get_pokemon_basic_info(pokemon_name)