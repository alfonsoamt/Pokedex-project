# 🧪 E2E Test Cases

## 🖼️ Suite: Grid Visualization (GRD)

<details>
<summary>🔴 <strong>TC-E-GRD-001: Verify card content (sprite, name, number, types)</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.01: Pokémon Grid visualization` |
| **Acceptance Criteria** | `AC-02 (Card-View content)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure that all essential Pokémon data (visuals, identification, and typing) is correctly displayed to the user, which is the core function of the application.

**Preconditions:**
1.  The user has navigated to the main page of the application.

**Test Steps:**
```gherkin
Scenario: Card content verification
  Given the user is on the main page
  When the Pokémon cards are loaded
  Then each card should display the Pokémon's sprite
  And each card should display the Pokémon's name
  And each card should display the Pokémon's Pokédex number
  And each card should display the Pokémon's type(s) as badges
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GRD-002: Verify default ascending order by Pokédex number</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.01: Pokémon Grid visualization` |
| **Acceptance Criteria** | `AC-04 (Pokémon order)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the default presentation of Pokémon follows the standard, expected numerical order, ensuring a consistent and predictable user experience.

**Preconditions:**
1.  The user is on the main page.
2.  No filters have been applied.

**Test Steps:**
```gherkin
Scenario: Default sorting order
  Given the user is on the main page without any filters applied
  When the Pokémon cards are loaded
  Then the Pokémon should be listed in ascending order of their Pokédex number
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GRD-003: Verify responsive grid layout on different screen sizes</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.01: Pokémon Grid visualization` |
| **Acceptance Criteria** | `AC-03 (Responsive grid layout)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To ensure the application provides an optimal and usable viewing experience across common device viewports (desktop, tablet, mobile).

**Preconditions:**
1.  The user is on the main page with Pokémon cards loaded.

**Test Steps:**
```gherkin
Scenario Outline: Responsive grid layout
  Given the user is on the main page
  When the viewport is set to <width> pixels wide
  Then the Pokémon grid should display <columns> columns per row

  Examples:
    | width | columns |
    | 1920  | 3       |
    | 768   | 2       |
    | 375   | 1       |
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-GRD-004: Verify card hover effect is present</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.01: Pokémon Grid visualization` |
| **Acceptance Criteria** | `AC-06 (Card hover effect)` |
| **Priority** | 🟡 `Medium` |
| **Type** | `UI-Visual` |

**Objective:**
> To verify that visual feedback is provided upon user interaction, enhancing the application's aesthetic and interactive feel.

**Preconditions:**
1.  The user is on the main page with Pokémon cards loaded.

**Test Steps:**
```gherkin
Scenario: Card hover effect
  Given the user is on the main page with Pokémon cards loaded
  When the user hovers the mouse cursor over a Pokémon card
  Then the card should tilt to create a 3D perspective effect
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GRD-005: Verify skeleton loader is displayed during data fetch</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.01: Pokémon Grid visualization` |
| **Acceptance Criteria** | `AC-05 (Loading state)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To ensure the application provides clear visual feedback that it is busy fetching data, preventing user confusion and improving the perceived performance.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Skeleton loader visibility
  Given the user is on the main page
  When an action is performed that triggers a data reload
  Then a skeleton loader should be displayed while the data is being fetched
  And the skeleton loader should be replaced by the new Pokémon grid once the data is loaded
```
---
</details>

---

## 📄 Suite: Pagination (PAG)

<details>
<summary>🔴 <strong>TC-E-PAG-001: Verify clicking "Next" loads the subsequent set of Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.02: Pagination` |
| **Acceptance Criteria** | `AC-02 (Next page)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can navigate forward through the entire dataset, which is a primary navigation feature.

**Preconditions:**
1.  The user is on the main page.
2.  The current page is not the last page.

