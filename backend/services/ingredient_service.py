import json
from pathlib import Path


class IngredientService:

    def __init__(self):

        database = Path(__file__).parent.parent / "database"
        ingredients_file = database / "ingredients.json"

        with open(ingredients_file, "r", encoding="utf-8") as file:
            self.ingredients = json.load(file)

    def get_all(self):
        return self.ingredients

    def get_by_id(self, ingredient_id):

        for ingredient in self.ingredients:

            if ingredient["id"] == ingredient_id:
                return ingredient

        return None

    def search(self, query: str):

        query = query.lower()

        results = []

        for ingredient in self.ingredients:

            if query in ingredient["name"].lower():
                results.append(ingredient)

        return results[:20]