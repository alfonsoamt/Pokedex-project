# 🔍 Test Strategy - Pokedex Project

> This document outlines the comprehensive testing strategy for the Pokedex Project v1.0. Its purpose is to define the quality objectives, scope, testing approach, and required resources to ensure the application is delivered with the highest possible quality. It serves as a guiding document for all testing activities.



## 1.- 🎯 Quality Objectives
- **Functionality:** Achieve *compliance* with 100% of the Acceptance Criteria defined in [FEATURES.md](./FEATURES.md) for the v1.0 release.
- **Performance:**
           * The application must achieve a Google Lighthouse performance score of 85 or higher.
           * The P95 response time for all API endpoints must be under 800ms.
- **Usability:** Ensure all main user flows are completed without critical errors or blockers during exploratory and E2E testing.
- **Compatibility:** *Maintain* full functional and visual consistency across all browsers and platforms defined in the "Supported Platforms" section.

## 2.- 🔭 Testing Scope
- **In Scope:** 
    * All features defined in [FEATURES.md](./FEATURES.md) for the v1.0 release, covering both backend (API) and frontend (UI) implementation.
- **Out of the Scope:**
    * Testing of the external PokeAPI itself is not covered. However, testing our backend's error handling and contract adherence with the PokeAPI is in scope.
    * Non-functional testing with high user loads (stress/load testing) is excluded due to this being a small-scale application and the lack of a specialized environment for such tests.
    * Any feature or workflow not defined in [FEATURES.md](./FEATURES.m) for the V1.0 release is out of scope.
    
## 3.- 🧪 Test Approach
- **Unit Testing (Owner: Development):** To ensure code-level quality and logic, with a target of >80% code coverage on business logic modules.
- **Integration Testing (API) (Owner: QA):** To verify the API contract, including request/response schemas, status codes, and error handling for all endpoints.
- **End-to-End (E2E) Testing (Owner: QA):** To validate complete user workflows through the UI. These automated tests will cover the main "happy paths" for all major features (search, filtering, pagination).
- **Baseline Performance Testing (Owner: QA):** To measure application efficiency against the defined Quality Objectives using tools like Lighthouse and API response time monitoring.
- **Manual Exploratory Testing (Owner: QA):** To be conducted before a release candidate is approved. Focus will be on usability, visual consistency between platforms, and discovering edge cases not covered by automation.

## 4.- 💻 Supported Platforms

This section defines the target platforms and browsers where the Pokedex application is expected to be fully functional and visually consistent. The matrix is based on general market share and project resource availability.

### Support Matrix

| Platform | Operating System | Browser | Support Tier |
| :--- | :--- | :--- | :--- |
| **Desktop**| Windows 10 / 11 | Chrome (Latest) | Tier 1 (Primary) |
| | | Edge (Latest) | Tier 1 (Primary) |
| | | Firefox (Latest) | Tier 2 (Secondary) |
| **Mobile** | Android | Chrome (Latest) | Tier 1 (Primary) |
| | iOS | Safari (Latest) | Tier 3 (Best-Effort) |

### Support Notes:
- **Versioning:** Support is guaranteed for the **latest stable version** of the listed browsers. Beta, developer, or legacy versions are not officially supported.
- **Screen Resolution:**
    - **Desktop:** Testing will primarily focus on a **1920x1080** resolution.
    - **Mobile:** Testing will be conducted on devices and emulators with a viewport width between **360px** and **420px**.
- **Tier Definitions:**
    - **Tier 1 (Primary):** Platforms receive the full suite of automated regression testing and in-depth exploratory testing. Critical bugs must be fixed before a release.
    - **Tier 2 (Secondary):** Platforms are validated with smoke tests and focused exploratory testing for major functionalities.
    - **Tier 3 (Best-Effort):** Platforms are not part of the regular regression cycle. Validation is performed on a best-effort basis, for example, through a one-time check on a cloud testing platform before a major release.

## 5.- 🔨 Tools

This section outlines the specific tools and libraries selected to implement the test strategy across different testing levels.

| Category | Tool / Library | Purpose |
| :--- | :--- | :--- |
| **Test Case Management** | **GitHub (Markdown Files)** | For lightweight creation, versioning, and tracking of manual test cases directly within the repository. |
| **Unit Testing** | **Pytest** | To test individual functions and logic units within the Python backend. |
| **API/Integration Testing**| **Pytest** + **Requests** | To execute automated checks against the FastAPI endpoints, verifying contracts, status codes, and responses. |
| | **Pydantic** | For robust validation of API response schemas (data types, structure, and required fields) within Pytest. |
| **E2E Testing** | **Playwright (with Python)** | For end-to-end automation of user flows through the web interface, simulating real user interactions. |
| **Performance Testing** | **Google Lighthouse** | To measure and audit frontend performance metrics (load speed, interactivity) against the defined quality objectives. |
| | **`k6` or `Locust`** | *(Future consideration)* For potential load and stress testing of the API endpoints. |
| **Compatibility Testing** | **BrowserStack** (or similar) | To perform validation on platforms not physically available, such as Safari on iOS. |
| **CI/CD** | **GitHub Actions** | To automate the execution of test suites (API, E2E) upon code changes (e.g., on pull requests). |
| **Code Quality** | **Ruff / Black** | To enforce consistent code style and quality standards within the Python codebase (including test code). |

## 6.- 📢 Risk Management

This section outlines potential quality risks and the strategies to mitigate them.

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| RISK-01 | Visual or functional bugs may exist on iOS/Safari due to the lack of physical devices for regular testing. | Medium | Medium | - Perform a one-time validation pass on a cloud-based testing platform (e.g., BrowserStack) before the v1.0 release.<br>- Officially classify iOS/Safari as "Best-Effort" support (Tier 3) to manage user expectations. |
| RISK-02 | A browser update (e.g., Chrome, Firefox) could introduce a breaking change that impacts application functionality or layout. | Medium | High | - Maintain a suite of E2E regression tests that can be run on demand after a major browser version is released.<br>- Monitor production for error spikes after significant browser updates are rolled out to the public. |