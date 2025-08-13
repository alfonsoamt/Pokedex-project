import httpx
import asyncio
import math
from typing import AsyncGenerator, Dict, List, Optional
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

async def get_streamed_pokemons(page: int, limit: int, types: Optional[List[str]] = None) -> AsyncGenerator[Dict, None]:
    """
    Streams Pokémon data, sending pagination info first, then each Pokémon individually.
    Dispatches to the correct fetcher based on whether types are provided.
    """
    if not types:
        stream = _get_all_pokemons(page, limit)
    elif len(types) == 1:
        stream = _get_pokemons_by_type(types[0], page, limit)
    elif len(types) >= 2:
        # Handles two types, ignores any more than two for now.
        stream = _get_pokemons_by_two_types(types[0], types[1], page, limit)
    
    async for item in stream:
        yield item

async def _get_all_pokemons(page: int, limit: int) -> AsyncGenerator[Dict, None]:
    """Streams all Pokémon, paginated."""
    offset = (page - 1) * limit
    total_items = 1025
    total_pages = math.ceil(total_items / limit)

    yield {
        "type": "pagination",
        "data": {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": page
        }
    }

    if offset >= total_items:
        return

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            list_url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
            response = await client.get(list_url)
            response.raise_for_status()
            pokemon_results = response.json().get("results", [])

            for p in pokemon_results:
                pokemon_id = int(p["url"].split("/")[-2])
                if pokemon_id > total_items:
                    continue
                
                pokemon_data = await get_pokemon_basic_info(pokemon_id)
                yield {"type": "pokemon", "data": pokemon_data}
            
            yield {"type": "done", "data": {"message": "Stream complete"}}

        except Exception as e:
            print(f"Error streaming pokemon list: {e}")
            yield {"type": "error", "data": {"message": str(e)}}

async def _fetch_pokemon_list_by_type(type_name: str, client: httpx.AsyncClient) -> List[str]:
    """Fetches a list of Pokémon names for a given type."""
    type_url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
    response = await client.get(type_url)
    response.raise_for_status()
    data = response.json()
    return [p["pokemon"]["url"] for p in data["pokemon"]]

async def _get_pokemons_by_type(type_name: str, page: int, limit: int) -> AsyncGenerator[Dict, None]:
    """Streams Pokémon of a specific type, paginated."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            pokemon_urls = await _fetch_pokemon_list_by_type(type_name, client)

        total_items = len(pokemon_urls)
        total_pages = math.ceil(total_items / limit)
        offset = (page - 1) * limit

        yield {
            "type": "pagination",
            "data": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page
            }
        }

        paginated_urls = pokemon_urls[offset:offset + limit]

        for url in paginated_urls:
            pokemon_id = int(url.split("/")[-2])
            if pokemon_id > 1025:
                continue
            pokemon_data = await get_pokemon_basic_info(pokemon_id)
            yield {"type": "pokemon", "data": pokemon_data}

        yield {"type": "done", "data": {"message": "Stream complete"}}

    except Exception as e:
        print(f"Error streaming pokemon by type: {e}")
        yield {"type": "error", "data": {"message": str(e)}}

async def _get_pokemons_by_two_types(type1: str, type2: str, page: int, limit: int) -> AsyncGenerator[Dict, None]:
    """Streams Pokémon that have BOTH of the two specified types, paginated."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fetch both lists concurrently
            task1 = _fetch_pokemon_list_by_type(type1, client)
            task2 = _fetch_pokemon_list_by_type(type2, client)
            results = await asyncio.gather(task1, task2)
            
            # Find the intersection of the two lists
            intersection_urls = set(results[0]).intersection(set(results[1]))
            pokemon_urls = sorted(list(intersection_urls), key=lambda url: int(url.split("/")[-2]))

        total_items = len(pokemon_urls)
        total_pages = math.ceil(total_items / limit)
        offset = (page - 1) * limit

        yield {
            "type": "pagination",
            "data": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page
            }
        }

        paginated_urls = pokemon_urls[offset:offset + limit]

        for url in paginated_urls:
            pokemon_id = int(url.split("/")[-2])
            if pokemon_id > 1025:
                continue
            pokemon_data = await get_pokemon_basic_info(pokemon_id)
            yield {"type": "pokemon", "data": pokemon_data}

        yield {"type": "done", "data": {"message": "Stream complete"}}

    except Exception as e:
        print(f"Error streaming pokemon by two types: {e}")
        yield {"type": "error", "data": {"message": str(e)}}

async def get_all_types() -> List[str]:
    """Fetches a list of all official Pokémon type names."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # The main type endpoint lists all types
            response = await client.get("https://pokeapi.co/api/v2/type")
            response.raise_for_status()
            data = response.json()
            # We exclude 'unknown', 'shadow' and 'stellar' as they are special cases
            type_names = [t["name"] for t in data["results"] if t["name"] not in ["unknown", "shadow", "stellar"]]
            return type_names
    except Exception as e:
        print(f"Error fetching all types: {e}")
        return []