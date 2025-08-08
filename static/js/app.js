document.addEventListener('DOMContentLoaded', () => {
    // --- DOM References ---
    const pokedexGrid = document.getElementById('pokedex-grid');
    const prevPageBtn = document.getElementById('prev-page-btn');
    const nextPageBtn = document.getElementById('next-page-btn');
    const pageIndicator = document.getElementById('page-indicator');

    // --- State Variables ---
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = false;
    let currentEventSource = null; // To hold the active stream connection
    const POKEMONS_PER_PAGE = 21;

    const createPokemonCard = (pokemon) => {
        if (!pokemon || !pokemon.types) {
            console.error('Invalid pokemon data received:', pokemon);
            return ''; // Return an empty string if data is invalid
        }
        const typesHtml = pokemon.types.map(type => 
            `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`
        ).join('');

        return `
            <article class="pokemon-card" data-pokemon-id="${pokemon.id}">
                <div class="card-reflection"></div>
                <div class="pokeball-top"></div>
                <div class="pokeball-bottom"></div>
                <div class="pokeball-divider"></div>
                <div class="pokeball-button"></div>
                <div class="sprite-container">
                    <img src="${pokemon.sprite}" alt="${pokemon.name}" class="pokemon-sprite" loading="lazy">
                </div>
                <span class="pokemon-number">#${String(pokemon.id).padStart(3, '0')}</span>
                <div class="info-panel">
                    <h2 class="pokemon-name">${pokemon.name}</h2>
                    <div class="types-container">${typesHtml}</div>
                </div>
            </article>
        `;
    };

    const createSkeletonGrid = () => {
        const skeletonHTML = Array.from({ length: POKEMONS_PER_PAGE })
            .map(() => `<div class="pokemon-card-skeleton"></div>`)
            .join('');
        pokedexGrid.innerHTML = skeletonHTML;
    };

    const apply3DEffect = (card) => {
        const handleMove = (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            card.style.transform = `perspective(1000px) scale(1.02) rotateX(${y * 10}deg) rotateY(${-x * 10}deg)`;
        };
        const handleLeave = () => { card.style.transform = ''; };
        card.addEventListener('mousemove', handleMove);
        card.addEventListener('mouseleave', handleLeave);
    };

    const updatePaginationControls = (paginationData) => {
        totalPages = paginationData.total_pages;
        currentPage = paginationData.current_page;
        pageIndicator.textContent = `Página ${currentPage} de ${totalPages}`;
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    };

    const streamAndDisplayPokemons = (page) => {
        if (isLoading) {
            currentEventSource?.close(); // Close any existing stream
        }
        isLoading = true;
        let cardIndex = 0;

        createSkeletonGrid();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        const url = `/api/pokemons/stream?page=${page}&limit=${POKEMONS_PER_PAGE}`;
        currentEventSource = new EventSource(url);

        let isFirstPokemon = true;

        currentEventSource.onmessage = function(event) {
            const eventData = JSON.parse(event.data);

            if (eventData.type === 'pagination') {
                updatePaginationControls(eventData.data);
            } else if (eventData.type === 'pokemon') {
                if (isFirstPokemon) {
                    pokedexGrid.innerHTML = ''; // Clear skeletons on first pokemon arrival
                    isFirstPokemon = false;
                }

                if (eventData.data.error) {
                    console.error("Error with Pokémon data:", eventData.data.error);
                    return; // Skip rendering this card
                }

                const cardHTML = createPokemonCard(eventData.data);
                const cardElement = document.createElement('div');
                cardElement.innerHTML = cardHTML;
                const newCard = cardElement.firstElementChild;

                if (newCard) {
                    pokedexGrid.appendChild(newCard);
                    newCard.style.setProperty('--card-index', cardIndex++);
                    newCard.classList.add('card-entrance');
                    apply3DEffect(newCard);
                }
            } else if (eventData.type === 'done') {
                // Stream finished successfully, close the connection gracefully
                currentEventSource.close();
                isLoading = false;
            }
        };

        currentEventSource.onerror = function(error) {
            // This will now only fire on actual network errors, not on stream completion
            console.error('EventSource failed:', error);
            if (isLoading) { // Avoid showing error if connection was closed intentionally
                pokedexGrid.innerHTML = `<div class="aero-error"><p>Error de conexión. Intente de nuevo.</p></div>`;
            }
            currentEventSource.close();
            isLoading = false;
        };
    };

    // --- Event Listeners ---
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            streamAndDisplayPokemons(currentPage - 1);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            streamAndDisplayPokemons(currentPage + 1);
        }
    });

    // --- Initial Load ---
    streamAndDisplayPokemons(currentPage);
});
