from playwright.sync_api import Page
from .base_page import BasePage
from tests.e2e.components.pokemon_grid import PokemonGridComponent

class MainPokedexPage(BasePage):
    """
    The MainPokedexPage class represents the main Pokédex page of the application.
    It extends the BasePage class and includes specific elements and functionalities
    related to the Pokédex page, such as interacting with the Pokémon grid.
    """
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.pokemon_grid = PokemonGridComponent(page)


    def navigate(self):
        """Navigates to the main Pokédex page."""
        self.page.goto(self.URL)
        
        return self