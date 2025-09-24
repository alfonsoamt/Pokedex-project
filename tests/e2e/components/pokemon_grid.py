from playwright.sync_api import Page, Locator
from typing import List


class PokemonGridComponent:
    """
    This component handles all interactions with the Pokémon grid itself,
    such as retrieving cards, getting card data, and checking grid state.
    """

    def __init__(self, page: Page):
        self.page = page
        # Locators for the grid elements
        self.grid_container = page.locator("#pokemon-grid")
        self.pokemon_cards = self.grid_container.locator(".pokemon-card")

    def get_all_cards(self) -> List[Locator]:
        """Returns a list of all Pokémon card locators currently visible."""
        return self.pokemon_cards.all()

    def get_card_by_name(self, name: str) -> Locator:
        """Finds and returns a specific Pokémon card locator by the Pokémon's name."""
        return self.pokemon_cards.filter(has_text=name)

    def wait_for_grid_to_load(self):
        """Waits for the first card to be visible, indicating the grid has loaded."""
        self.pokemon_cards.first.wait_for(state="visible")
