import pytest
from playwright.sync_api import Page, expect
from tests.e2e.pages.main_pokedex_page import MainPokedexPage


@pytest.mark.e2e
def test_filter_by_single_type(page: Page):
    """
    Covers Test Case TC-E-TYP-001: Verify filtering by a single type.
    """
    # 1. ARRANGE
    # The test setup is handled by the MainPokedexPage object.
    pokedex_page = MainPokedexPage(page)

    # 2. ACT
    # Load the page and wait for it to be ready.
    pokedex_page.load()

    # Perform the main user action using the high-level API from our POM.
    pokedex_page.filter_panel.filter_by_type("fire")

    # 3. ASSERT
    # Assertions are made using the component's methods and Playwright's `expect`.
    # This is where the detailed validation logic will go.
    
    # Example (conceptual):
    # first_card = pokedex_page.pokemon_grid.get_card_by_name("Charmander")
    # expect(first_card).to_be_visible()
    #
    # all_cards = pokedex_page.pokemon_grid.get_all_cards()
    # for card in all_cards:
    #     card_types = get_types_from_card(card) # This would be a helper or a method on the card component
    #     expect("fire" in card_types).to_be_true()
    pass


@pytest.mark.e2e
def test_initial_load_and_card_content(page: Page):
    """
    Covers Test Case TC-E-GRD-001: Verify card content.
    """
    # 1. ARRANGE
    pokedex_page = MainPokedexPage(page)

    # 2. ACT
    pokedex_page.load()

    # 3. ASSERT
    # Get the first card from the grid component.
    first_card = pokedex_page.pokemon_grid.pokemon_cards.first
    expect(first_card).to_be_visible()

    # Example of a more detailed assertion (conceptual):
    # card_name = first_card.locator(".pokemon-name").text_content()
    # expect(card_name).to_equal("Bulbasaur")
    pass
