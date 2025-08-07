// Esperamos a que el DOM esté completamente cargado para empezar a trabajar.
document.addEventListener('DOMContentLoaded', () => {
    // --- Referencias a elementos del DOM ---
    // Guardamos una referencia al contenedor donde pintaremos las tarjetas.
    const pokedexGrid = document.getElementById('pokedex-grid');
    
    // --- Constantes y Configuración ---
    // ¡CAMBIO CLAVE #1!
    // Ahora apuntamos al nuevo y potente endpoint que nos da todo de una vez.
    const API_URL = '/generation/1';
    const POKEMON_PER_BATCH = 12; // Número de Pokémon por lote
    const BATCH_DELAY = 300; // Milisegundos entre lotes
    const BATCH_SIZE = 12;
    let currentStartId = 1;
    let isLoading = false;
    const MAX_POKEMON = 151; // Primera generación

    /**
     * Obtiene la lista completa de Pokémon de nuestro backend.
     * Esta función hace UNA SOLA petición de red.
     */
    const fetchFirstGeneration = async () => {
        try {
            // Hacemos el fetch a nuestro endpoint de lote.
            const response = await fetch(API_URL);
            if (!response.ok) {
                // Si el backend devuelve un error (ej. 500), lo capturamos.
                throw new Error(`Error del servidor: ${response.status}`);
            }
            // El backend nos devuelve un array de objetos Pokémon, listo para usar.
            return await response.json();
        } catch (error) {
            console.error("Falló la obtención de la primera generación:", error);
            pokedexGrid.innerHTML = `<p class="error-message">Error al cargar los datos. El servidor puede estar ocupado.</p>`;
            return []; // Devolvemos un array vacío para no romper el resto del código.
        }
    };

    /**
     * ¡REUTILIZACIÓN DE CÓDIGO!
     * Esta función NO CAMBIA. Sigue siendo la misma porque su única
     * responsabilidad es tomar UN objeto Pokémon y convertirlo en HTML.
     * Es modular y reutilizable, una excelente práctica de diseño.
     * @param {object} pokemon - El objeto de un Pokémon.
     * @returns {string} - El string HTML de la tarjeta.
     */
    const createPokemonCard = (pokemon) => {
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
                    <img 
                        src="${pokemon.sprite}" 
                        alt="${pokemon.name}" 
                        class="pokemon-sprite"
                        loading="lazy"
                    >
                </div>
                
                <span class="pokemon-number">#${String(pokemon.id).padStart(3, '0')}</span>

                <!-- Panel de Información para agrupar nombre y tipos -->
                <div class="info-panel">
                    <h2 class="pokemon-name">${pokemon.name}</h2>
                    <div class="types-container">
                        ${typesHtml}
                    </div>
                </div>
            </article>
        `;
    };

    const createLoadingSpinner = () => `
        <div class="aero-loading">
            <div class="aero-spinner"></div>
            <p class="loading-text">Cargando Pokémon...</p>
        </div>
    `;

    const apply3DEffect = (card) => {
        const handleMove = (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            const rotateX = y * 10;
            const rotateY = -x * 10;
            
            card.style.transform = `
                perspective(1000px)
                scale(1.02)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
            `;

            // Ajustar reflejo según posición del mouse
            const reflection = card.querySelector('.card-reflection');
            if (reflection) {
                reflection.style.opacity = 0.5 + (y * 0.3);
            }
        };

        const handleLeave = () => {
            card.style.transform = '';
            const reflection = card.querySelector('.card-reflection');
            if (reflection) {
                reflection.style.opacity = 0.7;
            }
        };

        card.addEventListener('mousemove', handleMove);
        card.addEventListener('mouseleave', handleLeave);
    };

    const applyCardAnimations = () => {
        const cards = document.querySelectorAll('.pokemon-card');
        cards.forEach((card, index) => {
            card.style.setProperty('--card-index', index % BATCH_SIZE);
            card.classList.add('card-entrance');
            apply3DEffect(card);
        });
    };

    const loadNextBatch = async () => {
        if (isLoading || currentStartId > MAX_POKEMON) return;
        
        isLoading = true;
        
        if (currentStartId === 1) {
            pokedexGrid.innerHTML = createLoadingSpinner();
        }

        try {
            const response = await fetch(`/api/pokemon/batch?start=${currentStartId}&count=${BATCH_SIZE}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const pokemonBatch = await response.json();
            
            if (pokemonBatch.length === 0) {
                if (currentStartId === 1) {
                    pokedexGrid.innerHTML = '<div class="aero-error">No se encontraron Pokémon</div>';
                }
                return;
            }

            const batchHTML = pokemonBatch.map(createPokemonCard).join('');
            
            if (currentStartId === 1) {
                pokedexGrid.innerHTML = batchHTML;
            } else {
                pokedexGrid.insertAdjacentHTML('beforeend', batchHTML);
            }

            applyCardAnimations();
            currentStartId += pokemonBatch.length;

            if (currentStartId <= MAX_POKEMON) {
                setTimeout(() => loadNextBatch(), 300);
            }
        } catch (error) {
            console.error('Error:', error);
            if (currentStartId === 1) {
                pokedexGrid.innerHTML = `
                    <div class="aero-error">
                        <p>Error al cargar los Pokémon</p>
                        <button class="aero-button" onclick="location.reload()">Reintentar</button>
                    </div>
                `;
            }
        } finally {
            isLoading = false;
        }
    };

    // Iniciar la carga
    loadNextBatch();
});
