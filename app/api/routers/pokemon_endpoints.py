from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse
from app.api.services import pokemon_service
import json
from typing import List, Optional

router = APIRouter(prefix="/api")

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

async def sse_generator(page: int, limit: int, types: Optional[List[str]] = None, generation: Optional[int] = None):
    """Generator that yields Server-Sent Events."""
    async for item in pokemon_service.get_streamed_pokemons(page=page, limit=limit, types=types, generation=generation):
        yield f"data: {json.dumps(item)}\n\n"

@router.get("/pokemons/stream")
async def stream_pokemons(
    page: int = Query(1, ge=1),
    limit: int = Query(21, ge=1, le=100),
    types: Optional[List[str]] = Query(None),
    generation: Optional[int] = Query(None, ge=1)
):
    """
    Streams a paginated list of Pokemon using Server-Sent Events.
    Can be filtered by one or two types.
    """
    return StreamingResponse(sse_generator(page, limit, types, generation), media_type="text/event-stream")
