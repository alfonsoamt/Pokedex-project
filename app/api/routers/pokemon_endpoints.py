from fastapi import APIRouter, Query
from typing import List, Dict
from app.api.services import pokemon_service

router = APIRouter(prefix="/api")

@router.get("/generation/{gen_id}")
async def get_pokemon_generation(gen_id: int):
    """Get all Pokemon from a specific generation"""
    start_id = 1
    count = 151 if gen_id == 1 else 0  # For now, only handling gen 1
    return await pokemon_service.get_pokemon_batch(start_id, count)

@router.get("/pokemon/batch")
async def get_pokemon_batch(start: int = Query(1), count: int = Query(12)):
    """Get a batch of Pokemon"""
    return await pokemon_service.get_pokemon_batch(start, count)