import json
from pathlib import Path

database = Path(__file__).parent.parent / "database"
ingredients_file = database / "ingredients.json"

with open(ingredients_file, "r", encoding="utf-8") as file:
    ingredients = json.load(file)

slugs = sorted(
    ingredient["slug"]
    for ingredient in ingredients
)

output_file = Path(__file__).parent / "ingredient_slugs.txt"

with open(output_file, "w", encoding="utf-8") as file:

    file.write("=" * 50 + "\n")
    file.write("INGREDIENT SLUGS\n")
    file.write("=" * 50 + "\n\n")

    for slug in slugs:
        file.write(f"{slug}\n")

print(f"✅ Exported {len(slugs)} ingredient slugs.")
print(f"📄 File created: {output_file}")