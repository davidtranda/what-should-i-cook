from services.ingredient_service import IngredientService
from flask import request, jsonify
from services.recipe_service import RecipeService

recipe_service = RecipeService()
service = IngredientService()

print(f"{len(service.get_all())} ingredients loaded!")

print()

results = service.search("egg")

for ingredient in results[:20]:
    print(ingredient["name"])

@app.post("/recipes/recommend")
def recommend_recipes():

    data = request.get_json()

    inventory = data.get("inventory", [])

    recommendations = recipe_service.recommend(inventory)

    return jsonify(recommendations)