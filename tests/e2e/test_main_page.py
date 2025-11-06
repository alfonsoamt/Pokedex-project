import pytest
from playwright.sync_api import Page, expect
from tests.e2e.pages.main_pokedex_page import MainPokedexPage


POKEMON_CARD_DATA = [
    (1, "Bulbasaur",["Grass", "Poison"]), 
    (9, "Blastoise", ["Water"]), 
    (21, "Spearow", ["Normal", "Flying"])
    ]

class TestGridVisualization:
    @pytest.mark.parametrize("pokemon_id, pokemon_name, pokemon_types", POKEMON_CARD_DATA)
    def test_verify_card_content(self, page: Page, pokemon_id: int, pokemon_name: str, pokemon_types: list[str]):
        # Arrange - Page Object for Main Pokedex Page
        main_pokedex_page = MainPokedexPage(page)
        main_pokedex_page.navigate()
        #page.pause()

        # Act - Get the Pokémon card by Name
        pokemon_card = main_pokedex_page.pokemon_grid.get_card_by_name(pokemon_name)
        pokemon_number = pokemon_card.pokemon_number
        pokemon_name = pokemon_card.pokemon_name
        pokemon_types = pokemon_card.pokemon_types
        pokemon_sprite_url = pokemon_card.image_url
        expected_sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"

        # Assert - Verify the card content
        assert int(pokemon_number[1:]) == pokemon_id
        assert pokemon_name == pokemon_name
        assert pokemon_types == pokemon_types
        assert pokemon_sprite_url == expected_sprite_url

