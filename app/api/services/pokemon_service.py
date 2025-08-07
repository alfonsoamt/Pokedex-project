import httpx
import asyncio
from typing import List, Dict

async def get_pokemon_basic_info(pokemon_id: int) -> Dict:
    """Get basic info for a single Pokemon"""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    
    async with httpx.AsyncClient(timeout=10.0) as client:  # Added timeout
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            return {
                "id": data["id"],
                "name": data["name"].capitalize(),
                "sprite": data["sprites"]["front_default"],
                "types": [t["type"]["name"] for t in data["types"]]
            }
        except httpx.TimeoutException:
            print(f"Timeout fetching pokemon {pokemon_id}")
            return {"error": "Request timed out"}
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error for pokemon {pokemon_id}: {e}")
            return {"error": "Pokemon not found"}
        except Exception as e:
            print(f"Unexpected error for pokemon {pokemon_id}: {e}")
            return {"error": "Server error"}

async def get_pokemon_batch(start_id: int, count: int = 12) -> List[Dict]:
    """Get a batch of Pokemon"""
    MAX_POKEMON = 151  # Límite de la primera generación
    
    # Ajustar count si excedería el límite
    if start_id + count > MAX_POKEMON:
        count = MAX_POKEMON - start_id + 1
    
    # Si el start_id ya excede el límite, retornar lista vacía
    if start_id > MAX_POKEMON:
        return []
    
    # Crear tareas solo para IDs válidos
    ids = range(start_id, start_id + count)
    tasks = [get_pokemon_basic_info(pid) for pid in ids]
    
    try:
        results = await asyncio.gather(*tasks)
        return [r for r in results if "error" not in r]
    except Exception as e:
        print(f"Batch error: {e}")
        return []