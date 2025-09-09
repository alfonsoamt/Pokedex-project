# 📋 Pokedex Project - Test Plan V1.0

> This document outlines the detailed testing plan for the Pokedex Project V1.0. It defines the scope, approach, resources, and quality gates required to validate the release.

---

## 1.- 🎯 Introduction & Purpose

This document details the comprehensive testing plan for the **Pokedex Project V1.0**. Its purpose is to guide all testing activities by defining the features to be tested, the criteria for success, the required environment, and the key deliverables. It serves as the central source of truth for the V1.0 testing effort.

## 2.- 🔭 Scope

The testing scope is aligned with the `TEST_STRATEGY.md` document.

### 2.1.- In Scope
-   All features defined for the MVP V1.0 in [`FEATURES.md`](../../FEATURES.md).
-   **API Testing:** Contract, schema, and functional validation of all backend endpoints.
-   **End-to-End (E2E) Testing:** Validation of critical user flows through the UI.
-   **UI/UX Validation:** Verification of the user interface against functional requirements, including responsiveness.
-   **Compatibility Testing:** Functional and visual validation on all **Tier 1** platforms and browsers as defined in the Test Strategy.

### 2.2.- Out of Scope
-   Formal load, stress, or any other type of performance testing beyond the baseline established in the Quality Objectives.
-   Exhaustive security or penetration testing.
-   Testing of the external PokeAPI service itself.
-   Testing on platforms or browsers not defined in the support matrix.

## 3.- 🧪 Test Approach

A multi-layered testing approach will be used to ensure comprehensive quality coverage:

-   **API/Integration Testing (Automated):** Endpoints will be validated using `Pytest` to verify contracts, status codes, and business logic.
-   **End-to-End Testing (Automated):** A regression suite will be built using `Playwright` to cover the main "happy path" scenarios for all critical features.
-   **Manual Exploratory Testing:** Manual testing will be conducted to explore edge cases, test usability, and identify issues that are difficult to cover with automation. The test cases in this plan will serve as a baseline for this activity.

## 4.- 🚀 Features to be Tested

The following features, as detailed in `FEATURES.md`, are in scope for testing:

-   **F-1.01:** Pokemon Grid visualization
-   **F-1.02:** Pagination
-   **F-1.03:** Type filter
-   **F-1.04:** Generation filter
-   **F-1.05:** Searchbar with autocomplete
-   **F-1.06:** Surprise me button

## 5.- ✅ Entry and Exit Criteria

These criteria determine when the formal testing cycle can begin and when it can be considered complete.

### 5.1.- Entry Criteria
-   The V1.0 build has been successfully deployed to a stable test environment.
-   All unit and API integration tests in the CI/CD pipeline are passing.
-   The `FEATURES.md` document is finalized, and all features are code-complete.

### 5.2.- Exit Criteria
-   100% of `Critical` and `High` priority manual test cases have been executed and are in a `Passed` state.
-   The automated E2E regression suite is fully passing.
-   There are **no open bugs** with `Critical` or `High` severity.
-   All Quality Objectives defined in `TEST_STRATEGY.md` have been met (e.g., Lighthouse score ≥ 85, API P95 response time < 800ms).

## 6.- 💻 Test Environment and Resources

