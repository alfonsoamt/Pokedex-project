from playwright.sync_api import Page


class BasePage:
    """
    The BasePage class serves as a foundation for all other page objects.
    It contains common elements and functionalities that are shared across
    multiple pages of the application.
    """

    def __init__(self, page: Page):
        self.page = page
        self.body = page.locator("body")


    def get_title(self) -> str:
        """Returns the title of the current page."""
        return self.page.title()
    
    def wait_for_url(self, url_pattern: str, **kwargs):
        """Waits for the page URL to match the given pattern."""
        self.page.wait_for_url(url_pattern, **kwargs)
        
