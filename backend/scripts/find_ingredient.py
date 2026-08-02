import json
from pathlib import Path

database = Path(__file__).parent.parent / "database"

with open(database / "ingredients.json", "r", encoding="utf-8") as f:
    ingredients = json.load(f)

while True:

    query = input("\nIngredient (or 'exit'): ").strip().lower()

    if query == "exit":
        break

    found = False

    for ingredient in ingredients:

        if query in ingredient["slug"] or query in ingredient["name"].lower():

            print("-" * 60)
            print("Slug     :", ingredient["slug"])
            print("Name     :", ingredient["name"])
            print("Category :", ingredient["category"])
            print("Units    :", ingredient["allowed_units"])

            found = True

    if not found:
        print("No matches.")