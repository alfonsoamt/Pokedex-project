import httpx
import asyncio
import math
from typing import AsyncGenerator, Dict
from cachetools import TTLCache

# --- Cache Setup ---
pokemon_cache = TTLCache(maxsize=1024, ttl=3600)

async def get_pokemon_basic_info(pokemon_id: int) -> Dict:
    """Get basic info for a single Pokemon, using a cache."""
    if pokemon_id in pokemon_cache:
        return pokemon_cache[pokemon_id]

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            pokemon_data = {
                "id": data["id"],
                "name": data["name"].capitalize(),
                "sprite": data["sprites"]["front_default"],
                "types": [t["type"]["name"] for t in data["types"]]
            }
            pokemon_cache[pokemon_id] = pokemon_data
            return pokemon_data
        except Exception as e:
            print(f"Error for pokemon {pokemon_id}: {e}")
            return {"error": f"Data not available for Pokémon {pokemon_id}"}

async def get_streamed_pokemons(page: int, limit: int) -> AsyncGenerator[Dict, None]:
    """
    Streams Pokémon data, sending pagination info first, then each Pokémon individually.
    """
    offset = (page - 1) * limit
    total_items = 1025
    total_pages = math.ceil(total_items / limit)

    # 1. Yield pagination info immediately
    yield {
        "type": "pagination",
        "data": {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page
        }
    }

    # Check if the requested page is out of bounds
    if offset >= total_items:
        return

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 2. Fetch the list of Pokémon for the current page
            list_url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
            response = await client.get(list_url)
            response.raise_for_status()
            pokemon_results = response.json().get("results", [])

            # 3. Create and yield tasks for each Pokémon
            for p in pokemon_results:
                pokemon_id = int(p["url"].split("/")[-2])
                if pokemon_id > total_items:
                    continue # Skip Pokémon beyond the official count
                
                pokemon_data = await get_pokemon_basic_info(pokemon_id)
                yield {"type": "pokemon", "data": pokemon_data}
            
            # 4. Signal that the stream is complete
            yield {"type": "done", "data": {"message": "Stream complete"}}

        except Exception as e:
            print(f"Error streaming pokemon list: {e}")
            yield {"type": "error", "data": {"message": str(e)}}
