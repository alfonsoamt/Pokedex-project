import json
import pytest
from pydantic import ValidationError
from tests.api.models.response_models import StreamEvents, PaginationEvent, PokemonEvent, DoneEvent

# Generation ranges to validate generation filtering
GENERATION_RANGES = {
    1: (1, 151),
    2: (152, 251),
    3: (252, 386),
    4: (387, 493),
    5: (494, 649),
    6: (650, 721),
    7: (722, 809),
    8: (810, 905),
    9: (906, 1025),
}


@pytest.mark.parametrize(
    "test_id, params, expected_assertions",
    [
        # TC-A-STR-001: Default response
        pytest.param(
            "TC-A-STR-001",
            {},
            {"expected_page": 1},
            id="TC-A-STR-001: Default response"
        ),
        # TC-A-STR-002: Pagination
        pytest.param(
            "TC-A-STR-002",
            {"page": 2, "limit": 10},
            {"expected_page": 2, "expected_count": 10},
            id="TC-A-STR-002: Pagination"
        ),
        # TC-A-STR-003: Single type filter
        pytest.param(
            "TC-A-STR-003.1",
            {"types": "water"},
            {"expected_types": ["water"]},
            id="TC-A-STR-003: Filter by single type"
        ),
        # TC-A-STR-003: Double type filter
        pytest.param(
            "TC-A-STR-003.2",
            {"types": ["fire", "flying"]},
            {"expected_types": ["fire", "flying"]},
            id="TC-A-STR-003: Filter by two types"
        ),
        # TC-A-STR-004: Generation filter
        pytest.param(
            "TC-A-STR-004",
            {"generation": 1},
            {"expected_generation": 1},
            id="TC-A-STR-004: Filter by generation"
        ),
        # TC-A-STR-005: Specific Pokemon ID
        pytest.param(
            "TC-A-STR-005",
            {"pokemon_id": 25},
            {"expected_count": 1, "expected_pokemon_names": ["Pikachu"]},
            id="TC-A-STR-005: Fetch by pokemon_id"
        ),
        # TC-A-STR-006: Specific list of Pokemon IDs
                    pytest.param(
                        "TC-A-STR-006",
                        {"pokemon_ids": [1, 4, 7]},
                        {"expected_count": 3, "expected_pokemon_names": ["Bulbasaur", "Charmander", "Squirtle"]},
                        id="TC-A-STR-006: Fetch by list of ids"
                    ),        # TC-A-STR-007: Combined filter
        pytest.param(
            "TC-A-STR-007",
            {"generation": 1, "types": "water"},
            {"expected_generation": 1, "expected_types": ["water"]},
            id="TC-A-STR-007: Combined filter"
        ),
    ]
)
def test_pokemon_stream_parameterized(api_client, test_id, params, expected_assertions):
    """
    A parameterized test for the /pokemons/stream endpoint covering multiple test cases.
    This test validates both the response contract and the data correctness.
    """
    # 1. Make the API call with the provided parameters
    response = api_client.get("/pokemons/stream", params=params)
    assert response.status_code == 200, f"[{test_id}] Expected status code 200"

    # 2. Process and validate the stream contract
    stream_lines = response.text.strip().split('\n\n')
    json_events = [json.loads(line.replace('data: ', '')) for line in stream_lines if line.startswith('data: ')]

    try:
        validated_stream = StreamEvents.model_validate(json_events)
    except ValidationError as e:
        pytest.fail(f"[{test_id}] Stream validation failed the contract. ERRORS:\n{e}")

    # 3. Separate events for easier data validation
    events = validated_stream.root
    pagination_event = next((e for e in events if isinstance(e, PaginationEvent)), None)
    pokemon_events = [e for e in events if isinstance(e, PokemonEvent)]
    done_event = next((e for e in events if isinstance(e, DoneEvent)), None)

    # --- Contract Assertions ---
    assert pagination_event is not None, f"[{test_id}] Pagination event is missing"
    assert done_event is not None, f"[{test_id}] Done event is missing"

    # --- Data Assertions ---
    if "expected_page" in expected_assertions:
        assert pagination_event.data.current_page == expected_assertions["expected_page"], \
            f"[{test_id}] Incorrect page number"

    if "expected_count" in expected_assertions:
        assert len(pokemon_events) == expected_assertions["expected_count"], \
            f"[{test_id}] Incorrect number of pokemon returned"

    if "expected_types" in expected_assertions:
        for event in pokemon_events:
            for type_name in expected_assertions["expected_types"]:
                assert type_name in event.data.types, \
                    f"[{test_id}] Pokemon {event.data.name} should have type '{type_name}'"

    if "expected_generation" in expected_assertions:
        gen_range = GENERATION_RANGES[expected_assertions["expected_generation"]]
        for event in pokemon_events:
            assert gen_range[0] <= event.data.id <= gen_range[1], \
                f"[{test_id}] Pokemon {event.data.name} (ID: {event.data.id}) is not in Generation {expected_assertions['expected_generation']}"

    if "expected_pokemon_names" in expected_assertions:
        # Sort both lists to ensure comparison is order-independent
        returned_names = sorted([e.data.name for e in pokemon_events])
        expected_names = sorted(expected_assertions["expected_pokemon_names"])
        assert returned_names == expected_names, \
            f"[{test_id}] Returned pokemon names do not match expected names"


@pytest.mark.parametrize(
    "test_id, params",
    [
        ("TC-A-STR-009.1", {"page": -1}),
        ("TC-A-STR-009.2", {"limit": 9999}),
        ("TC-A-STR-009.3", {"types": "invalid-type"}),
        ("TC-A-STR-009.4", {"generation": 99}),
    ]
)
def test_pokemon_stream_invalid_parameters(api_client, test_id, params):
    """
    TC-A-STR-009: Verify handling of invalid parameters.
    The API should return a 422 Unprocessable Entity status code.
    """
    response = api_client.get("/pokemons/stream", params=params)
    assert response.status_code == 422, f"[{test_id}] Expected status code 422 for invalid parameters"
