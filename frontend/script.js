const API = "http://127.0.0.1:8000";

const ingredientSearch = document.getElementById("ingredient-search");
const searchResults = document.getElementById("search-results");
const quantityInput = document.getElementById("quantity-input");
const saveButton = document.getElementById("save-btn");
const ingredientList = document.getElementById("ingredient-list");
const modal = document.getElementById("modal-overlay");
const openModalButton = document.getElementById("open-modal-btn");
const closeModalButton = document.getElementById("close-modal-btn");
const unitChips = document.getElementById("unit-chips");
const findMealButton = document.getElementById("find-meal-btn");


let selectedUnit = null;
let inventory = [];
let showAll = false;
let selectedIngredient = null;
let inventoryQuery = "";

const inventorySearch =
    document.getElementById("inventory-search");

const toggleText =
    document.getElementById("toggle-text");

const toggleIcon =
    document.getElementById("toggle-icon");

const toggleInventoryButton =
    document.getElementById("toggle-inventory-btn");

const recommendationsSection =
    document.getElementById("recommendations-section");

const recommendationsList =
    document.getElementById("recommendations-list");    


toggleInventoryButton.addEventListener("click", () => {

    showAll = !showAll;

    renderInventory();

});

inventorySearch.addEventListener("input", () => {

    inventoryQuery =
        inventorySearch.value.toLowerCase();

    renderInventory();

});

saveButton.addEventListener("click", addIngredient);

ingredientSearch.addEventListener("input", searchIngredients);

openModalButton.addEventListener("click", openModal);

closeModalButton.addEventListener("click", closeModal);

findMealButton.addEventListener(
    "click",
    findMeal
);

const categoryIcons = {

    dairy: "milk",

    meat: "beef",

    fruits: "apple",

    vegetables: "carrot",

    grains: "wheat",

    spices: "chef-hat",

    seafood: "fish",

    drinks: "glass-water",

    sweets: "cookie",

    pantry: "package",

    other: "package"

};

async function searchIngredients() {

    const query = ingredientSearch.value.trim();
    selectedIngredient = null;

    if (query.length < 2) {

        searchResults.innerHTML = "";
        return;

    }

    try {

        const response = await fetch(
            `${API}/ingredients/search?q=${encodeURIComponent(query)}`
        );

        const ingredients = await response.json();

        displayResults(ingredients);

    } catch (error) {

        console.error(error);

    }

}

function displayResults(ingredients) {

    searchResults.innerHTML = "";

    ingredients.forEach(ingredient => {

        const item = document.createElement("div");

        item.className = "search-item";

        item.textContent = ingredient.name;

        item.addEventListener("click", () => {

            console.log("Ingredient selectat:", ingredient);

            selectedIngredient = ingredient;

            ingredientSearch.value = ingredient.name;

            searchResults.innerHTML = "";
    console.log(ingredient);
    console.log(ingredient.allowed_units);

    renderUnitChips(ingredient.allowed_units);

        });

        searchResults.appendChild(item);

    });

}

function renderUnitChips(units) {

    unitChips.innerHTML = "";

    selectedUnit = units[0];

    units.forEach((unit, index) => {

        const chip = document.createElement("button");

        chip.className = "unit-chip";

        if (index === 0) {
            chip.classList.add("active");
        }

        chip.textContent = unit;

        chip.addEventListener("click", () => {

            document
                .querySelectorAll(".unit-chip")
                .forEach(c => c.classList.remove("active"));

            chip.classList.add("active");

            selectedUnit = unit;

        });

        unitChips.appendChild(chip);

    });

}

function addIngredient() {

    if (!selectedIngredient) return;

    const quantity = quantityInput.value.trim();

    if (quantity === "") return;

    const ingredient = {

    id: selectedIngredient.id,

    slug: selectedIngredient.slug,

    name: selectedIngredient.name,

    quantity: quantity,

    unit: selectedUnit,

    category: selectedIngredient.category

    };

    inventory.push(ingredient);

    renderInventory();

    clearModal();

    closeModal();

}

function renderInventory() {

    ingredientList.innerHTML = "";

    let filteredInventory = inventory.filter(item =>
    item.name
        .toLowerCase()
        .includes(inventoryQuery)
    );

    const visibleIngredients = showAll
        ? filteredInventory
        : filteredInventory.slice(0, 3);


    visibleIngredients.forEach((item, index) => {

        const card = document.createElement("div");

        card.className = "ingredient-card";

        card.innerHTML = `
            <div class="ingredient-info">

                <div class="ingredient-name">
                    <i data-lucide="${categoryIcons[item.category] || 'package'}"></i>
                    <span>${item.name}</span>
                </div>

                <div class="ingredient-quantity">
                    ${item.quantity} ${item.unit}
                </div>

            </div>

            <button
                class="delete-button"
                onclick="removeIngredient(${index})"
                >
                <i data-lucide="trash-2"></i>
            </button>
        `;

        ingredientList.appendChild(card);

        lucide.createIcons();

        if (filteredInventory.length <= 3) {

        toggleInventoryButton.classList.add("hidden");

        } else {

        toggleInventoryButton.classList.remove("hidden");

        if (showAll) {

            toggleText.textContent =
                "Show less";

                toggleIcon.setAttribute(
                    "data-lucide",
                    "chevron-up"
                );

        } else {

            toggleText.textContent =
                `Show all (${filteredInventory.length})`;

                toggleIcon.setAttribute(
                    "data-lucide",
                    "chevron-down"
                );
        }

    lucide.createIcons();

    }

    });

}

function removeIngredient(index) {

    inventory.splice(index, 1);

    renderInventory();

}

function clearModal() {

    selectedIngredient = null;

    ingredientSearch.value = "";

    quantityInput.value = "";

    searchResults.innerHTML = "";

    unitChips.innerHTML = "";

    selectedUnit = null;

}

