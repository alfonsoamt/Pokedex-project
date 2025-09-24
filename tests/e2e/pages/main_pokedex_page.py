from playwright.sync_api import Page
from tests.e2e.pages.base_page import BasePage
from tests.e2e.components.filter_panel import FilterPanelComponent
from tests.e2e.components.pokemon_grid import PokemonGridComponent


class MainPokedexPage(BasePage):
    """
    The Page Object for the main Pokedex application page.

    This class orchestrates the different components of the page, such as the
    filter panel and the pokemon grid. It provides a high-level API for tests
    to interact with the page.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Component initialization
        self.filter_panel = FilterPanelComponent(page)
        self.pokemon_grid = PokemonGridComponent(page)
        # Other components like a search bar or pagination can be added here

    def load(self):
        """Loads the main page and waits for the grid to be ready."""
        self.navigate()
        self.pokemon_grid.wait_for_grid_to_load()
