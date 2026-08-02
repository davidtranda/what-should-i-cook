import json
from collections import defaultdict
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BACKEND_DIR / "database"
INGREDIENTS_FILE = DATABASE_DIR / "ingredients.json"


with open(INGREDIENTS_FILE, "r", encoding="utf-8") as file:
    ingredients = json.load(file)


family_groups = defaultdict(list)
category_groups = defaultdict(list)

for ingredient in ingredients:
    family = ingredient.get("family") or ingredient.get("slug")
    family_groups[family].append(ingredient["slug"])
    category_groups[ingredient.get("category", "other")].append(ingredient["slug"])


updated = 0

for ingredient in ingredients:
    family = ingredient.get("family") or ingredient.get("slug")
    category = ingredient.get("category", "other")

    substitutes = [
        slug
        for slug in family_groups.get(family, [])
        if slug != ingredient["slug"]
    ]

    if not substitutes:
        substitutes = [
            slug
            for slug in category_groups.get(category, [])
            if slug != ingredient["slug"]
        ][:5]

    ingredient["substitutes"] = substitutes
    updated += 1


with open(INGREDIENTS_FILE, "w", encoding="utf-8") as file:
    json.dump(
        ingredients,
        file,
        indent=4,
        ensure_ascii=False
    )


print(f"\nUpdated {updated} ingredients with family/category-based substitutes.")