-   **Test Environment URL:** [https://amt-pokedex.netlify.app/](https://amt-pokedex.netlify.app/)
-   **Browsers (Tier 1):** Chrome (Latest), Edge (Latest) on Windows 10/11.
-   **Tools:**
    -   Playwright (for E2E automation)
    -   Pytest (for API testing)
    -   Browser Developer Tools
    -   Google Lighthouse

## 7.-  deliverables

The following artifacts will be produced as part of the testing process:

-   This Test Plan document.
-   Manual test case suites.
-   Bug reports logged as GitHub Issues, clearly linked to test cases where applicable.
-   Automated test execution reports from the CI/CD pipeline (GitHub Actions).
-   A final Test Summary Report, including a Go/No-Go recommendation for the release.

## 8.- 🗺️ Test Case Coverage Matrix

This section provides a high-level overview of the test cases required to achieve full coverage for the v1.0 features, broken down by test type. It serves as a master list to define the scope of testing.

### End-to-End (E2E) Test Cases

*These tests validate the complete user-facing behavior as described in `FEATURES.md`.*

**Suite: Grid Visualization (GRD)**
- `TC-E-GRD-001`: Verify card content (sprite, name, number, types).
- `TC-E-GRD-002`: Verify default ascending order by Pokédex number.
- `TC-E-GRD-003`: Verify responsive grid layout on different screen sizes.
- `TC-E-GRD-004`: Verify card hover effect is present.
- `TC-E-GRD-005`: Verify skeleton loader is displayed during data fetch.

**Suite: Pagination (PAG)**
- `TC-E-PAG-001`: Verify clicking "Next" loads the subsequent set of Pokémon.
- `TC-E-PAG-002`: Verify clicking "Previous" loads the previous set of Pokémon.
- `TC-E-PAG-003`: Verify "Previous" button is disabled on the first page.
- `TC-E-PAG-004`: Verify "Next" button is disabled on the last page.

**Suite: Type Filter (TYP)**
- `TC-E-TYP-001`: Verify filtering by a single type.
- `TC-E-TYP-002`: Verify filtering by two types (AND logic).
- `TC-E-TYP-003`: Verify deselecting an active filter restores the previous state.
- `TC-E-TYP-004`: Verify clicking a third type filter has no effect (shake animation).
- `TC-E-TYP-005`: Verify "See All" button removes all active type filters.
- `TC-E-TYP-006`: Verify "No results found" message for non-matching type combinations.

**Suite: Generation Filter (GEN)**
- `TC-E-GEN-001`: Verify filtering by a single generation.
- `TC-E-GEN-002`: Verify combining a generation filter with a type filter.
- `TC-E-GEN-003`: Verify "No results found" message for non-matching generation/type combinations.

**Suite: Searchbar (SRC)**
- `TC-E-SRC-001`: Verify autocomplete suggestions appear after typing >= 2 characters.
- `TC-E-SRC-002`: Verify clicking a suggestion filters to that single Pokémon.
- `TC-E-SRC-003`: Verify filters and pagination are disabled after a successful search.
- `TC-E-SRC-004`: Verify clearing the search bar re-enables controls and restores the grid.
- `TC-E-SRC-005`: Verify "No results found" message for non-matching search terms.

**Suite: Surprise Me (RND)**
- `TC-E-RND-001`: Verify clicking the button displays 3 random Pokémon.
- `TC-E-RND-002`: Verify filters and pagination are disabled after a random search.

### API (Integration) Test Cases

*These tests validate the backend endpoints to ensure they behave as expected, handle parameters correctly, and manage errors gracefully.*

**Endpoint: `/api/pokemons/stream`**
- `TC-A-STR-001`: Verify default response (no parameters) returns the first page of Pokémon.
- `TC-A-STR-002`: Verify `page` and `limit` parameters control pagination correctly.
- `TC-A-STR-003`: Verify `types` parameter filters by one or two types.
- `TC-A-STR-004`: Verify `generation` parameter filters by generation ID.
- `TC-A-STR-005`: Verify `pokemon_id` parameter returns a single, specific Pokémon.
- `TC-A-STR-006`: Verify `pokemon_ids` parameter returns a specific list of Pokémon.
- `TC-A-STR-007`: Verify combined filtering (`types` and `generation`).
- `TC-A-STR-008`: Verify response schema is correct for all valid requests.
- `TC-A-STR-009`: Verify handling of invalid parameters (e.g., `page=-1`, `types=invalid`).

**Endpoint: `/api/types`**
- `TC-A-TYP-001`: Verify endpoint returns a list of all Pokémon types.
- `TC-A-TYP-002`: Verify response schema is correct.

**Endpoint: `/api/generations`**
- `TC-A-GEN-001`: Verify endpoint returns a list of all Pokémon generations.
- `TC-A-GEN-002`: Verify response schema is correct.

**Endpoint: `/api/pokemons/names_autocomplete`**
- `TC-A-SRC-001`: Verify `query` parameter returns matching Pokémon names.
- `TC-A-SRC-002`: Verify response schema is correct.
- `TC-A-SRC-003`: Verify handling of short or non-matching queries.

### Performance (Baseline) Test Cases

*These tests validate the application against the performance targets defined in the Quality Objectives.*

- `TC-P-API-001`: Measure P95 response time for all API endpoints under normal conditions.
- `TC-P-FE-001`: Measure Google Lighthouse score (Performance, Accessibility, Best Practices, SEO) on the main page.

## 9.- 📋 Manual Test Cases

The detailed manual test cases are maintained in separate suite files to keep this document concise and improve maintainability.

-   [**E2E Test Cases**](./Suites/01_E2E/E2E_Test_Cases.md)
-   [**API Test Cases**](./Suites/02_API/API_Test_Cases.md)
