from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse
from app.api.services import pokemon_service
import json
from typing import List, Optional

router = APIRouter(prefix="/api")

@router.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return JSONResponse(content={"status": "ok"})

@router.get("/types")
async def get_pokemon_types():
    """Endpoint to get a list of all Pokémon types."""
    types = await pokemon_service.get_all_types()
    return JSONResponse(content=types)

@router.get("/generations")
async def get_pokemon_generations():
    """Endpoint to get a list of all Pokémon generations."""
    generations = await pokemon_service.get_all_generations()
    return JSONResponse(content=generations)

@router.get("/pokemons/names_autocomplete")
async def get_pokemon_names_autocomplete(query: str = Query(..., min_length=1)):
    """Endpoint to get Pokémon names for autocomplete based on a partial query."""
    names = await pokemon_service.get_pokemon_names_by_partial_match(query)
    return JSONResponse(content=names)

async def sse_generator(page: int, limit: int, types: Optional[List[str]] = None, generation: Optional[int] = None, pokemon_id: Optional[int] = None, pokemon_ids: Optional[List[int]] = None):
    """Generator that yields Server-Sent Events."""
    async for item in pokemon_service.get_streamed_pokemons(page=page, limit=limit, types=types, generation=generation, pokemon_id=pokemon_id, pokemon_ids=pokemon_ids):
        yield f"data: {json.dumps(item)}\n\n"

@router.get("/pokemons/stream")
async def stream_pokemons(
    page: int = Query(1, ge=1),
    limit: int = Query(21, ge=1, le=100),
    types: Optional[List[str]] = Query(None),
    generation: Optional[int] = Query(None, ge=1),
    pokemon_id: Optional[int] = Query(None, ge=1),
    pokemon_ids: Optional[List[int]] = Query(None)
):
    """
    Streams a paginated list of Pokemon using Server-Sent Events.
    Can be filtered by one or two types.
    """
    return StreamingResponse(sse_generator(page, limit, types, generation, pokemon_id, pokemon_ids), media_type="text/event-stream")
