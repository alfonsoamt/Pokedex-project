from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.api.services import pokemon_service
import json

router = APIRouter(prefix="/api")

async def sse_generator(page: int, limit: int):
    """Generator that yields Server-Sent Events."""
    async for item in pokemon_service.get_streamed_pokemons(page=page, limit=limit):
        yield f"data: {json.dumps(item)}\n\n"

@router.get("/pokemons/stream")
async def stream_pokemons(page: int = Query(1, ge=1), limit: int = Query(21, ge=1, le=100)):
    """
    Streams a paginated list of Pokemon using Server-Sent Events.
    """
    return StreamingResponse(sse_generator(page, limit), media_type="text/event-stream")
