import httpx

async def  get_pokemon_basic_info(pokemon:str) -> dict:
    """
    Fetches basic information about a pokemon from the PokeAPI.
    Args:
        pokemon (str): The name or ID of the pokemon.
    Returns:
        pokedata (dict): A dictionary containing basic information about the pokemon."""
    
    print(f"Fetching data for {pokemon} from PokeAPI...")
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"

    async with httpx.AsyncClient() as client:
        try: 
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            raw_data = response.json()
            pokedata = {
                "id": raw_data.get("id"),
                "name": raw_data.get("name"),
                "height": raw_data.get("height")/10,  # Convert height to meters
                "weight": raw_data.get("weight")/10,  # Convert weight to kg
                "types": [type_info["type"]["name"] for type_info in raw_data.get("types", [])],
                "sprite": raw_data.get("sprites", {}).get("front_default"),
            }
            return pokedata

        except httpx.RequestException as e:
            print(f"SERVICE ERROR: Error fetching data from PokeAPI: {e}")
            return {"error": "Failed to retrieve data from PokeAPI."}