# 📡 API Test Cases

## Endpoint: `/api/pokemons/stream`

<details>
<summary>🔴 <strong>TC-A-STR-001: Verify default response (no parameters)</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To ensure the endpoint provides a valid, default, paginated response when called without any parameters. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** None

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The response is a valid Server-Sent Event stream. Each event's data is a JSON object containing `pokemons` (a list of objects matching the Pokémon schema) and `pagination` (an object with `total_pages` and `current_page` keys). The `current_page` should be `1`.
---
</details>

<details>
<summary>🔴 <strong>TC-A-STR-002: Verify `page` and `limit` parameters control pagination correctly</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To verify the core pagination logic of the endpoint. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?page=2&limit=10`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The `pagination` object in the response data should have `current_page` equal to `2`. The `pokemons` list should contain exactly 10 items, corresponding to the Pokémon for that page.
---
</details>

<details>
<summary>🔴 <strong>TC-A-STR-003: Verify `types` parameter filters by one or two types</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To verify the type filtering logic, which is a primary feature of the application. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?types=fire,flying`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** Every Pokémon object in the `pokemons` list must have both "fire" and "flying" in its `types` array.
---
</details>

<details>
<summary>🟠 <strong>TC-A-STR-004: Verify `generation` parameter filters by generation ID</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To verify the generation filtering logic at the API level. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?generation=1`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** All Pokémon in the `pokemons` list must have a Pokédex ID between 1 and 151.
---
</details>

<details>
<summary>🟠 <strong>TC-A-STR-005: Verify `pokemon_id` parameter returns a single, specific Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To verify the functionality of fetching a single Pokémon by its ID, used by the search feature. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?pokemon_id=25`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The `pokemons` list in the response data must contain exactly one object, and its `name` field must be "pikachu".
---
</details>

<details>
<summary>🟠 <strong>TC-A-STR-006: Verify `pokemon_ids` parameter returns a specific list of Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To verify the backend logic for the "Surprise Me" feature. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?pokemon_ids=1,4,7`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The `pokemons` list must contain exactly three objects with the names "bulbasaur", "charmander", and "squirtle".
---
</details>

<details>
<summary>🟠 <strong>TC-A-STR-007: Verify combined filtering (`types` and `generation`)</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To ensure the API correctly handles the combination of multiple different filter parameters. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** `?generation=1&types=water`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** All Pokémon in the response must belong to Generation 1 AND have "water" in their `types` array.
---
</details>

<details>
<summary>🔴 <strong>TC-A-STR-008: Verify response schema is correct for all valid requests (Covered by other tests)</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To ensure the data contract between the backend and any client is strictly maintained, preventing integration issues. |
| **Note** | *This is a cross-cutting concern, not a standalone test. It is considered `PASSED` if the Pydantic schema validation within tests `TC-A-STR-001` through `TC-A-STR-007` executes successfully for each case.* |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/stream`
*   **Parameters:** Any valid combination of parameters.

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The entire JSON payload must strictly adhere to the defined OpenAPI schema, validating all data types, required fields, and object structures.
---
</details>

<details>
<summary>🟠 <strong>TC-A-STR-009: Verify handling of invalid parameters</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To ensure the API is robust against bad input and provide meaningful client-side error messages. |

**Request (Examples):**
1.  `GET /api/pokemons/stream?page=-1`
2.  `GET /api/pokemons/stream?types=invalidtype`
3.  `GET /api/pokemons/stream?limit=9999`

**Expected Response:**
*   **Status Code:** `422 Unprocessable Entity`
*   **Body (Schema):** The response body should contain a `detail` field explaining which parameter is invalid and why.
---
</details>

---

## Endpoint: `/api/types`

<details>
<summary>🔴 <strong>TC-A-TYP-001: Verify endpoint returns a list of all Pokémon types</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To verify the endpoint returns a complete and accurate list of all available Pokémon types for filtering. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/types`
*   **Parameters:** None

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The response is a JSON array of strings, where each string is a valid Pokémon type (e.g., `["normal", "fire", "water", "electric", ...]` ). The list should contain all 18 official types.
---
</details>

<details>
<summary>🔴 <strong>TC-A-TYP-002: Verify response schema is correct</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To ensure the data contract for the types endpoint is strictly maintained, preventing integration issues with the frontend. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/types`
*   **Parameters:** None

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The entire JSON payload must be a valid `Array[string]`.
---
</details>

---

## Endpoint: `/api/generations`

<details>
<summary>🔴 <strong>TC-A-GEN-001: Verify endpoint returns a list of all Pokémon generations</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To verify the endpoint returns a complete and accurate list of all available Pokémon generations for filtering. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/generations`
*   **Parameters:** None

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The response is a JSON array of objects. Each object must contain an `id` (integer) and a `name` (string), (e.g., `[{"id": 1, "name": "generation-i"}, ...]` ).
---
</details>

<details>
<summary>🔴 <strong>TC-A-GEN-002: Verify response schema is correct</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🔴 `Critical` |
| **Objective** | To ensure the data contract for the generations endpoint is strictly maintained. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/generations`
*   **Parameters:** None

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The entire JSON payload must be a valid `Array[Object]` where each object conforms to the schema `{"id": integer, "name": string}`.
---
</details>

---

## Endpoint: `/api/pokemons/names_autocomplete`

<details>
<summary>🟠 <strong>TC-A-SRC-001: Verify `query` parameter returns matching Pokémon names</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To verify that the autocomplete feature returns relevant Pokémon names based on a partial query string. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/names_autocomplete`
*   **Parameters:** `?query=pika`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The response is a JSON array of objects. It should contain an object for Pikachu: `{"id": 25, "name": "pikachu"}`.
---
</details>

<details>
<summary>🟠 <strong>TC-A-SRC-002: Verify response schema is correct</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟠 `High` |
| **Objective** | To ensure the data contract for the autocomplete endpoint is strictly maintained. |

**Request:**
*   **Method:** `GET`
*   **Endpoint:** `/api/pokemons/names_autocomplete`
*   **Parameters:** `?query=char`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The entire JSON payload must be a valid `Array[Object]` where each object conforms to the schema `{"id": integer, "name": string}`.
---
</details>

<details>
<summary>🟡 <strong>TC-A-SRC-003: Verify handling of short or non-matching queries</strong></summary>

| | |
| :--- | :--- |
| **Priority** | 🟡 `Medium` |
| **Objective** | To ensure the endpoint handles queries that are too short or have no matches gracefully by returning an empty list. |

**Request (Examples):**
1.  `GET /api/pokemons/names_autocomplete?query=a`
2.  `GET /api/pokemons/names_autocomplete?query=nonexistentpokemon`

**Expected Response:**
*   **Status Code:** `200 OK`
*   **Body (Schema):** The response body for both requests should be an empty JSON array `[]`.
---
</details>

