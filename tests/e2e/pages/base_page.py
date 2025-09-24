from playwright.sync_api import Page


class BasePage:
    """
    The BasePage class serves as a foundation for all other page objects.
    It contains common elements and functionalities that are shared across
    multiple pages of the application.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/"):
        """Navigates to a specific path. Relies on the `base_url` from playwright.config."""
        self.page.goto(path)
