import json
from pathlib import Path

import requests

API_URL = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"

print("Downloading ingredients...")

response = requests.get(API_URL)
response.raise_for_status()

data = response.json()

ingredients = []

for ingredient in data["meals"]:

    name = ingredient["strIngredient"]

    if not name:
        continue

    ingredients.append(
        {
            "id": int(ingredient["idIngredient"]),
            "name": name.strip(),
            "category": 0,
            "default_unit": "",
            "emoji": "",
            "aliases": [],
            "common": False
        }
    )

# eliminare duplicate
unique = {}

for ingredient in ingredients:
    unique[ingredient["name"].lower()] = ingredient

ingredients = list(unique.values())

# sortare alfabetică
ingredients.sort(key=lambda ingredient: ingredient["name"])

database_folder = Path("database")
database_folder.mkdir(exist_ok=True)

ingredients_file = database_folder / "ingredients.json"

with open(ingredients_file, "w", encoding="utf-8") as file:
    json.dump(
        ingredients,
        file,
        indent=4,
        ensure_ascii=False
    )

print()
print(f"Saved {len(ingredients)} ingredients!")
print(f"File created: {ingredients_file}")