**Test Steps:**
```gherkin
Scenario: Navigate to the next page
  Given the user is on the main page and not on the last page
  When the user clicks the "Next" button
  Then the Pokémon grid updates to show the next set of results
  And the page indicator updates to the new page number
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-PAG-002: Verify clicking "Previous" loads the previous set of Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.02: Pagination` |
| **Acceptance Criteria** | `AC-03 (Previous page)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can navigate backward through the dataset after moving forward.

**Preconditions:**
1.  The user has navigated to a page greater than 1.

**Test Steps:**
```gherkin
Scenario: Navigate to the previous page
  Given the user is on page "2" of the Pokémon list
  When the user clicks the "Previous" button
  Then the Pokémon grid updates to show the results for page "1"
  And the page indicator updates to "1"
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-PAG-003: Verify "Previous" button is disabled on the first page</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.02: Pagination` |
| **Acceptance Criteria** | `AC-04 (Disabled states)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent the user from performing an invalid action and to provide clear visual cues about the navigation state.

**Preconditions:**
1.  The user is on the first page of the application.

**Test Steps:**
```gherkin
Scenario: Previous button state on first page
  Given the user is on the first page of the Pokémon list
  Then the "Previous" button should be visible but in a disabled state
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-PAG-004: Verify "Next" button is disabled on the last page</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.02: Pagination` |
| **Acceptance Criteria** | `AC-04 (Disabled states)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent the user from attempting to navigate past the end of the dataset and provide clear visual cues.

**Preconditions:**
1.  The user has navigated to the final page of the Pokémon list.

**Test Steps:**
```gherkin
Scenario: Next button state on last page
  Given the user is on the last page of the Pokémon list
  Then the "Next" button should be visible but in a disabled state
```
---
</details>

---

## 🎨 Suite: Type Filter (TYP)

<details>
<summary>🔴 <strong>TC-E-TYP-001: Verify filtering by a single type</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-02 (Filter by one type)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the type filter, ensuring users can narrow down the Pokémon list by a single criterion.

**Preconditions:**
1.  The user is on the main page with the default Pokémon list loaded.

**Test Steps:**
```gherkin
Scenario: Filter by a single type
  Given the user is on the main page
  When the user clicks the "Fire" type button
  Then the grid should only display Pokémon that include the "Fire" type
  And the "Fire" button should appear as active
  And the "See All" button should appear as inactive
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-TYP-002: Verify filtering by two types (AND logic)</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-03 (Filter by two types)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify that the filter can handle complex AND-logic, allowing users to perform more specific searches by combining two criteria.

**Preconditions:**
1.  The user has already applied a single type filter (e.g., "Fire").

**Test Steps:**
```gherkin
Scenario: Filter by two types with AND logic
  Given the user has an active filter for the "Fire" type
  When the user clicks the "Flying" type button
  Then the grid should only display Pokémon that have both "Fire" AND "Flying" types
  And both the "Fire" and "Flying" buttons should appear as active
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-003: Verify deselecting an active filter</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-05 (Deselect filter)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can easily undo a filter selection and return to a broader view.

**Preconditions:**
1.  The user has one or more active type filters.

**Test Steps:**
```gherkin
Scenario: Deselect an active filter
  Given the user has an active filter for the "Fire" type
  When the user clicks the "Fire" type button again
  Then the "Fire" type filter should be removed
  And the grid should return to the default "See All" state
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-TYP-004: Verify filter limit by attempting to select a third type</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-04 (Filter limit)` |
| **Priority** | 🟡 `Medium` |
| **Type** | `Functional` |

**Objective:**
> To verify the business rule that limits filtering to a maximum of two types, preventing user error and managing system complexity.

**Preconditions:**
1.  The user has two active type filters (e.g., "Fire" and "Flying").

**Test Steps:**
```gherkin
Scenario: Attempt to select a third type filter
  Given the user has active filters for "Fire" and "Flying"
  When the user clicks the "Water" type button
  Then the grid of Pokémon should not change
  And a visual shake animation should occur on the filter buttons to indicate an invalid action
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-005: Verify "See All" button removes all active type filters</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-01 (Display filters)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure the primary reset mechanism for the type filters works correctly, providing a clear and easy way for users to start over.

**Preconditions:**
1.  The user has one or more active type filters.

