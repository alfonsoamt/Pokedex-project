import pytest
from core.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    """
    Pytest fixture to provide a single instance of the ApiClient for the entire test session.

    This follows the dependency injection pattern and handles setup/teardown.

    Yields:
        ApiClient: An instance of the API client.
    """
    client = ApiClient()
    yield client
    # Teardown: close the session after all tests are done
    print("Closing API client session...")
    client.session.close()