function openModal() {

    modal.classList.remove("hidden");

}

function closeModal() {

    modal.classList.add("hidden");

}

async function findMeal() {

    const inventorySlugs = inventory.map(
        ingredient => ingredient.slug
    );

    try {

        const originalText = findMealButton.innerHTML;

            findMealButton.disabled = true;

            findMealButton.innerHTML = `
                <i data-lucide="loader-circle"></i>
                <span>Finding meals...</span>
            `;

            lucide.createIcons();

        const response = await fetch(
            "http://127.0.0.1:8000/recipes/recommend",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    inventory: inventorySlugs
                })
            }
        );

        const recipes = await response.json();

        console.log(recipes);
        renderRecommendations(recipes);

        recommendationsSection.scrollIntoView({
            behavior: "smooth"
        });

        findMealButton.disabled = false;
        findMealButton.innerHTML = originalText;

        lucide.createIcons();

    } catch (error) {

        findMealButton.disabled = false;
        findMealButton.innerHTML = originalText;

        lucide.createIcons();
        console.error(error);

    }

}

function renderRecipeCard(recipe) {

    const matchedIngredients = recipe.matched_ingredients
        .map(ingredient => `
            <div class="ingredient-item available">
                <i data-lucide="check-circle-2"></i>
                ${formatIngredientName(ingredient)}
            </div>
        `)
        .join("");

    const missingIngredients = recipe.missing_ingredients
        .map(ingredient => `
            <div class="ingredient-item missing">
                <i data-lucide="circle-alert"></i>
                ${formatIngredientName(ingredient)}
            </div>
        `)
        .join("");

    return `

        <div class="recipe-card">

            <div class="recipe-card-header">

                <div class="recipe-title">
                    <i data-lucide="chef-hat"></i>
                    ${recipe.name}
                </div>

                <div class="match-badge ${getMatchBadgeClass(recipe.score)}">
                    ${recipe.score}% Match
                </div>

            </div>

            <div class="match-progress">
                <div
                    class="match-progress-fill"
                    style="width:${recipe.score}%"
                ></div>
            </div>

            <div class="recipe-meta">

                <div>
                    <i data-lucide="clock-3"></i>
                    ${recipe.time} min
                </div>

                <div class="difficulty-badge ${getDifficultyClass(recipe.difficulty)}">
                    <i data-lucide="bar-chart-3"></i>
                    ${recipe.difficulty}
                </div>

            </div>

            <div class="recipe-ingredients">

                <h4>You have</h4>

                ${matchedIngredients}

            </div>

            ${
                recipe.missing_ingredients.length > 0
                    ? `
                    <div class="recipe-ingredients">

                        <h4>Missing</h4>

                        ${missingIngredients}

                    </div>
                    `
                    : `
                    <div class="recipe-ready">

                        <i data-lucide="badge-check"></i>

                        Ready to cook

                    </div>
                    `
            }

        </div>

    `;

}

function renderRecommendations(recipes) {

    recommendationsSection.classList.remove("hidden");

    recommendationsList.innerHTML = "";

    if (recipes.length === 0) {

        recommendationsList.innerHTML = `

            <div class="empty-state">

                <i data-lucide="utensils-crossed"></i>

                <h3>No meals found</h3>

                <p>Try adding more ingredients.</p>

            </div>

        `;

        lucide.createIcons();

        return;

    }

    const readyRecipes = recipes.filter(recipe => recipe.ready_to_cook);

    const almostReadyRecipes = recipes.filter(
        recipe =>
            !recipe.ready_to_cook &&
            recipe.missing_count <= 2
    );

    const otherRecipes = recipes.filter(
        recipe =>
            !recipe.ready_to_cook &&
            recipe.missing_count > 2
    );

    if (readyRecipes.length > 0) {

        recommendationsList.innerHTML += `

            <div class="recommendation-group">

                <h3>Ready to cook (${readyRecipes.length})</h3>

            </div>

        `;

        readyRecipes.forEach(recipe => {

            recommendationsList.innerHTML += renderRecipeCard(recipe);

        });

    }

    if (almostReadyRecipes.length > 0) {

        recommendationsList.innerHTML += `

            <div class="recommendation-group">

                <h3>Almost ready (${almostReadyRecipes.length})</h3>

            </div>

        `;

        almostReadyRecipes.forEach(recipe => {

            recommendationsList.innerHTML += renderRecipeCard(recipe);

        });

    }

    if (otherRecipes.length > 0) {

        recommendationsList.innerHTML += `

            <div class="show-more-container">

                <button
                    id="show-more-recipes-btn"
                    class="secondary-button"
                >

                    <i data-lucide="chevrons-down"></i>

                    Show ${otherRecipes.length} more recipes

                </button>

            </div>

        `;

    }

    const showMoreButton = document.getElementById("show-more-recipes-btn");

    if (showMoreButton) {

        showMoreButton.addEventListener("click", () => {

            showMoreButton.parentElement.remove();

            otherRecipes.forEach(recipe => {

                recommendationsList.innerHTML += renderRecipeCard(recipe);

            });

            lucide.createIcons();

        });

    }

    lucide.createIcons();
}

function getMatchBadgeClass(score) {

    if (score >= 90) return "match-excellent";

    if (score >= 70) return "match-good";

    return "match-poor";

}

function getDifficultyClass(difficulty) {

    switch (difficulty.toLowerCase()) {

        case "easy":
            return "difficulty-easy";

        case "medium":
            return "difficulty-medium";

        case "hard":
            return "difficulty-hard";

        default:
            return "";
    }

}

function formatIngredientName(name) {

    return name
        .replaceAll("_", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());

}