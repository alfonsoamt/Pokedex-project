import requests
from requests import Response
from core.config import settings


class ApiClient:
    """A generic API client to handle HTTP requests."""

    def __init__(self):
        """Initializes the ApiClient, setting the base URL and a session object."""
        self.base_url = settings.api_base_url
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict = None) -> Response:
        """
        Performs a GET request to a specified endpoint.

        Args:
            endpoint: The API endpoint to call (e.g., '/pokemons').
            params: A dictionary of query parameters to include in the request.

        Returns:
            The full Response object from the requests library.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params)

    def post(self, endpoint: str, data: dict = None, json: dict = None) -> Response:
        """
        Performs a POST request to a specified endpoint.

        Args:
            endpoint: The API endpoint to call.
            data: Dictionary to send in the body of the request (form-encoded).
            json: Dictionary to send in the body of the request (JSON-encoded).

        Returns:
            The full Response object from the requests library.
        """
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, data=data, json=json)
