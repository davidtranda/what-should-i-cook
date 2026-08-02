import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

database = Path(__file__).parent.parent / "database"
ingredients_file = database / "ingredients.json"


def slugify(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def resolve_family(ingredient):
    slug = ingredient.get("slug", "")
    name = ingredient.get("name", "")
    aliases = ingredient.get("aliases", [])
    haystack = " ".join([slug, name, *aliases]).lower()

    if "tomato" in haystack or "tomatoes" in haystack or "tomatos" in haystack:
        return "tomato"
    if "cheese" in haystack or "cheddar" in haystack or "mozzarella" in haystack or "parmesan" in haystack or "feta" in haystack or "gouda" in haystack or "bryndza" in haystack or "emmentaler" in haystack or "stilton" in haystack or "swiss" in haystack or "cottage" in haystack:
        return "cheese"
    if "onion" in haystack or "shallot" in haystack or "scallion" in haystack:
        return "onion"
    if "garlic" in haystack:
        return "garlic"
    if "egg" in haystack:
        return "egg"
    if "butter" in haystack:
        return "butter"
    if "milk" in haystack:
        return "milk"
    if "bread" in haystack or "bun" in haystack or "baguette" in haystack or "toast" in haystack:
        return "bread"
    if "pasta" in haystack or "spaghetti" in haystack or "penne" in haystack or "fusilli" in haystack or "macaroni" in haystack or "farfalle" in haystack or "linguine" in haystack or "tagliatelle" in haystack:
        return "pasta"
    if "rice" in haystack:
        return "rice"
    if "chicken" in haystack:
        return "chicken"
    if "beef" in haystack:
        return "beef"
    if "fish" in haystack or "salmon" in haystack or "tuna" in haystack or "cod" in haystack or "anchovy" in haystack or "sardine" in haystack:
        return "fish"
    if "lettuce" in haystack or "romaine" in haystack or "iceberg" in haystack:
        return "lettuce"
    if "pepper" in haystack:
        return "pepper"
    if "potato" in haystack:
        return "potato"
    if "mushroom" in haystack:
        return "mushroom"
    if "carrot" in haystack:
        return "carrot"
    if "cucumber" in haystack:
        return "cucumber"
    if "spinach" in haystack:
        return "spinach"

    return ingredient.get("family") or ingredient.get("slug")


with open(ingredients_file, "r", encoding="utf-8") as file:
    ingredients = json.load(file)


family_groups = defaultdict(list)
category_groups = defaultdict(list)
for ingredient in ingredients:
    family = ingredient.get("family") or ingredient.get("slug")
    family_groups[family].append(ingredient["slug"])
    category_groups[ingredient.get("category", "other")].append(ingredient["slug"])


for ingredient in ingredients:
    ingredient["slug"] = slugify(ingredient["name"])

    if not ingredient.get("aliases"):
        ingredient["aliases"] = [ingredient["name"].lower()]

    ingredient["family"] = resolve_family(ingredient)

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

with open(ingredients_file, "w", encoding="utf-8") as file:
    json.dump(ingredients, file, indent=4, ensure_ascii=False)

print(f"Prepared {len(ingredients)} ingredients.")
