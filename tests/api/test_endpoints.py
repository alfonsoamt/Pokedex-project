import pytest
from pydantic import ValidationError
from tests.api.models.response_models import Generation

def test_get_generations(api_client):
    """
    Test the GET /generations endpoint to ensure it returns a list of generations.
    ARGS:
        api_client (ApiClient): The API client fixture for making requests.
    """

    response = api_client.get("/generations")
    response_json = response.json()
    assert response.status_code == 200, "Expected status code 200"
    
    try:
        generations_response = [Generation(**generation) for generation in response_json]

    except ValidationError as e:
        pytest.fail(f"Response validation failed the contract ERRORS:\n {e.json(indent=2)}")
