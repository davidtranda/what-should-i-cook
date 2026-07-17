import json
from pathlib import Path

DATABASE = Path(__file__).parent.parent / "database"

INGREDIENTS_FILE = DATABASE / "ingredients.json"
CATEGORY_FILE = DATABASE / "category_rules.json"
UNIT_FILE = DATABASE / "unit_rules.json"


with open(INGREDIENTS_FILE, encoding="utf-8") as f:
    ingredients = json.load(f)

with open(CATEGORY_FILE, encoding="utf-8") as f:
    category_rules = json.load(f)

with open(UNIT_FILE, encoding="utf-8") as f:
    unit_rules = json.load(f)

def find_category(name):

    for category, keywords in category_rules.items():

        for keyword in keywords:

            if keyword in name:

                return category

    return "other"

def find_units(name):

    for rule, keywords in unit_rules.items():

        for keyword in keywords:

            if keyword in name:

                if rule == "pcs":
                    return ["pcs"]

                if rule == "ml_l":
                    return ["ml", "L"]

                if rule == "g_kg":
                    return ["g", "kg"]

                if rule == "pcs_g_kg":
                    return ["pcs", "g", "kg"]

    return ["pcs"]

for ingredient in ingredients:

    name = ingredient["name"].lower()

    ingredient["category"] = find_category(name)

    ingredient["allowed_units"] = find_units(name)

with open(
    INGREDIENTS_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        ingredients,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Updated {len(ingredients)} ingredients.")