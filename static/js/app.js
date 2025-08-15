document.addEventListener('DOMContentLoaded', () => {
    // --- DOM References ---
    const pokedexGrid = document.getElementById('pokedex-grid');
    const prevPageBtn = document.getElementById('prev-page-btn');
    const nextPageBtn = document.getElementById('next-page-btn');
    const pageIndicator = document.getElementById('page-indicator');
    const typeFilterContainer = document.getElementById('type-filters');
    
    // --- Custom Generation Select DOM References ---
    const generationSelectContainer = document.getElementById('generation-select'); // This is the main clickable div
    const generationSelectedValue = generationSelectContainer.querySelector('.selected-value');
    const generationOptionsContainer = document.getElementById('generation-options');

    const pokemonSearchInput = document.getElementById('pokemon-search');
    const autocompleteSuggestionsContainer = document.getElementById('autocomplete-suggestions');
    const surpriseMeBtn = document.getElementById('surprise-me-btn'); // New button
    const filterContainer = document.getElementById('filter-container'); // Reference to the main filter container
    const generationFilterContainer = document.getElementById('generation-filter-container'); // New reference

    // --- State Variables ---
    let currentPage = 1;
    let totalPages = 1;
    let isLoading = false;
    let currentEventSource = null;
    let selectedTypes = [];
    let selectedGeneration = 'all';
    let isSearchingByName = false; // New state variable for search bar
    let searchTimeout = null; // For debouncing
    const POKEMONS_PER_PAGE = 21;

    // --- Utility Functions ---
    const debounce = (func, delay) => {
        let timeout;
        return function(...args) {
            const context = this;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), delay);
        };
    };

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
        
        const disablePagination = isSearchingByName || totalPages <= 1;
        prevPageBtn.disabled = disablePagination || currentPage === 1;
        nextPageBtn.disabled = disablePagination || currentPage === totalPages;
    };

    const toggleFilterControls = (disable) => {
        // This function will now ONLY handle the visual aspect (dimming)
        // The actual disabling logic is handled by `isSearchingByName` in each event listener
        if (disable) {
            typeFilterContainer.classList.add('filter-section-disabled');
            generationSelectContainer.parentElement.classList.add('filter-section-disabled');
        } else {
            typeFilterContainer.classList.remove('filter-section-disabled');
            generationSelectContainer.parentElement.classList.remove('filter-section-disabled');
        }
    };

    const streamAndDisplayPokemons = (page, types = [], generation = 'all', pokemonId = null) => {
        if (isLoading) {
            currentEventSource?.close();
        }
        isLoading = true;
        let cardIndex = 0;

        createSkeletonGrid();
        window.scrollTo({ top: 0, behavior: 'smooth' });

        let url;
        if (pokemonId) {
            url = `/api/pokemons/stream?page=1&limit=1&pokemon_id=${pokemonId}`; // Fetch only the specific pokemon
            // Pagination controls will be disabled by updatePaginationControls
        } else {
            url = `/api/pokemons/stream?page=${page}&limit=${POKEMONS_PER_PAGE}`;
            if (types.length > 0) {
                const typeParams = types.map(t => `types=${t}`).join('&');
                url += `&${typeParams}`;
            }
            if (generation !== 'all' && generation !== null && generation !== undefined && generation !== '') {
                url += `&generation=${encodeURIComponent(generation)}`;
            }
        }

        currentEventSource = new EventSource(url);
        let isFirstPokemon = true;

        currentEventSource.onmessage = function (event) {
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
                if (isFirstPokemon) { // No pokemon were streamed
                    pokedexGrid.innerHTML = `<div class="grid-message"><p>No Pokémon match the selected filters.</p></div>`;
                    if (isSearchingByName) {
                        pokedexGrid.innerHTML = `<div class="grid-message"><p>No Pokémon found with that name.</p></div>`;
                    }
                    isFirstPokemon = false;
                }
                currentEventSource.close();
                isLoading = false;
            }
        };

        currentEventSource.onerror = function (error) {
            console.error('EventSource failed:', error);
            if (isLoading) {
                pokedexGrid.innerHTML = `<div class="grid-message"><p>Error de conexión. Intente de nuevo.</p></div>`;
            }
            currentEventSource.close();
            isLoading = false;
        };
    };

    const triggerShake = () => {
        typeFilterContainer.parentElement.classList.add('shake');
        setTimeout(() => typeFilterContainer.parentElement.classList.remove('shake'), 500);
    };

    const handleFilterClick = (event) => {
        if (isSearchingByName) {
            resetSearch();
            return;
        }
        const button = event.target.closest('.type-filter-btn');
        if (!button) return;

        const type = button.dataset.type;
        const seeAllButton = typeFilterContainer.querySelector('[data-type="all"]');

        if (type === 'all') {
            selectedTypes = [];
            typeFilterContainer.querySelectorAll('.type-filter-btn.active').forEach(btn => btn.classList.remove('active'));
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
        streamAndDisplayPokemons(1, selectedTypes, selectedGeneration);
    };

    const populateTypeFilters = async () => {
        try {
            const response = await fetch('/api/types');
            if (!response.ok) throw new Error('Failed to fetch types');
            const types = await response.json();

            types.forEach(type => {
                const button = document.createElement('button');
                button.className = `type-filter-btn type-${type.toLowerCase()}`;
                button.dataset.type = type;
                button.textContent = type;
                typeFilterContainer.appendChild(button);
            });
        } catch (error) {
            console.error('Could not populate type filters:', error);
        }
    };

    const populateGenerationFilter = async () => {
        try {
            const response = await fetch('/api/generations');
            if (!response.ok) throw new Error('Failed to fetch generations');
            const generations = await response.json();

            // Clear previous options and add the 'All Generations' option first
            generationOptionsContainer.innerHTML = '';
            const allGenOption = document.createElement('div');
            allGenOption.className = 'aero-option selected'; // Selected by default
            allGenOption.dataset.value = 'all';
            allGenOption.textContent = 'All Generations';
            generationOptionsContainer.appendChild(allGenOption);

            generations.forEach(gen => {
                const option = document.createElement('div');
                option.className = 'aero-option';
                option.dataset.value = gen.id;
                option.textContent = `Generation ${gen.name}`;
                generationOptionsContainer.appendChild(option);
            });
        } catch (error) {
            console.error('Could not populate generation filter:', error);
        }
    };

    // --- Autocomplete Logic ---
    const fetchAutocompleteSuggestions = async (query) => {
        if (query.length < 2) { // Only search if query is at least 2 characters
            autocompleteSuggestionsContainer.innerHTML = '';
            autocompleteSuggestionsContainer.style.display = 'none';
            return;
        }
        try {
            const response = await fetch(`/api/pokemons/names_autocomplete?query=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Failed to fetch autocomplete suggestions');
            const suggestions = await response.json();
            
            autocompleteSuggestionsContainer.innerHTML = '';
            if (suggestions.length > 0) {
                suggestions.forEach(pokemon => {
                    const item = document.createElement('div');
                    item.classList.add('autocomplete-suggestion-item');
                    item.textContent = pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1); // Capitalize name
                    item.dataset.pokemonId = pokemon.id;
                    autocompleteSuggestionsContainer.appendChild(item);
                });
                autocompleteSuggestionsContainer.style.display = 'block';
            } else {
                autocompleteSuggestionsContainer.style.display = 'none';
            }
        } catch (error) {
            console.error('Error fetching autocomplete suggestions:', error);
            autocompleteSuggestionsContainer.style.display = 'none';
        }
    };

    const handleAutocompleteSelection = (event) => {
        const selectedItem = event.target.closest('.autocomplete-suggestion-item');
        if (selectedItem) {
            const pokemonName = selectedItem.textContent;
            const pokemonId = selectedItem.dataset.pokemonId;
            pokemonSearchInput.value = pokemonName;
            autocompleteSuggestionsContainer.style.display = 'none';
            isSearchingByName = true;
            toggleFilterControls(true); // Disable filters
            streamAndDisplayPokemons(1, [], [], pokemonId); // Display single pokemon
        }
    };

    const resetSearch = () => {
        pokemonSearchInput.value = '';
        isSearchingByName = false;
        toggleFilterControls(false); // Enable filters
        autocompleteSuggestionsContainer.style.display = 'none';
        streamAndDisplayPokemons(1, selectedTypes, selectedGeneration); // Restore filtered view
    };

    // --- Event Listeners ---
    prevPageBtn.addEventListener('click', () => {
        if (isSearchingByName) {
            resetSearch();
            return;
        }
        if (currentPage > 1) {
            streamAndDisplayPokemons(currentPage - 1, selectedTypes, selectedGeneration);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (isSearchingByName) {
            resetSearch();
            return;
        }
        if (currentPage < totalPages) {
            streamAndDisplayPokemons(currentPage + 1, selectedTypes, selectedGeneration);
        }
    });

    typeFilterContainer.addEventListener('click', handleFilterClick);

    // --- Custom Generation Select Logic ---
    generationSelectContainer.addEventListener('click', (e) => {
        if (isSearchingByName) {
            resetSearch();
            return;
        }
        e.stopPropagation();
        const isOpen = generationOptionsContainer.classList.toggle('show');
        generationSelectContainer.classList.toggle('open', isOpen);
    });

    generationOptionsContainer.addEventListener('click', (event) => {
        const option = event.target.closest('.aero-option');
        if (option) {
            event.stopPropagation(); // Stop event from closing the dropdown immediately
            if (isSearchingByName) {
                resetSearch();
            }
            
            selectedGeneration = option.dataset.value;
            generationSelectedValue.textContent = option.textContent;
            
            generationOptionsContainer.querySelectorAll('.aero-option').forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');

            // Close dropdown after selection
            generationOptionsContainer.classList.remove('show');
            generationSelectContainer.classList.remove('open');

            streamAndDisplayPokemons(1, selectedTypes, selectedGeneration);
        }
    });

    pokemonSearchInput.addEventListener('input', debounce((e) => {
        const query = e.target.value.trim();
        if (query === '') {
            resetSearch();
        } else {
            fetchAutocompleteSuggestions(query);
        }
    }, 300));

    pokemonSearchInput.addEventListener('focus', () => {
        if (pokemonSearchInput.value.length >= 2) {
            autocompleteSuggestionsContainer.style.display = 'block';
        }
    });

    // Hide suggestions and custom dropdown when clicking outside
    document.addEventListener('click', (event) => {
        if (!pokemonSearchInput.contains(event.target) && !autocompleteSuggestionsContainer.contains(event.target)) {
            autocompleteSuggestionsContainer.style.display = 'none';
        }
        if (!generationSelectContainer.contains(event.target)) {
            generationOptionsContainer.classList.remove('show');
            generationSelectContainer.classList.remove('open');
        }
    });

    autocompleteSuggestionsContainer.addEventListener('click', handleAutocompleteSelection);

    surpriseMeBtn.addEventListener('click', () => {
        // Generate 3 unique random IDs
        const randomIds = new Set();
        while (randomIds.size < 3) {
            const randomId = Math.floor(Math.random() * 1025) + 1;
            randomIds.add(randomId);
        }

        // Clear search input and disable filters
        pokemonSearchInput.value = '';
        isSearchingByName = true;
        toggleFilterControls(true);
        autocompleteSuggestionsContainer.style.display = 'none';

        // Fetch the 3 random Pokémon
        const idsArray = Array.from(randomIds);
        const idParams = idsArray.map(id => `pokemon_ids=${id}`).join('&');
        const url = `/api/pokemons/stream?${idParams}`;

        // Close any existing stream and start a new one
        if (isLoading) {
            currentEventSource?.close();
        }
        currentEventSource = new EventSource(url);
        
        // Reuse the main streaming logic to display the cards
        let isFirstPokemon = true;
        createSkeletonGrid(); // Show skeletons while loading

        currentEventSource.onmessage = function (event) {
            const eventData = JSON.parse(event.data);

            if (eventData.type === 'pagination') {
                updatePaginationControls({ total_pages: 1, current_page: 1 }); // Override pagination
            } else if (eventData.type === 'pokemon') {
                if (isFirstPokemon) {
                    pokedexGrid.innerHTML = '';
                    isFirstPokemon = false;
                }
                const cardHTML = createPokemonCard(eventData.data);
                const cardElement = document.createElement('div');
                cardElement.innerHTML = cardHTML;
                const newCard = cardElement.firstElementChild;
                if (newCard) {
                    pokedexGrid.appendChild(newCard);
                    apply3DEffect(newCard);
                }
            } else if (eventData.type === 'done') {
                currentEventSource.close();
                isLoading = false;
            }
        };

        currentEventSource.onerror = function (error) {
            console.error('EventSource failed:', error);
            pokedexGrid.innerHTML = `<div class="grid-message"><p>Error fetching random Pokémon.</p></div>`;
            currentEventSource.close();
            isLoading = false;
        };
    });

    // --- Initial Load ---
    populateTypeFilters();
    populateGenerationFilter();
    streamAndDisplayPokemons(1, selectedTypes, selectedGeneration);
});