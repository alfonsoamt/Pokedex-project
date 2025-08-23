# Pokedex Project: A Decoupled Full-Stack Application

An interactive Pokedex application designed to explore Pokémon information, built with a modern, decoupled architecture. This project serves as a practical and functional platform for Quality Assurance (QA) and Quality Engineering (QE) professionals to implement features and apply testing strategies.

### 🚀 Live Demo

**[Visit the live application here!](https://amt-pokedex.netlify.app/)**

### ✨ Live Preview

![Project Screenshot](Frontend/Frontend1.png)

---

### 🛠️ Tech Stack & Tools

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render"/>
  <img src="https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white" alt="Netlify"/>
</p>

---

## 🏛️ Architecture

The application is built with a decoupled full-stack architecture, ensuring a clean separation of concerns between the frontend and backend.

*   **Backend:** Developed in **Python** using the **FastAPI** framework. It handles all business logic, interacts with the external [PokeAPI](https://pokeapi.co/), and exposes data through a RESTful API. Deployed on **Render**.
*   **Frontend:** A pure client-side application built with standard web technologies: **HTML** for structure, **CSS** for styling, and **JavaScript** for interactivity and consuming the backend API. Deployed on **Netlify**.

## ✅ Features

### Implemented

-   [x] **Pokémon Grid:** Displays Pokémon in a visually appealing and responsive grid.
-   [x] **Efficient Pagination:** Handles large amounts of data by loading Pokémon in batches via a Server-Sent Events (SSE) stream.
-   [x] **Live Search:** A search bar with autocomplete functionality suggests Pokémon names as the user types.
-   [x] **Dynamic Filtering:** Allows users to filter the grid by Pokémon type and generation.
-   [x] **"Surprise Me!":** A button to display a random selection of Pokémon.

### Future Roadmap

-   [ ] **Pokémon Detail Modal:** A pop-up view with detailed stats, abilities, and evolution chains when a Pokémon is clicked.
-   [ ] **Pokémon Comparator:** A tool to compare two Pokémon side-by-side.
-   [ ] **Team Builder:** Allows users to create and manage a team of up to 6 Pokémon.
-   [ ] **Team Analyzer:** Provides insights into a created team's strengths and weaknesses.

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png" alt="Pokeball"/>
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png" alt="Bulbasaur"/>
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png" alt="Charmander"/>
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png" alt="Squirtle"/>
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" alt="Pikachu"/>
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/master-ball.png" alt="Masterball"/>
</p>

## 🛠️ Local Development Setup

To run this project locally, you need to run the backend and frontend servers in two separate terminals.

**1. Run the Backend Server:**

Navigate to the project root directory and start the FastAPI server using Uvicorn.

```bash
# Installs dependencies
pip install -r requirements.txt

# Starts the API server on http://127.0.0.1:8000
uvicorn app.main:app --reload
```

**2. Run the Frontend Server:**

The recommended way is to use the **Live Server** extension in Visual Studio Code.

1.  Install the `Live Server` extension.
2.  Right-click the `public/index.html` file.
3.  Select "Open with Live Server".
4.  Your browser will open to `http://127.0.0.1:5500` (or a similar port).

Alternatively, you can use Python's built-in HTTP server. In a new terminal:

```bash
# Navigate into the public directory
cd public

# Start a simple web server on port 8081
python -m http.server 8081
```

## 🧪 QA/QE & CI/CD Focus

This project is designed to be a sandbox for testing and automation. Future goals include:

*   **CI/CD Pipeline:** Set up GitHub Actions to automate testing and deployments upon pull requests and merges.
*   **Automated Testing:**
    *   **Backend:** Implement unit and integration tests for the FastAPI endpoints using `pytest`.
    *   **Frontend:** Use a framework like Playwright or Cypress for end-to-end (E2E) tests that simulate user interactions.
*   **Containerization:** Package the application with Docker to ensure a consistent environment for development and testing.
