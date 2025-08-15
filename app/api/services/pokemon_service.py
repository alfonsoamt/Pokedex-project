import httpx
import asyncio
import math
from typing import AsyncGenerator, Dict, List, Optional, Set
from cachetools import TTLCache

# --- Cache Setup ---
pokemon_cache = TTLCache(maxsize=1024, ttl=3600)

# Cache for all Pokémon names for autocomplete
_all_pokemon_names: List[Dict] = []

async def _fetch_all_pokemon_names():
    """Fetches all Pokémon names and their IDs for autocomplete caching."""
    global _all_pokemon_names
    if not _all_pokemon_names:
        url = "https://pokeapi.co/api/v2/pokemon?limit=10000" # Fetch all known Pokémon
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                _all_pokemon_names = [
                    {"name": p["name"], "id": int(p["url"].split("/")[-2])}
                    for p in data["results"]
                ]
            except Exception as e:
                # Log the error, but don't fail the app startup
                print(f"Error fetching all pokemon names for autocomplete: {e}")

async def get_pokemon_names_by_partial_match(query: str) -> List[Dict]:
    """Returns a list of Pokémon names and IDs that partially match the query."""
    if not _all_pokemon_names:
        await _fetch_all_pokemon_names() # Ensure names are loaded

    if not query: # If query is empty, return nothing
        return []

    query_lower = query.lower()
    matches = []
    for pokemon in _all_pokemon_names:
        if query_lower in pokemon["name"].lower():
            matches.append(pokemon)
        if len(matches) >= 10: # Limit suggestions to 10
            break
    return matches

# --- Service Helper Functions ---

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
        except Exception:
            
            return {"error": f"Data not available for Pokémon {pokemon_id}"}

def _get_id_from_url(url: str) -> int:
    """Extracts a numeric ID from a PokeAPI URL."""
    return int(url.split("/")[-2])

async def _fetch_pokemon_ids_by_type(type_name: str, client: httpx.AsyncClient) -> Set[int]:
    """Fetches a set of Pokémon IDs for a given type."""
    type_url = f"https://pokeapi.co/api/v2/type/{type_name.lower()}"
    response = await client.get(type_url)
    response.raise_for_status()
    data = response.json()
    return {_get_id_from_url(p["pokemon"]["url"]) for p in data["pokemon"]}

async def _fetch_pokemon_ids_by_generation(gen_id: int, client: httpx.AsyncClient) -> Set[int]:
    """Fetches a set of Pokémon IDs for a given generation."""
    gen_url = f"https://pokeapi.co/api/v2/generation/{gen_id}"
    response = await client.get(gen_url)
    response.raise_for_status()
    data = response.json()
    return {_get_id_from_url(spec["url"]) for spec in data["pokemon_species"]}

# --- Main Service Function ---

async def get_streamed_pokemons(page: int, limit: int, types: Optional[List[str]] = None, generation: Optional[int] = None, pokemon_id: Optional[int] = None, pokemon_ids: Optional[List[int]] = None) -> AsyncGenerator[Dict, None]:
    """
    Streams Pokémon data, applying filters by type and/or generation, or fetching a specific Pokémon by ID.
    """
    try:
        if pokemon_ids:
            # If a list of Pokémon IDs is provided, fetch only those
            total_items = len(pokemon_ids)
            yield {"type": "pagination", "data": {"total_items": total_items, "total_pages": 1, "current_page": 1}}
            for pid in pokemon_ids:
                pokemon_data = await get_pokemon_basic_info(pid)
                if "error" not in pokemon_data:
                    yield {"type": "pokemon", "data": pokemon_data}
            yield {"type": "done", "data": {"message": "Stream complete"}}
            return

        if pokemon_id:
            # If a specific Pokémon ID is provided, fetch only that one
            pokemon_data = await get_pokemon_basic_info(pokemon_id)
            if "error" not in pokemon_data:
                yield {"type": "pagination", "data": {"total_items": 1, "total_pages": 1, "current_page": 1}}
                yield {"type": "pokemon", "data": pokemon_data}
            else:
                yield {"type": "error", "data": {"message": f"Pokémon with ID {pokemon_id} not found."}}
            yield {"type": "done", "data": {"message": "Stream complete"}}
            return

        paginated_ids = []
        total_items = 0

        if not types and not generation:
            # --- NO FILTERS --- #
            total_items = 1025
            offset = (page - 1) * limit
            list_url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(list_url)
                response.raise_for_status()
                paginated_ids = [_get_id_from_url(p["url"]) for p in response.json().get("results", [])]
        else:
            # --- FILTERS APPLIED --- #
            async with httpx.AsyncClient(timeout=30.0) as client:
                tasks = []
                if types:
                    for type_name in types[:2]:
                        tasks.append(_fetch_pokemon_ids_by_type(type_name, client))
                if generation:
                    tasks.append(_fetch_pokemon_ids_by_generation(generation, client))
                
                if tasks:
                    results = await asyncio.gather(*tasks)
                    intersected_ids = set.intersection(*results)
                    final_ids = sorted(list(intersected_ids))
                    total_items = len(final_ids)
                    
                    # Manual pagination on the final ID list
                    offset = (page - 1) * limit
                    paginated_ids = final_ids[offset:offset + limit]

        total_pages = math.ceil(total_items / limit) if total_items > 0 else 1

        yield {
            "type": "pagination",
            "data": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page
            }
        }

        for pokemon_id in paginated_ids:
            if pokemon_id > 1025:
                continue
            pokemon_data = await get_pokemon_basic_info(pokemon_id)
            yield {"type": "pokemon", "data": pokemon_data}

        yield {"type": "done", "data": {"message": "Stream complete"}}

    except Exception as e:
        
        yield {"type": "error", "data": {"message": str(e)}}

# --- API Data Fetchers ---

async def get_all_types() -> List[str]:
    """Fetches a list of all official Pokémon type names."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://pokeapi.co/api/v2/type")
            response.raise_for_status()
            data = response.json()
            type_names = [t["name"] for t in data["results"] if t["name"] not in ["unknown", "shadow", "stellar"]]
            return type_names
    except Exception:
        
        return []

async def get_all_generations() -> List[Dict]:
    """Fetches a list of all official Pokémon generations."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://pokeapi.co/api/v2/generation")
            response.raise_for_status()
            data = response.json()
            generation_list = [
                {
                    "id": int(g["url"].split("/")[-2]),
                    "name": g["name"].replace("generation-", "").upper()
                }
                for g in data["results"]
            ]
            return generation_list
    except Exception:
        
        return []