**Test Steps:**
```gherkin
Scenario: Reset filters using "See All"
  Given the user has an active filter for "Water"
  When the user clicks the "See All" button
  Then all type filters should be deactivated
  And the "See All" button should become active
  And the grid should display all Pokémon from the current page
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-006: Verify "No results found" message for non-matching type combinations</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.03: Type filter` |
| **Acceptance Criteria** | `AC-06 (No results found)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the application provides clear feedback to the user when their filter combination results in an empty dataset.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Type 1:** `Ice`
*   **Type 2:** `Fire` (A combination known to have no results)

**Test Steps:**
```gherkin
Scenario: No results found view
  Given the user is on the main page
  When the user applies filters for "Ice" and "Fire" types
  Then the grid should be empty
  And a message indicating "No Pokémon match the selected filters" should be displayed
  And an image of Snorlax should be visible
```
---
</details>

---

##  generational_dinosaurs Suite: Generation Filter (GEN)

<details>
<summary>🔴 <strong>TC-E-GEN-001: Verify filtering by a single generation</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.04: Generation filter` |
| **Acceptance Criteria** | `AC-02 (Select generation)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the generation filter, ensuring users can scope the dataset to a specific Pokémon generation.

**Preconditions:**
1.  The user is on the main page with the default Pokémon list loaded.

**Test Steps:**
```gherkin
Scenario: Filter by a single generation
  Given the user is on the main page
  When the user selects "Generation I" from the generation dropdown
  Then the grid should only display Pokémon that belong to Generation I (numbers 1-151)
  And the dropdown text should show "Generation I" as the selected value
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GEN-002: Verify combining a generation filter with a type filter</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.04: Generation filter` |
| **Acceptance Criteria** | `AC-03 (Combine with type filters)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure that the generation and type filters interoperate correctly, allowing for highly specific filtering combinations.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Combine generation and type filters
  Given the user is on the main page
  When the user selects "Generation I" from the generation dropdown
  And the user clicks the "Water" type button
  Then the grid should only display Pokémon that are from "Generation I" AND are of the "Water" type
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GEN-003: Verify "No results found" message for non-matching combinations</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.04: Generation filter` |
| **Acceptance Criteria** | `AC-04 (No results found)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the application provides clear feedback when a combined filter yields no results.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Generation:** `Generation IX`
*   **Type:** `Poison` (A combination known to have few or no results, for testing purposes)

**Test Steps:**
```gherkin
Scenario: No results view for combined filters
  Given the user is on the main page
  When the user selects "Generation IX" from the generation dropdown
  And the user applies a filter for the "Poison" type
  Then the grid should be empty
  And a message indicating "No Pokémon match the selected filters" should be displayed
```
---
</details>

---

## 🔍 Suite: Searchbar (SRC)

<details>
<summary>🔴 <strong>TC-E-SRC-001: Verify autocomplete suggestions appear after typing >= 2 characters</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.05: Searchbar with autocomplete` |
| **Acceptance Criteria** | `AC-01 (Autocomplete suggestions)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure the searchbar provides real-time assistance to the user, improving usability and search speed.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Search Term:** `pi`

**Test Steps:**
```gherkin
Scenario: Autocomplete suggestions appear
  Given the user is on the main page
  When the user types "pi" into the search bar
  Then a list of suggestions should appear below the search bar
  And the suggestion list should contain "Pikachu"
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-SRC-002: Verify clicking a suggestion filters to that single Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.05: Searchbar with autocomplete` |
| **Acceptance Criteria** | `AC-02 (Select suggestion)` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify that the user can successfully select a Pokémon from the autocomplete list to see its specific card.

**Preconditions:**
1.  The user has typed a search term (e.g., "pika") and the suggestion list is visible.

