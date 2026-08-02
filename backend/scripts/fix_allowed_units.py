import json
from pathlib import Path

# ==========================================
# FILES
# ==========================================

database = Path(__file__).parent.parent / "database"
ingredients_file = database / "ingredients.json"

# ==========================================
# UNIT FIXES
# ==========================================

UNIT_FIXES = {

    # Seasonings
    "salt": ["g", "pinch"],
    "black_pepper": ["g", "pinch"],
    "white_pepper": ["g", "pinch"],
    "paprika": ["g", "tsp"],
    "oregano": ["g", "tsp"],
    "basil": ["g", "tsp"],
    "thyme": ["g", "tsp"],
    "parsley": ["g", "bunch"],

    # Oils & liquids
    "olive_oil": ["ml", "L", "tbsp"],
    "vegetable_oil": ["ml", "L", "tbsp"],
    "sunflower_oil": ["ml", "L", "tbsp"],
    "soy_sauce": ["ml", "L", "tbsp"],
    "vinegar": ["ml", "L", "tbsp"],
    "lemon_juice": ["ml", "L", "tbsp"],

    # Dairy
    "milk": ["ml", "L"],
    "cream": ["ml", "L"],
    "butter": ["g", "kg"],
    "parmesan": ["g", "kg"],
    "cheddar": ["g", "kg", "slice"],
    "mozzarella": ["g", "kg"],

    # Dry goods
    "rice": ["g", "kg"],
    "spaghetti": ["g", "kg"],
    "pasta": ["g", "kg"],
    "flour": ["g", "kg"],
    "sugar": ["g", "kg"],

    # Vegetables
    "lettuce": ["pcs", "g"],
    "broccoli": ["pcs", "g"]

}

# ==========================================
# LOAD
# ==========================================

with open(ingredients_file, "r", encoding="utf-8") as file:
    ingredients = json.load(file)

# ==========================================
# UPDATE
# ==========================================

updated = 0

for ingredient in ingredients:

    slug = ingredient["slug"]

    if slug in UNIT_FIXES:

        ingredient["allowed_units"] = UNIT_FIXES[slug]

        updated += 1

# ==========================================
# SAVE
# ==========================================

with open(ingredients_file, "w", encoding="utf-8") as file:

    json.dump(
        ingredients,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"✅ Updated {updated} ingredients.")