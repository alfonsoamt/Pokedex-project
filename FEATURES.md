# 🚀 Pokedex Project - Features & Acceptance Criteria

> This document describes the features for the MVP v1.0, defining what is being built and its requirements.

---

# **🛠 MVP v1.0**

### **🎯 Feature 1.01:** *Pokémon Grid visualization*

**User story:** As a User, I want to visualize the Pokémon, so that I can see them, their names, number, and types.

#### ✅ Acceptance Criteria (AC)

1.  **AC-01 (Pokeball Card-View):**
    -   **GIVEN** I am on the main page
    -   **WHEN** The page loads at least one Pokémon
    -   **THEN** I can see a Card-View in a pokeball shape.

2.  **AC-02 (Card-View content):**
    -   **GIVEN** A Pokémon card is visible
    -   **WHEN** I view the card
    -   **THEN** I can see the Pokémon's official sprite, its name, its Pokédex number, and its type(s) as badges.

3.  **AC-03 (Responsive grid layout):**
    -   **GIVEN** I am on the main page
    -   **WHEN** The page loads Pokémon
    -   **THEN** The cards are arranged in a responsive grid that displays 3 columns on wide screens and adjusts to fewer columns on narrower screens.

4.  **AC-04 (Pokémon order):**
    -   **GIVEN** I am on the main page without filters
    -   **WHEN** The page loads Pokémon
    -   **THEN** The Pokémon on the Card-Views are shown in ascending order of their Pokédex number.

5.  **AC-05 (Loading state):**
    -   **GIVEN** I perform an action that reloads the grid (e.g., changing page or filter)
    -   **WHEN** The application is waiting for data from the server
    -   **THEN** The grid is temporarily replaced by a skeleton loader that mimics the card layout.

6.  **AC-06 (Card hover effect):**
    -   **GIVEN** The Pokémon grid is displayed
    -   **WHEN** I move the mouse cursor over a Pokémon card
    -   **THEN** The card tilts with a 3D perspective effect, following the cursor's movement.

#### ❌ Out of Scope
*   Displaying shiny versions of sprites.
*   Clicking on a card to see more details (feature for a future version).

#### 🔧 Tech Notes
*   Pokemon cards are generated dynamically in `app.js` using a `<template>` from `index.html`.
*   The layout is managed by CSS Grid in `main.css`.
*   The default data stream comes from the `/api/pokemons/stream` endpoint.


### **🎯 Feature 1.02:** *Pagination*

**User story:** As a User, I want to navigate through pages of Pokémon, so that I can see them in batches to avoid loading all the Pokémon at once.

#### ✅ Acceptance Criteria (AC)
1.  **AC-01 (Pagination controls):**
    -   **GIVEN** I am on the main page
    -   **WHEN** The page loads
    -   **THEN** I can see a "Next" button, a "Previous" button, and a page indicator (e.g., "Page 1 of X").

2.  **AC-02 (Next page):**
    -   **GIVEN** I am not on the last page
    -   **WHEN** I click the "Next" button
    -   **THEN** The grid updates to show the next set of Pokémon.
    -   **AND** The page indicator updates to the new page number.

3.  **AC-03 (Previous page):**
    -   **GIVEN** I am not on the first page
    -   **WHEN** I click the "Previous" button
    -   **THEN** The grid updates to show the previous set of Pokémon.
    -   **AND** The page indicator updates to the new page number.

4.  **AC-04 (Disabled states):**
    -   **GIVEN** I am on the first page
    -   **WHEN** The page loads
    -   **THEN** The "Previous" button is disabled.
    -   **AND** **GIVEN** I am on the last page, **THEN** the "Next" button is disabled.

#### ❌ Out of Scope
*   Input field to jump to a specific page number.
*   Infinite scrolling.

#### 🔧 Tech Notes
*   The frontend sends `page` and `limit` query parameters to the `/api/pokemons/stream` endpoint.
*   The backend includes pagination metadata (`total_pages`, `current_page`) in the SSE stream.
*   `app.js` updates the button states and page indicator based on this metadata.


### **🎯 Feature 1.03:** *Type filter*

**User story:** As a User, I want buttons with the Pokémon types, so that I can see the Pokémon by selecting one or two types.

#### ✅ Acceptance Criteria (AC)
1.  **AC-01 (Display filters):**
    -   **GIVEN** I am on the main page
    -   **WHEN** The page loads
    -   **THEN** I can see a "See All" button and a button for each Pokémon type.
    -   **AND** The "See All" button is active by default.

2.  **AC-02 (Filter by one type):**
    -   **GIVEN** No type filter is active
    -   **WHEN** I click on a type button (e.g., "Fire")
    -   **THEN** The grid updates to show only Pokémon that include the "Fire" type.
    -   **AND** The "Fire" button becomes active, and "See All" becomes inactive.

3.  **AC-03 (Filter by two types):**
    -   **GIVEN** One type filter is active (e.g., "Fire")
    -   **WHEN** I click on a second type button (e.g., "Flying")
    -   **THEN** The grid updates to show only Pokémon that have both "Fire" AND "Flying" types.
    -   **AND** Both the "Fire" and "Flying" buttons are active.

4.  **AC-04 (Filter limit):**
    -   **GIVEN** Two type filters are active
    -   **WHEN** I click on a third type button
    -   **THEN** The grid does not change and a visual indicator (shake animation) occurs.

