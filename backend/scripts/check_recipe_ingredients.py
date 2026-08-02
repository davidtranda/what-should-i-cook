import json
import difflib
from pathlib import Path

# ==========================================
# FILE PATHS
# ==========================================

database = Path(__file__).parent.parent / "database"

ingredients_file = database / "ingredients.json"
recipes_file = database / "recipes.json"
category_rules_file = database / "category_rules.json"

# ==========================================
# LOAD INGREDIENTS
# ==========================================

with open(ingredients_file, "r", encoding="utf-8") as file:
    ingredients = json.load(file)

with open(category_rules_file, "r", encoding="utf-8") as file:
    category_rules = json.load(file)

ingredient_slugs = set()
ingredient_units = {}

for ingredient in ingredients:

    slug = ingredient["slug"]

    ingredient_slugs.add(slug)

    # Override dacă există
    if ingredient["allowed_units"]:

        ingredient_units[slug] = ingredient["allowed_units"]

    # Altfel folosim regula categoriei
    else:

        category = ingredient["category"]

        ingredient_units[slug] = category_rules[category]["allowed_units"]

# ==========================================
# LOAD RECIPES
# ==========================================

with open(recipes_file, "r", encoding="utf-8") as file:
    recipes = json.load(file)

# ==========================================
# VALIDATION
# ==========================================

errors = 0

recipe_ids = set()
recipe_slugs = set()

for recipe in recipes:

    recipe_name = recipe["name"]

    # -------------------------
    # Duplicate recipe ID
    # -------------------------

    if recipe["id"] in recipe_ids:

        print(f"\n❌ Duplicate recipe id: {recipe['id']}")

        errors += 1

    recipe_ids.add(recipe["id"])

    # -------------------------
    # Duplicate recipe slug
    # -------------------------

    if recipe["slug"] in recipe_slugs:

        print(f"\n❌ Duplicate recipe slug: {recipe['slug']}")

        errors += 1

    recipe_slugs.add(recipe["slug"])

    # -------------------------
    # At least one required ingredient
    # -------------------------

    required_found = False

    # -------------------------
    # Ingredients
    # -------------------------

    for ingredient in recipe["ingredients"]:

        slug = ingredient["slug"]

        quantity = ingredient["quantity"]

        unit = ingredient["unit"]

        required = ingredient["required"]

        # -------------------------
        # Ingredient exists
        # -------------------------

        if slug not in ingredient_slugs:

            print(f"\n❌ {recipe_name}")
            print(f"Missing ingredient: '{slug}'")

            suggestions = difflib.get_close_matches(
                slug,
                ingredient_slugs,
                n=3,
                cutoff=0.5
            )

            if suggestions:

                print("Did you mean:")

                for suggestion in suggestions:

                    print(f"   • {suggestion}")

            errors += 1

            continue

        # -------------------------
        # Allowed unit
        # -------------------------

        if unit not in ingredient_units[slug]:

            print(f"\n❌ {recipe_name}")

            print(
                f"Ingredient '{slug}' does not allow unit '{unit}'."
            )

            print(
                "Allowed units:",
                ", ".join(ingredient_units[slug])
            )

            errors += 1

        # -------------------------
        # Quantity
        # -------------------------

        if quantity <= 0:

            print(
                f"\n❌ {recipe_name}: '{slug}' has invalid quantity."
            )

            errors += 1

        # -------------------------
        # Required must be boolean
        # -------------------------

        if not isinstance(required, bool):

            print(
                f"\n❌ {recipe_name}: '{slug}' required must be true or false."
            )

            errors += 1

        if required:

            required_found = True

    # -------------------------
    # Recipe has required ingredient
    # -------------------------

    if not required_found:

        print(
            f"\n❌ {recipe_name}: no required ingredients."
        )

        errors += 1

# ==========================================
# RESULT
# ==========================================

print("\n=========================================")

if errors == 0:

    print("✅ Recipe database is valid!")

    print(f"Recipes checked : {len(recipes)}")

    print(f"Ingredients     : {len(ingredients)}")

else:

    print(f"❌ Found {errors} error(s).")

print("=========================================")