**Test Steps:**
```gherkin
Scenario: Select a suggestion
  Given the user has typed "pika" into the search bar and the suggestion list is visible
  When the user clicks on the "Pikachu" suggestion
  Then the grid should update to show only the "Pikachu" Pokémon card
  And the search bar text should be updated to "Pikachu"
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-SRC-003: Verify filters and pagination are disabled after a successful search</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.05: Searchbar with autocomplete` |
| **Acceptance Criteria** | `AC-03 (Disabled controls)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent user confusion and invalid state combinations when viewing a single, specific Pokémon.

**Preconditions:**
1.  The user has successfully searched for and is viewing a single Pokémon.

**Test Steps:**
```gherkin
Scenario: UI controls are disabled after search
  Given the user has successfully searched for "Pikachu"
  Then all type filter buttons should be disabled
  And the generation filter dropdown should be disabled
  And the pagination controls should be disabled
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-SRC-004: Verify clearing the search bar re-enables controls and restores the grid</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.05: Searchbar with autocomplete` |
| **Acceptance Criteria** | `AC-04 (Clear search)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure the user can easily exit the single-Pokémon view and return to the previous browsing state.

**Preconditions:**
1.  The user is viewing the search result for a single Pokémon.

**Test Steps:**
```gherkin
Scenario: Clear search and restore state
  Given the user is viewing the search result for a single Pokémon
  When the user clears all text from the search bar
  Then the grid should return to its previous state (e.g., the last used filter and page)
  And all filter and pagination controls should be re-enabled
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-SRC-005: Verify "No results found" message for non-matching search terms</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.05: Searchbar with autocomplete` |
| **Acceptance Criteria** | `AC-05 (No results found)` |
| **Priority** | 🟡 `Medium` |
| **Type** | `Functional` |

**Objective:**
> To provide clear feedback when a user's search term does not match any Pokémon.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Search Term:** `NonExistentPokemon`

**Test Steps:**
```gherkin
Scenario: No results for a search term
  Given the user is on the main page
  When the user types "NonExistentPokemon" into the search bar
  Then the grid should be empty
  And a message indicating "No Pokémon found with that name" should be displayed
```
---
</details>

---

## ✨ Suite: Surprise Me (RND)

<details>
<summary>🟠 <strong>TC-E-RND-001: Verify clicking the button displays 3 random Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.06: Surprise me button` |
| **Acceptance Criteria** | `AC-01 (Random button)` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the "Surprise Me" feature, ensuring it provides a random selection of Pokémon for exploration.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Get a random selection of Pokémon
  Given the user is on the main page
  When the user clicks the "Random Explore" button
  Then the grid should update to show exactly 3 Pokémon cards
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-RND-002: Verify filters and pagination are disabled after a random search</strong></summary>

| | |
| :--- | :--- |
| **Requirement** | `F-1.06: Surprise me button` |
| **Acceptance Criteria** | `AC-02 (Disabled controls)` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent user confusion and invalid state combinations when viewing the special "Surprise Me" results.

**Preconditions:**
1.  The user is viewing the result of a "Random Explore" action.

**Test Steps:**
```gherkin
Scenario: UI controls are disabled after random search
  Given the user is viewing the result of a "Random Explore" action
  Then all type filter buttons should be disabled
  And the generation filter dropdown should be disabled
  And the pagination controls should be disabled
```
---
</details>

</details>

<details>
<summary>🟠 <strong>TC-E-GRD-002: Verify default ascending order by Pokédex number</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.01: Pokemon Grid visualization` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the default presentation of Pokémon follows the standard, expected numerical order, ensuring a consistent and predictable user experience.

**Preconditions:**
1.  The user is on the main page.
2.  No filters have been applied.

**Test Steps:**
```gherkin
Scenario: Default sorting order
  Given the user is on the main page without any filters applied
  When the Pokémon cards are loaded
  Then the Pokémon should be listed in ascending order of their Pokédex number
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GRD-003: Verify responsive grid layout on different screen sizes</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.01: Pokemon Grid visualization` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To ensure the application provides an optimal and usable viewing experience across common device viewports (desktop, tablet, mobile).

**Preconditions:**
1.  The user is on the main page with Pokémon cards loaded.

**Test Steps:**
```gherkin
Scenario Outline: Responsive grid layout
  Given the user is on the main page
  When the viewport is set to <width> pixels wide
  Then the Pokémon grid should display <columns> columns per row

  Examples:
    | width | columns |
    | 1920  | 3       |
    | 768   | 2       |
    | 375   | 1       |
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-GRD-004: Verify card hover effect is present</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.01: Pokemon Grid visualization` |
| **Priority** | 🟡 `Medium` |
| **Type** | `UI-Visual` |