5.  **AC-05 (Deselect filter):**
    -   **GIVEN** A type filter is active
    -   **WHEN** I click the same active type button again
    -   **THEN** The filter is removed.

6.  **AC-06 (No results found):**
    -   **GIVEN** I apply a filter combination
    -   **WHEN** There are no Pokémon that match the criteria
    -   **THEN** I see a message indicating "No Pokémon match the selected filters" along with the Snorlax image.

#### ❌ Out of Scope
*   Filtering by more than two types.
*   Logic for OR filtering (e.g., show Pokémon that are "Fire" OR "Water").

#### 🔧 Tech Notes
*   Type buttons are dynamically generated by fetching data from the `/api/types` endpoint.
*   Selected types are sent as a `types` query parameter array to `/api/pokemons/stream`.


### **🎯 Feature 1.04:** *Generation filter*

**User story:** As a User, I want a dropdown filter for the Pokémon, so that I can see the Pokémon by the selected generation.

#### ✅ Acceptance Criteria (AC)
1.  **AC-01 (Display dropdown):**
    -   **GIVEN** I am on the main page
    -   **WHEN** The page loads
    -   **THEN** I can see a dropdown menu with "All Generations" selected by default.

2.  **AC-02 (Select generation):**
    -   **GIVEN** The generation dropdown is available
    -   **WHEN** I click the dropdown and select a specific generation (e.g., "Generation I")
    -   **THEN** The grid updates to show only Pokémon from that generation.
    -   **AND** The dropdown text updates to show "Generation I".

3.  **AC-03 (Combine with type filters):**
    -   **GIVEN** A generation and a type filter are active
    -   **WHEN** I apply both filters
    -   **THEN** The grid shows only Pokémon that match both the selected generation AND the selected type(s).

4.  **AC-04 (No results found):**
    -   **GIVEN** I apply a filter combination (e.g., Generation IX and a type)
    -   **WHEN** There are no Pokémon that match the criteria
    -   **THEN** The "No results found" view (with Snorlax image) is displayed, as defined in `Feature 1.03 / AC-06`.

#### ❌ Out of Scope
*   Filtering by multiple generations at once.

#### 🔧 Tech Notes
*   The generation list is fetched from the `/api/generations` endpoint.
*   The selected generation ID is sent as a `generation` query parameter to `/api/pokemons/stream`.


### **🎯 Feature 1.05:** *Searchbar with autocomplete*

**User story:** As a User, I want to write a Pokémon name on the searchbar and get name suggestions, so that I can search and select a specific Pokémon by name.

#### ✅ Acceptance Criteria (AC)
1.  **AC-01 (Autocomplete suggestions):**
    -   **GIVEN** I am on the main page
    -   **WHEN** I type at least 2 characters into the search bar
    -   **THEN** A list of Pokémon names that contain the typed text appears below the search bar.

2.  **AC-02 (Select suggestion):**
    -   **GIVEN** The autocomplete suggestion list is visible
    -   **WHEN** I click on a suggested Pokémon name
    -   **THEN** The grid updates to show only the selected Pokémon.
    -   **AND** The search bar is filled with the full name of the Pokémon.

3.  **AC-03 (Disabled controls):**
    -   **GIVEN** I have successfully searched for a Pokémon
    -   **WHEN** The grid displays the single Pokémon result
    -   **THEN** The pagination controls and all filters (type and generation) are disabled.

4.  **AC-04 (Clear search):**
    -   **GIVEN** I have searched for a Pokémon
    -   **WHEN** I clear the text in the search bar
    -   **THEN** The grid returns to the previous state (e.g., the last used filter and page).
    -   **AND** The pagination and filter controls are re-enabled.

5.  **AC-05 (No results found):**
    -   **GIVEN** I search for a term
    -   **WHEN** No Pokémon match the search term
    -   **THEN** I see a message indicating "No Pokémon found with that name" along with the Snorlax image.

#### ❌ Out of Scope
*   Searching by Pokémon number or other attributes.
*   Fuzzy search or "did you mean" functionality for typos.

#### 🔧 Tech Notes
*   Autocomplete suggestions are fetched from `/api/pokemons/names_autocomplete`.
*   A `pokemon_id` is sent to the `/api/pokemons/stream` endpoint for the final search.
*   A state variable `isSearchingByName` is used in `app.js` to manage the UI state.


### **🎯 Feature 1.06:** *Surprise me button*

**User story:** As a User, I want to click a button to see random Pokémon, so that I can see them without a specific order.

#### ✅ Acceptance Criteria (AC)
1.  **AC-01 (Random button):**
    -   **GIVEN** I am on the main page
    -   **WHEN** I click the "Random Explore" button
    -   **THEN** The grid updates to show a small, fixed number (3) of randomly selected Pokémon.

2.  **AC-02 (Disabled controls):**
    -   **GIVEN** The grid is showing random Pokémon
    -   **WHEN** I view the results
    -   **THEN** The pagination controls and all filters (type and generation) are disabled.

#### ❌ Out of Scope
*   Allowing the user to choose the number of random Pokémon.

#### 🔧 Tech Notes
*   The frontend (`app.js`) generates an array of 3 random Pokémon IDs.
*   These IDs are sent as a `pokemon_ids` query parameter to the `/api/pokemons/stream` endpoint.
