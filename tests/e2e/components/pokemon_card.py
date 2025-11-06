from playwright.sync_api import Page, Locator
from typing import List

class PokemonCardComponent:
    """This represent a single card with the Pokemon information."""
    
    def __init__(self, root_locator: Locator):
        """Initialize the root container locator. This 'root_locator' should point to a single card."""
        self.root = root_locator # .pokemon-card.pokemon-entrance

        # Locators for elements within the card
        self._image = self.root.locator("div.sprite-container img")
        self._name = self.root.locator("div.info-panel h2.pokemon-name")
        self._number = self.root.locator("span.pokemon-number")
        self._types = self.root.locator("div.types-container span.type-badge")

    @property
    def image_url(self) -> str:
        """Return the URL of the Pokemon sprite image."""
        return self._image.get_attribute("src")
    
    @property
    def pokemon_name(self) -> str:
        """Return the name of the Pokemon."""
        return self._name.text_content()
    
    @property
    def pokemon_number(self) -> str:
        """Return the Pokedex number of the Pokemon."""
        return self._number.text_content()
    
    @property
    def pokemon_types(self) -> List[str]:
        """Return a list of types associated with the Pokemon."""
        return [_type.text_content() for _type in self._types.all()]