**Objective:**
> To verify that visual feedback is provided upon user interaction, enhancing the application's aesthetic and interactive feel.

**Preconditions:**
1.  The user is on the main page with Pokémon cards loaded.

**Test Steps:**
```gherkin
Scenario: Card hover effect
  Given the user is on the main page with Pokémon cards loaded
  When the user hovers the mouse cursor over a Pokémon card
  Then the card should tilt to create a 3D perspective effect
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GRD-005: Verify skeleton loader is displayed during data fetch</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.01: Pokemon Grid visualization` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To ensure the application provides clear visual feedback that it is busy fetching data, preventing user confusion and improving the perceived performance.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Skeleton loader visibility
  Given the user is on the main page
  When an action is performed that triggers a data reload
  Then a skeleton loader should be displayed while the data is being fetched
  And the skeleton loader should be replaced by the new Pokémon grid once the data is loaded
```
---
</details>

---

## 📄 Suite: Pagination (PAG)

<details>
<summary>🔴 <strong>TC-E-PAG-001: Verify clicking "Next" loads the subsequent set of Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.02: Pagination` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can navigate forward through the entire dataset, which is a primary navigation feature.

**Preconditions:**
1.  The user is on the main page.
2.  The current page is not the last page.

**Test Steps:**
```gherkin
Scenario: Navigate to the next page
  Given the user is on the main page and not on the last page
  When the user clicks the "Next" button
  Then the Pokémon grid updates to show the next set of results
  And the page indicator updates to the new page number
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-PAG-002: Verify clicking "Previous" loads the previous set of Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.02: Pagination` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can navigate backward through the dataset after moving forward.

**Preconditions:**
1.  The user has navigated to a page greater than 1.

**Test Steps:**
```gherkin
Scenario: Navigate to the previous page
  Given the user is on page "2" of the Pokémon list
  When the user clicks the "Previous" button
  Then the Pokémon grid updates to show the results for page "1"
  And the page indicator updates to "1"
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-PAG-003: Verify "Previous" button is disabled on the first page</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.02: Pagination` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent the user from performing an invalid action and to provide clear visual cues about the navigation state.

**Preconditions:**
1.  The user is on the first page of the application.

**Test Steps:**
```gherkin
Scenario: Previous button state on first page
  Given the user is on the first page of the Pokémon list
  Then the "Previous" button should be visible but in a disabled state
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-PAG-004: Verify "Next" button is disabled on the last page</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.02: Pagination` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent the user from attempting to navigate past the end of the dataset and provide clear visual cues.

**Preconditions:**
1.  The user has navigated to the final page of the Pokémon list.

**Test Steps:**
```gherkin
Scenario: Next button state on last page
  Given the user is on the last page of the Pokémon list
  Then the "Next" button should be visible but in a disabled state
```
---
</details>

---

## 🎨 Suite: Type Filter (TYP)

<details>
<summary>🔴 <strong>TC-E-TYP-001: Verify filtering by a single type</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the type filter, ensuring users can narrow down the Pokémon list by a single criterion.

**Preconditions:**
1.  The user is on the main page with the default Pokémon list loaded.

**Test Steps:**
```gherkin
Scenario: Filter by a single type
  Given the user is on the main page
  When the user clicks the "Fire" type button
  Then the grid should only display Pokémon that include the "Fire" type
  And the "Fire" button should appear as active
  And the "See All" button should appear as inactive
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-TYP-002: Verify filtering by two types (AND logic)</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify that the filter can handle complex AND-logic, allowing users to perform more specific searches by combining two criteria.

**Preconditions:**
1.  The user has already applied a single type filter (e.g., "Fire").

**Test Steps:**
```gherkin
Scenario: Filter by two types with AND logic
  Given the user has an active filter for the "Fire" type
  When the user clicks the "Flying" type button
  Then the grid should only display Pokémon that have both "Fire" AND "Flying" types
  And both the "Fire" and "Flying" buttons should appear as active
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-003: Verify deselecting an active filter</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure users can easily undo a filter selection and return to a broader view.

