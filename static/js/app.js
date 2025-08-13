document.addEventListener('DOMContentLoaded', () => {
    // --- DOM References ---
    const pokedexGrid = document.getElementById('pokedex-grid');
    const prevPageBtn = document.getElementById('prev-page-btn');
    const nextPageBtn = document.getElementById('next-page-btn');
    const pageIndicator = document.getElementById('page-indicator');
    const filterContainer = document.getElementById('filter-container');

    // --- State Variables ---
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = false;
    let currentEventSource = null;
    let selectedTypes = [];
    const POKEMONS_PER_PAGE = 21;

    const createPokemonCard = (pokemon) => {
        if (!pokemon || !pokemon.types) {
            console.error('Invalid pokemon data received:', pokemon);
            return '';
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

    const streamAndDisplayPokemons = (page, types = []) => {
        if (isLoading) {
            currentEventSource?.close();
        }
        isLoading = true;
        let cardIndex = 0;

        createSkeletonGrid();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        let url = `/api/pokemons/stream?page=${page}&limit=${POKEMONS_PER_PAGE}`;
        if (types.length > 0) {
            const typeParams = types.map(t => `types=${t}`).join('&');
            url += `&${typeParams}`;
        }
        
        currentEventSource = new EventSource(url);
        let isFirstPokemon = true;

        currentEventSource.onmessage = function(event) {
            const eventData = JSON.parse(event.data);

            if (eventData.type === 'pagination') {
                updatePaginationControls(eventData.data);
            } else if (eventData.type === 'pokemon') {
                if (isFirstPokemon) {
                    pokedexGrid.innerHTML = '';
                    isFirstPokemon = false;
                }
                if (eventData.data.error) {
                    console.error("Error with Pokémon data:", eventData.data.error);
                    return;
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
                if (isFirstPokemon) { // Handle case where no pokemon are returned
                    pokedexGrid.innerHTML = `<div class="grid-message"><p>No Pokémon match the selected filters.</p></div>`;
                    isFirstPokemon = false;
                }
                currentEventSource.close();
                isLoading = false;
            }
        };

        currentEventSource.onerror = function(error) {
            console.error('EventSource failed:', error);
            if (isLoading) {
                pokedexGrid.innerHTML = `<div class="aero-error"><p>Error de conexión. Intente de nuevo.</p></div>`;
            }
            currentEventSource.close();
            isLoading = false;
        };
    };

    const triggerShake = () => {
        filterContainer.classList.add('shake');
        setTimeout(() => filterContainer.classList.remove('shake'), 500);
    };

    const handleFilterClick = (event) => {
        const button = event.target.closest('.type-filter-btn');
        if (!button) return;

        const type = button.dataset.type;
        const seeAllButton = filterContainer.querySelector('[data-type="all"]');

        if (type === 'all') {
            selectedTypes = [];
            filterContainer.querySelectorAll('.type-filter-btn.active').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        } else {
            seeAllButton.classList.remove('active');
            const index = selectedTypes.indexOf(type);

            if (index > -1) {
                selectedTypes.splice(index, 1);
                button.classList.remove('active');
            } else {
                if (selectedTypes.length < 2) {
                    selectedTypes.push(type);
                    button.classList.add('active');
                } else {
                    triggerShake();
                }
            }

            if (selectedTypes.length === 0) {
                seeAllButton.classList.add('active');
            }
        }
        // Reset to page 1 and fetch new data only if selection changed
        if (button.dataset.type !== 'all' && selectedTypes.length >= 2 && selectedTypes.indexOf(type) === -1) {
            // Do not fetch if user tried to select a 3rd type
        } else {
            streamAndDisplayPokemons(1, selectedTypes);
        }
    };

    const populateTypeFilters = async () => {
        try {
            const response = await fetch('/api/types');
            if (!response.ok) throw new Error('Failed to fetch types');
            const types = await response.json();
            
            types.forEach(type => {
                const button = document.createElement('button');
                // NEW: Always add the specific type class for coloring
                button.className = `type-filter-btn type-${type.toLowerCase()}`;
                button.dataset.type = type;
                button.textContent = type;
                filterContainer.appendChild(button);
            });
        } catch (error) {
            console.error('Could not populate type filters:', error);
            filterContainer.innerHTML += '<p class="aero-error">Could not load filters.</p>';
        }
    };

    // --- Event Listeners ---
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            streamAndDisplayPokemons(currentPage - 1, selectedTypes);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            streamAndDisplayPokemons(currentPage + 1, selectedTypes);
        }
    });

    filterContainer.addEventListener('click', handleFilterClick);

    // --- Initial Load ---
    populateTypeFilters();
    streamAndDisplayPokemons(1, selectedTypes);
});
