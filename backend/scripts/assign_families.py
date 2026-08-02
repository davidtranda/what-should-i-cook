from pathlib import Path
import json

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BACKEND_DIR / "database"
INGREDIENTS_FILE = DATABASE_DIR / "ingredients.json"

FAMILIES = {
    "onion": [
        "onion",
        "red_onion",
        "white_onion",
        "shallot",
        "shallots",
        "spring_onion",
        "green_onion",
        "scallion",
        "spring_onions",
    ],
    "garlic": ["garlic"],
    "egg": ["egg", "eggs"],
    "butter": ["butter", "salted_butter", "unsalted_butter"],
    "milk": ["milk", "whole_milk", "semi_skimmed_milk", "skimmed_milk"],
    "cheese": [
        "cheese",
        "cheddar_cheese",
        "mozzarella",
        "parmesan",
        "cubed_feta_cheese",
        "feta_cheese",
        "gouda_cheese",
        "cream_cheese",
        "bryndza_cheese",
        "cottage_cheese",
        "goats_cheese",
        "emmentaler_cheese",
        "farmers_cheese",
        "liquid_cheese",
        "monterey_jack_cheese",
        "panquehue_cheese",
        "shredded_mexican_cheese",
        "stilton_cheese",
        "swiss_cheese",
        "cheese_curds",
    ],
    "bread": ["bread", "burger_buns", "baguette", "toast_bread", "toast", "bread_rolls"],
    "pasta": [
        "spaghetti",
        "penne_pasta",
        "fusilli",
        "macaroni",
        "farfalle",
        "linguine_pasta",
        "tagliatelle",
        "bowtie_pasta",
    ],
    "rice": ["rice", "basmati_rice", "brown_rice", "arabic_rice"],
    "chicken": ["chicken", "chicken_breast", "chicken_legs"],
    "beef": ["beef", "ground_beef", "beef_steak"],
    "fish": ["salmon", "tuna", "cod", "anchovy_fillet", "anchovy"],
    "lettuce": ["lettuce", "romaine_lettuce", "iceberg_lettuce", "baby_lettuce_leaves"],
    "tomato": [
        "tomato",
        "tomato_sauce",
        "tomato_puree",
        "tomato_ketchup",
        "cherry_tomatoes",
        "baby_plum_tomatoes",
        "beef_tomatoes",
        "canned_tomatoes",
        "chopped_tomatoes",
        "diced_tomatoes",
        "grape_tomatoes",
        "plum_tomatoes",
        "sun_dried_tomatoes",
        "tinned_tomatos",
        "vine_tomatoes",
    ],
    "pepper": [
        "bell_pepper",
        "red_bell_pepper",
        "green_bell_pepper",
        "yellow_bell_pepper",
        "banana_pepper",
        "pepper",
        "black_pepper",
    ],
    "potato": ["potato", "potatoes", "baby_new_potatoes", "new_potatoes"],
    "mushroom": ["mushroom", "button_mushroom", "chestnut_mushroom", "shiitake_mushroom"],
    "carrot": ["carrot", "carrots"],
    "cucumber": ["cucumber", "cucumbers"],
    "spinach": ["spinach"],
}

FAMILY_KEYWORDS = {
    "tomato": ["tomato", "tomatoes", "tomatos"],
    "cheese": ["cheese", "cheddar", "mozzarella", "parmesan", "feta", "gouda", "bryndza", "emmentaler", "stilton", "swiss", "cottage"],
    "onion": ["onion", "shallot", "shallots", "scallion", "spring onion", "green onion"],
    "garlic": ["garlic"],
    "egg": ["egg"],
    "butter": ["butter"],
    "milk": ["milk"],
    "bread": ["bread", "bun", "buns", "baguette", "toast"],
    "pasta": ["pasta", "spaghetti", "penne", "fusilli", "macaroni", "farfalle", "linguine", "tagliatelle"],
    "rice": ["rice"],
    "chicken": ["chicken"],
    "beef": ["beef"],
    "fish": ["fish", "salmon", "tuna", "cod", "anchovy", "sardine"],
    "lettuce": ["lettuce", "romaine", "iceberg"],
    "pepper": ["pepper"],
    "potato": ["potato", "potatoes"],
    "mushroom": ["mushroom"],
    "carrot": ["carrot", "carrots"],
    "cucumber": ["cucumber"],
    "spinach": ["spinach"],
}


def resolve_family(ingredient):
    slug = ingredient.get("slug", "")
    name = ingredient.get("name", "")
    aliases = ingredient.get("aliases", [])
    haystack = " ".join([slug, name, *aliases]).lower()

    for family, members in FAMILIES.items():
        if slug in members:
            return family

    for family, keywords in FAMILY_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            return family

    return ingredient.get("family") or slug


with open(INGREDIENTS_FILE, "r", encoding="utf-8") as file:
    ingredients = json.load(file)

updated = 0

for ingredient in ingredients:
    previous_family = ingredient.get("family")
    new_family = resolve_family(ingredient)
    ingredient["family"] = new_family

    if previous_family != new_family:
        updated += 1

with open(INGREDIENTS_FILE, "w", encoding="utf-8") as file:
    json.dump(ingredients, file, indent=4, ensure_ascii=False)

print(f"\nUpdated {updated} ingredients.")