**Preconditions:**
1.  The user has one or more active type filters.

**Test Steps:**
```gherkin
Scenario: Deselect an active filter
  Given the user has an active filter for the "Fire" type
  When the user clicks the "Fire" type button again
  Then the "Fire" type filter should be removed
  And the grid should return to the default "See All" state
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-TYP-004: Verify filter limit by attempting to select a third type</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🟡 `Medium` |
| **Type** | `Functional` |

**Objective:**
> To verify the business rule that limits filtering to a maximum of two types, preventing user error and managing system complexity.

**Preconditions:**
1.  The user has two active type filters (e.g., "Fire" and "Flying").

**Test Steps:**
```gherkin
Scenario: Attempt to select a third type filter
  Given the user has active filters for "Fire" and "Flying"
  When the user clicks the "Water" type button
  Then the grid of Pokémon should not change
  And a visual shake animation should occur on the filter buttons to indicate an invalid action
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-005: Verify "See All" button removes all active type filters</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure the primary reset mechanism for the type filters works correctly, providing a clear and easy way for users to start over.

**Preconditions:**
1.  The user has one or more active type filters.

**Test Steps:**
```gherkin
Scenario: Reset filters using "See All"
  Given the user has an active filter for "Water"
  When the user clicks the "See All" button
  Then all type filters should be deactivated
  And the "See All" button should become active
  And the grid should display all Pokémon from the current page
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-TYP-006: Verify "No results found" message for non-matching type combinations</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.03: Type filter` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the application provides clear feedback to the user when their filter combination results in an empty dataset.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Type 1:** `Ice`
*   **Type 2:** `Fire` (A combination known to have no results)

**Test Steps:**
```gherkin
Scenario: No results found view
  Given the user is on the main page
  When the user applies filters for "Ice" and "Fire" types
  Then the grid should be empty
  And a message indicating "No Pokémon match the selected filters" should be displayed
  And an image of Snorlax should be visible
```
---
</details>

---

##  🧬 Suite: Generation Filter (GEN)

<details>
<summary>🔴 <strong>TC-E-GEN-001: Verify filtering by a single generation</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.04: Generation filter` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the generation filter, ensuring users can scope the dataset to a specific Pokémon generation.

**Preconditions:**
1.  The user is on the main page with the default Pokémon list loaded.

**Test Steps:**
```gherkin
Scenario: Filter by a single generation
  Given the user is on the main page
  When the user selects "Generation I" from the generation dropdown
  Then the grid should only display Pokémon that belong to Generation I (numbers 1-151)
  And the dropdown text should show "Generation I" as the selected value
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GEN-002: Verify combining a generation filter with a type filter</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.04: Generation filter` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure that the generation and type filters interoperate correctly, allowing for highly specific filtering combinations.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Combine generation and type filters
  Given the user is on the main page
  When the user selects "Generation I" from the generation dropdown
  And the user clicks the "Water" type button
  Then the grid should only display Pokémon that are from "Generation I" AND are of the "Water" type
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-GEN-003: Verify "No results found" message for non-matching combinations</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.04: Generation filter` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify that the application provides clear feedback when a combined filter yields no results.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Generation:** `Generation IX`
*   **Type:** `Poison` (A combination known to have few or no results, for testing purposes)

**Test Steps:**
```gherkin
Scenario: No results view for combined filters
  Given the user is on the main page
  When the user selects "Generation IX" from the generation dropdown
  And the user applies a filter for the "Poison" type
  Then the grid should be empty
  And a message indicating "No Pokémon match the selected filters" should be displayed
```
---
</details>

---

## 🔍 Suite: Searchbar (SRC)

<details>
<summary>🔴 <strong>TC-E-SRC-001: Verify autocomplete suggestions appear after typing >= 2 characters</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.05: Searchbar with autocomplete` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To ensure the searchbar provides real-time assistance to the user, improving usability and search speed.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Search Term:** `pi`

**Test Steps:**
```gherkin
Scenario: Autocomplete suggestions appear
  Given the user is on the main page
  When the user types "pi" into the search bar
  Then a list of suggestions should appear below the search bar
  And the suggestion list should contain "Pikachu"
