#VERIFICA FOARTE DETALIAT CA TOT DATABASE-UL ESTE VALID, NU DOAR STRUCTURA JSON, CI SI LOGICA DIN SPATE, DE EXEMPLU: NU EXISTA SLUG DUPLICAT, NU EXISTA ID DUPLICAT, TOATE SLUG-URILE DIN RETETE EXISTĂ IN INGREDIENTE, TOATE CAMPOURILE OBLIGATORII SUNT PREZENTE, TOATE VALORILE SUNT VALIDE (DE EXEMPLU NU EXISTA TIMP NEGATIV SAU CANTITATI NEGATIVE), ETC.

import json
from pathlib import Path

# ==========================================================
# LOAD DATABASE
# ==========================================================

database = Path(__file__).parent.parent / "database"

with open(database / "ingredients.json", "r", encoding="utf-8") as file:
    ingredients = json.load(file)

with open(database / "recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

errors = 0
warnings = 0

def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# ==========================================================
# DUPLICATE INGREDIENT SLUGS
# ==========================================================

section("Duplicate ingredient slugs")

slugs = set()

duplicate_found = False

for ingredient in ingredients:

    slug = ingredient["slug"]

    if slug in slugs:

        print(f"❌ {slug}")

        duplicate_found = True
        errors += 1

    else:

        slugs.add(slug)

if not duplicate_found:

    print("✔ None")


# ==========================================================
# DUPLICATE INGREDIENT NAMES
# ==========================================================

section("Duplicate ingredient names")

names = set()

duplicate_found = False

for ingredient in ingredients:

    name = ingredient["name"].strip().lower()

    if name in names:

        print(f"❌ {ingredient['name']}")

        duplicate_found = True
        errors += 1

    else:

        names.add(name)

if not duplicate_found:

    print("✔ None")


# ==========================================================
# MISSING CATEGORIES
# ==========================================================

section("Missing categories")

missing_found = False

for ingredient in ingredients:

    if not ingredient.get("category"):

        print(f"❌ {ingredient['slug']}")

        missing_found = True
        errors += 1

if not missing_found:

    print("✔ None")


# ==========================================================
# MISSING ALLOWED UNITS
# ==========================================================

section("Missing allowed units")

missing_found = False

for ingredient in ingredients:

    if not ingredient.get("allowed_units"):

        print(f"❌ {ingredient['slug']}")

        missing_found = True
        errors += 1

if not missing_found:

    print("✔ None")


# ==========================================================
# DUPLICATE RECIPE IDS
# ==========================================================

section("Duplicate recipe ids")

ids = set()

duplicate_found = False

for recipe in recipes:

    if recipe["id"] in ids:

        print(f"❌ {recipe['id']}")

        duplicate_found = True
        errors += 1

    else:

        ids.add(recipe["id"])

if not duplicate_found:

    print("✔ None")


# ==========================================================
# DUPLICATE RECIPE SLUGS
# ==========================================================

section("Duplicate recipe slugs")

slugs = set()

duplicate_found = False

for recipe in recipes:

    slug = recipe["slug"]

    if slug in slugs:

        print(f"❌ {slug}")

        duplicate_found = True
        errors += 1

    else:

        slugs.add(slug)

if not duplicate_found:

    print("✔ None")


# ==========================================================
# DUPLICATE INGREDIENTS INSIDE RECIPES
# ==========================================================

section("Duplicate ingredients inside recipes")

duplicate_found = False

for recipe in recipes:

    used = set()

    for ingredient in recipe["ingredients"]:

        slug = ingredient["slug"]

        if slug in used:

            print(f"❌ {recipe['name']} -> {slug}")

            duplicate_found = True
            errors += 1

        else:

            used.add(slug)

if not duplicate_found:

    print("✔ None")


# ==========================================================
# EMPTY RECIPES
# ==========================================================

section("Empty recipes")

empty_found = False

for recipe in recipes:

    if len(recipe["ingredients"]) == 0:

        print(f"❌ {recipe['name']}")

        empty_found = True
        errors += 1

if not empty_found:

    print("✔ None")

# ==========================================================
# RECIPE INGREDIENTS EXIST
# ==========================================================

section("Recipe ingredients exist")

ingredient_slugs = {
    ingredient["slug"]
    for ingredient in ingredients
}

missing_found = False

for recipe in recipes:

    for ingredient in recipe["ingredients"]:

        slug = ingredient["slug"]

        if slug not in ingredient_slugs:

            print(f"❌ {recipe['name']} -> {slug}")

            missing_found = True
            errors += 1

if not missing_found:

    print("✔ None")

# ==========================================================
# REQUIRED FIELDS
# ==========================================================

section("Required fields")

ingredient_required = [
    "id",
    "slug",
    "name",
    "category",
    "allowed_units"
]

recipe_required = [
    "id",
    "slug",
    "name",
    "ingredients",
    "difficulty",
    "time"
]

missing_found = False

for ingredient in ingredients:

    for field in ingredient_required:

        if field not in ingredient:

            print(
                f"❌ Ingredient '{ingredient.get('slug', '?')}' "
                f"missing '{field}'"
            )

            missing_found = True
            errors += 1


for recipe in recipes:

    for field in recipe_required:

        if field not in recipe:

            print(
                f"❌ Recipe '{recipe.get('name', '?')}' "
                f"missing '{field}'"
            )

            missing_found = True
            errors += 1


if not missing_found:

    print("✔ None")

# ==========================================================
# INVALID VALUES
# ==========================================================

section("Invalid values")

valid_difficulties = {
    "easy",
    "medium",
    "hard"
}

invalid_found = False

for recipe in recipes:

    if recipe["difficulty"] not in valid_difficulties:

        print(
            f"❌ {recipe['name']} "
            f"invalid difficulty '{recipe['difficulty']}'"
        )

        invalid_found = True
        errors += 1

    if recipe["time"] <= 0:

        print(
            f"❌ {recipe['name']} "
            f"invalid cooking time ({recipe['time']})"
        )

        invalid_found = True
        errors += 1


for recipe in recipes:

    for ingredient in recipe["ingredients"]:

        if ingredient["quantity"] <= 0:

            print(
                f"❌ {recipe['name']} -> "
                f"{ingredient['slug']} "
                f"invalid quantity ({ingredient['quantity']})"
            )

            invalid_found = True
            errors += 1


if not invalid_found:

    print("✔ None")

# ==========================================================
# UNUSED INGREDIENTS
# ==========================================================

section("Unused ingredients")

used = set()

for recipe in recipes:

    for ingredient in recipe["ingredients"]:

        used.add(ingredient["slug"])

unused = []

for ingredient in ingredients:

    if ingredient["slug"] not in used:

        unused.append(ingredient["slug"])

unused.sort()

print(f"{len(unused)} unused ingredients")

for slug in unused:

    print(f"• {slug}")

# ==========================================================
# CONSECUTIVE RECIPE IDS
# ==========================================================

section("Consecutive recipe ids")

recipe_ids = sorted(
    recipe["id"]
    for recipe in recipes
)

missing_ids = []

if recipe_ids:

    first = recipe_ids[0]
    last = recipe_ids[-1]

    expected = set(range(first, last + 1))
    existing = set(recipe_ids)

    missing_ids = sorted(expected - existing)

if missing_ids:

    for recipe_id in missing_ids:

        print(f"⚠ Missing recipe id: {recipe_id}")

        warnings += 1

else:

    print("✔ None")

# ==========================================================
# CONSECUTIVE INGREDIENT IDS
# ==========================================================

section("Consecutive ingredient ids")

ingredient_ids = sorted(
    ingredient["id"]
    for ingredient in ingredients
)

missing_ids = []

if ingredient_ids:

    first = ingredient_ids[0]
    last = ingredient_ids[-1]

    expected = set(range(first, last + 1))
    existing = set(ingredient_ids)

    missing_ids = sorted(expected - existing)

if missing_ids:

    for ingredient_id in missing_ids:

        print(f"⚠ Missing ingredient id: {ingredient_id}")

        warnings += 1

else:

    print("✔ None")

# ==========================================================
# INGREDIENT IMPORTANCE
# ==========================================================

section("Ingredient importance")

importance_errors = False

for recipe in recipes:

    for ingredient in recipe["ingredients"]:

        slug = ingredient["slug"]

        if "importance" not in ingredient:

            print(
                f"❌ {recipe['slug']} -> {slug}: missing importance"
            )

            importance_errors = True
            errors += 1

            continue

        importance = ingredient["importance"]

        if not isinstance(importance, int):

            print(
                f"❌ {recipe['slug']} -> {slug}: importance must be an integer"
            )

            importance_errors = True
            errors += 1

            continue

        if importance < 1 or importance > 10:

            print(
                f"❌ {recipe['slug']} -> {slug}: invalid importance ({importance})"
            )

            importance_errors = True
            errors += 1

if not importance_errors:

    print("✔ All ingredient importance values are valid")

# ==========================================================
# FINAL REPORT
# ==========================================================

print()
print("=" * 60)
print("DATABASE AUDIT")
print("=" * 60)

print(f"Errors:   {errors}")
print(f"Warnings: {warnings}")

print()

if errors == 0:

    print("✅ DATABASE HEALTH: PASS")

else:

    print("❌ DATABASE HEALTH: FAIL")

print("=" * 60)