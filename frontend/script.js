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
