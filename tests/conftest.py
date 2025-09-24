import pytest
from core.api_client import ApiClient


import pytest
from core.api_client import ApiClient


@pytest.fixture(scope="session")
def api_client(request):
    """
    Pytest fixture to provide a single instance of the ApiClient for the entire test session.

    It reads the base_url from the [api] section of the pytest.ini file.
    This follows the dependency injection pattern and handles setup/teardown.

    Yields:
        ApiClient: An instance of the API client.
    """
    api_base_url = request.config.getini("api_base_url")
    client = ApiClient(base_url=api_base_url)
    yield client
    # Teardown: close the session after all tests are done
    print("Closing API client session...")
    client.session.close()
