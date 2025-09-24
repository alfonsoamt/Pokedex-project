import httpx
import asyncio
import math
from typing import AsyncGenerator, Dict, List, Optional, Set
from cachetools import TTLCache

# --- Constants ---
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"



# --- Cache Setup ---
pokemon_cache = TTLCache(maxsize=1024, ttl=3600)
_all_pokemon_names: List[Dict] = []

# --- Autocomplete and Basic Info Fetchers ---

async def _fetch_all_pokemon_names():
    """Fetches all Pokémon names and their IDs for autocomplete caching."""
    global _all_pokemon_names
    if not _all_pokemon_names:
        url = f"{POKEAPI_BASE_URL}/pokemon?limit=10000"
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
                print(f"Error fetching all pokemon names for autocomplete: {e}")

async def get_pokemon_names_by_partial_match(query: str) -> List[Dict]:
    """Returns a list of Pokémon names and IDs that partially match the query."""
    if not _all_pokemon_names:
        await _fetch_all_pokemon_names()
    if not query:
        return []
    query_lower = query.lower()
    matches = [p for p in _all_pokemon_names if query_lower in p["name"].lower()]
    return matches[:10]

async def get_pokemon_basic_info(pokemon_id: int) -> Dict:
    """Get basic info for a single Pokemon, using a cache."""
    if pokemon_id in pokemon_cache:
        return pokemon_cache[pokemon_id]
    url = f"{POKEAPI_BASE_URL}/pokemon/{pokemon_id}"
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

# --- Helper Functions ---

def _get_id_from_url(url: str) -> int:
    """Extracts a numeric ID from a PokeAPI URL."""
    return int(url.split("/")[-2])

async def _fetch_pokemon_ids_by_type(type_name: str, client: httpx.AsyncClient) -> Set[int]:
    """Fetches a set of Pokémon IDs for a given type."""
    type_url = f"{POKEAPI_BASE_URL}/type/{type_name.lower()}"
    response = await client.get(type_url)
    response.raise_for_status()
    data = response.json()
    return {_get_id_from_url(p["pokemon"]["url"]) for p in data["pokemon"]}

async def _fetch_pokemon_ids_by_generation(gen_id: int, client: httpx.AsyncClient) -> Set[int]:
    """Fetches a set of Pokémon IDs for a given generation."""
    gen_url = f"{POKEAPI_BASE_URL}/generation/{gen_id}"
    response = await client.get(gen_url)
    response.raise_for_status()
    data = response.json()
    return {_get_id_from_url(spec["url"]) for spec in data["pokemon_species"]}

# --- Streaming Sub-Functions (Refactored Logic) ---

async def _stream_by_ids(pokemon_ids: List[int]) -> AsyncGenerator[Dict, None]:
    """Streams a specific list of Pokémon by their IDs."""
    total_items = len(pokemon_ids)
    yield {"type": "pagination", "data": {"total_items": total_items, "total_pages": 1, "current_page": 1}}
    for pid in pokemon_ids:
        pokemon_data = await get_pokemon_basic_info(pid)
        if "error" not in pokemon_data:
            yield {"type": "pokemon", "data": pokemon_data}

async def _stream_by_single_id(pokemon_id: int) -> AsyncGenerator[Dict, None]:
    """Streams a single Pokémon by its ID."""
    pokemon_data = await get_pokemon_basic_info(pokemon_id)
    if "error" not in pokemon_data:
        yield {"type": "pagination", "data": {"total_items": 1, "total_pages": 1, "current_page": 1}}
        yield {"type": "pokemon", "data": pokemon_data}
    else:
        yield {"type": "error", "data": {"message": f"Pokémon with ID {pokemon_id} not found."}}

async def _stream_with_filters(page: int, limit: int, types: List[str], generation: Optional[int]) -> AsyncGenerator[Dict, None]:
    """Streams Pokémon that match type and/or generation filters."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        if types:
            for type_name in types[:2]:
                tasks.append(_fetch_pokemon_ids_by_type(type_name, client))
        if generation:
            tasks.append(_fetch_pokemon_ids_by_generation(generation, client))
        
        results = await asyncio.gather(*tasks)
        intersected_ids = set.intersection(*results)
        final_ids = sorted(list(intersected_ids))
        total_items = len(final_ids)
        
        offset = (page - 1) * limit
        paginated_ids = final_ids[offset:offset + limit]

    total_pages = math.ceil(total_items / limit) if total_items > 0 else 1
    yield {"type": "pagination", "data": {"total_items": total_items, "total_pages": total_pages, "current_page": page}}

    for pid in paginated_ids:
        if pid > 1025: continue
        pokemon_data = await get_pokemon_basic_info(pid)
        yield {"type": "pokemon", "data": pokemon_data}

async def _stream_default_paginated(page: int, limit: int) -> AsyncGenerator[Dict, None]:
    """Streams a paginated list of all Pokémon."""
    total_items = 1025
    offset = (page - 1) * limit
    list_url = f"{POKEAPI_BASE_URL}/pokemon?limit={limit}&offset={offset}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(list_url)
        response.raise_for_status()
        paginated_ids = [_get_id_from_url(p["url"]) for p in response.json().get("results", [])]

    total_pages = math.ceil(total_items / limit)
    yield {"type": "pagination", "data": {"total_items": total_items, "total_pages": total_pages, "current_page": page}}

    for pid in paginated_ids:
        if pid > 1025: continue
        pokemon_data = await get_pokemon_basic_info(pid)
        yield {"type": "pokemon", "data": pokemon_data}

# --- Main Service Function (Dispatcher) ---

async def get_streamed_pokemons(
    page: int, limit: int, types: Optional[List[str]] = None, 
    generation: Optional[int] = None, pokemon_id: Optional[int] = None, 
    pokemon_ids: Optional[List[int]] = None
) -> AsyncGenerator[Dict, None]:
    """
    Streams Pokémon data by dispatching to the appropriate specialized function.
    """
    try:
        streamer = None
        if pokemon_ids:
            streamer = _stream_by_ids(pokemon_ids)
        elif pokemon_id:
            streamer = _stream_by_single_id(pokemon_id)
        elif types or generation:
            streamer = _stream_with_filters(page, limit, types, generation)
        else:
            streamer = _stream_default_paginated(page, limit)
        
        async for item in streamer:
            yield item
            
        yield {"type": "done", "data": {"message": "Stream complete"}}

    except Exception as e:
        yield {"type": "error", "data": {"message": str(e)}}

# --- API Data Fetchers ---

async def get_all_types() -> List[str]:
    """Fetches a list of all official Pokémon type names."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/type")
            response.raise_for_status()
            data = response.json()
            return [t["name"] for t in data["results"] if t["name"] not in ["unknown", "shadow", "stellar"]]
    except Exception:
        return []

async def get_all_generations() -> List[Dict]:
    """Fetches a list of all official Pokémon generations."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{POKEAPI_BASE_URL}/generation")
            response.raise_for_status()
            data = response.json()
            return [
                {"id": int(g["url"].split("/")[-2]), "name": g["name"].replace("generation-", "").upper()}
                for g in data["results"]
            ]
    except Exception:
        return []
