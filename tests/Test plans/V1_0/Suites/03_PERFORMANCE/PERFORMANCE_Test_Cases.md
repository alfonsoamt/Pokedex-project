# ⏱️ Performance (Baseline) Test Cases

## 🔬 API Test Cases

<details>
<summary><strong>TC-P-API-001: Measure P95 latency for the /api/pokemons/stream endpoint under baseline load</strong></summary>

| | |
| :--- | :--- |
| **Linked Objective** | `TEST_STRATEGY.md > Quality Objectives > "The P95 response time for all API endpoints must be under 800ms."` |
| **Test Type** | `Load Test` |
| **Tool** | `k6` |

**Test Objective:**
> To validate that the main Pokémon-fetching endpoint responds below the acceptable threshold under a normal, sustained user load.

**Endpoint(s) Under Test:**
*   `GET /api/pokemons/stream`

**Load Profile:**
*   **Virtual Users (VUs):** 25 concurrent VUs.
*   **Duration:** 5 minutes.
*   **Ramp-up:** Ramp up from 0 to 25 VUs over the first minute, then sustain the load for the remaining 4 minutes.

**Acceptance Criteria (Pass/Fail):**
*   **Pass if:**
    *   95th percentile (p95) latency is < 800ms.
    *   Error rate is < 1%.
*   **Fail if:** Any of the above criteria are not met.

---
</details>

---

## 🖥️ Frontend Test Cases

<details>
<summary><strong>TC-P-FE-001: Measure the Google Lighthouse score on the main page</strong></summary>

| | |
| :--- | :--- |
| **Linked Objective** | `TEST_STRATEGY.md > Quality Objectives > "The application must achieve a Google Lighthouse performance score of 85 or higher."` |
| **Test Type** | `Frontend Audit` |
| **Tool** | `Google Lighthouse` |

**Test Objective:**
> To ensure the initial page load and rendering meet modern web performance standards.

**Page Under Test:**
*   Home page (`index.html`)

**Load Profile:**
*   Not applicable (it's a single-user browser test). A "Fast 3G" connection is simulated to evaluate a reasonable worst-case scenario.

**Acceptance Criteria (Pass/Fail):**
*   **Pass if:** The overall "Performance" score in the Lighthouse report is ≥ 85.
*   **Fail if:** The score is < 85.

---
</details>

