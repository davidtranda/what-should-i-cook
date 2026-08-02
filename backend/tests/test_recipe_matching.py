import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from services.recipe_service import RecipeService

service = RecipeService()

inventory = [

    "egg",

    "butter",

    "bread",

    "cheddar_cheese"

]

results = service.recommend(inventory)

for recipe in results[:10]:

    print("=" * 60)

    print(f'{recipe["name"]}')
    print(f'Score: {recipe["score"]}%')
    print(f'Can cook: {recipe["can_cook"]}')

    print(
        f'Required: {recipe["required_found"]}/{recipe["required_total"]}'
    )

    print(
        f'Optional: {recipe["optional_found"]}/{recipe["optional_total"]}'
    )

    print(f'Matched: {recipe["matched_ingredients"]}')

    print(f'Missing: {recipe["missing_ingredients"]}')