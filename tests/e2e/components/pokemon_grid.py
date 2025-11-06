from playwright.sync_api import Page, Locator
from typing import List

from .pokemon_card import PokemonCardComponent


class PokemonGridComponent:
    """
    This component handles all interactions with the Pokémon grid itself,
    such as retrieving cards, getting card data, and checking grid state.
    """

    def __init__(self, page: Page):
        self.page = page
        # Locators for the grid element
        self._grid_container = page.locator("#pokedex-grid")
        # Locator for all Pokémon cards within the grid
        self._pokemon_cards = self._grid_container.locator(".pokemon-card.card-entrance")

    def get_all_cards(self) -> List[PokemonCardComponent]:
        """Returns a list of all Pokémon card locators currently visible."""
        return [PokemonCardComponent(card) for card in self._pokemon_cards.all()]

    def get_card_by_name(self, name: str) -> PokemonCardComponent:
        """Finds and returns a specific Pokémon card component by the Pokémon's name."""
        # This locator finds a card that has a descendant img with a specific, case-sensitive alt text.
        card_locator = self._grid_container.locator(f".pokemon-card.card-entrance:has(img[alt='{name}'])")
        
        # Wait for the located card to be visible to ensure it's ready for interaction.
        card_locator.wait_for(state="visible", timeout=15000)

        return PokemonCardComponent(card_locator)