```
---
</details>

<details>
<summary>🔴 <strong>TC-E-SRC-002: Verify clicking a suggestion filters to that single Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.05: Searchbar with autocomplete` |
| **Priority** | 🔴 `Critical` |
| **Type** | `Functional` |

**Objective:**
> To verify that the user can successfully select a Pokémon from the autocomplete list to see its specific card.

**Preconditions:**
1.  The user has typed a search term (e.g., "pika") and the suggestion list is visible.

**Test Steps:**
```gherkin
Scenario: Select a suggestion
  Given the user has typed "pika" into the search bar and the suggestion list is visible
  When the user clicks on the "Pikachu" suggestion
  Then the grid should update to show only the "Pikachu" Pokémon card
  And the search bar text should be updated to "Pikachu"
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-SRC-003: Verify filters and pagination are disabled after a successful search</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.05: Searchbar with autocomplete` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent user confusion and invalid state combinations when viewing a single, specific Pokémon.

**Preconditions:**
1.  The user has successfully searched for and is viewing a single Pokémon.

**Test Steps:**
```gherkin
Scenario: UI controls are disabled after search
  Given the user has successfully searched for "Pikachu"
  Then all type filter buttons should be disabled
  And the generation filter dropdown should be disabled
  And the pagination controls should be disabled
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-SRC-004: Verify clearing the search bar re-enables controls and restores the grid</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.05: Searchbar with autocomplete` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To ensure the user can easily exit the single-Pokémon view and return to the previous browsing state.

**Preconditions:**
1.  The user is viewing the search result for a single Pokémon.

**Test Steps:**
```gherkin
Scenario: Clear search and restore state
  Given the user is viewing the search result for a single Pokémon
  When the user clears all text from the search bar
  Then the grid should return to its previous state (e.g., the last used filter and page)
  And all filter and pagination controls should be re-enabled
```
---
</details>

<details>
<summary>🟡 <strong>TC-E-SRC-005: Verify "No results found" message for non-matching search terms</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.05: Searchbar with autocomplete` |
| **Priority** | 🟡 `Medium` |
| **Type** | `Functional` |

**Objective:**
> To provide clear feedback when a user's search term does not match any Pokémon.

**Preconditions:**
1.  The user is on the main page.

**Test Data:**
*   **Search Term:** `NonExistentPokemon`

**Test Steps:**
```gherkin
Scenario: No results for a search term
  Given the user is on the main page
  When the user types "NonExistentPokemon" into the search bar
  Then the grid should be empty
  And a message indicating "No Pokémon found with that name" should be displayed
```
---
</details>

---

## ✨ Suite: Surprise Me (RND)

<details>
<summary>🟠 <strong>TC-E-RND-001: Verify clicking the button displays 3 random Pokémon</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.06: Surprise me button` |
| **Priority** | 🟠 `High` |
| **Type** | `Functional` |

**Objective:**
> To verify the core functionality of the "Surprise Me" feature, ensuring it provides a random selection of Pokémon for exploration.

**Preconditions:**
1.  The user is on the main page.

**Test Steps:**
```gherkin
Scenario: Get a random selection of Pokémon
  Given the user is on the main page
  When the user clicks the "Random Explore" button
  Then the grid should update to show exactly 3 Pokémon cards
```
---
</details>

<details>
<summary>🟠 <strong>TC-E-RND-002: Verify filters and pagination are disabled after a random search</strong></summary>

| | |
| :--- | :--- |
| **Feature Link** | `F-1.06: Surprise me button` |
| **Priority** | 🟠 `High` |
| **Type** | `UI-Visual` |

**Objective:**
> To prevent user confusion and invalid state combinations when viewing the special "Surprise Me" results.

**Preconditions:**
1.  The user is viewing the result of a "Random Explore" action.

**Test Steps:**
```gherkin
Scenario: UI controls are disabled after random search
  Given the user is viewing the result of a "Random Explore" action
  Then all type filter buttons should be disabled
  And the generation filter dropdown should be disabled
  And the pagination controls should be disabled
```
---
</details>

