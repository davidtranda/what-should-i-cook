from services.ingredient_service import IngredientService

service = IngredientService()

print(f"{len(service.get_all())} ingredients loaded!")

print()

results = service.search("egg")

for ingredient in results[:20]:
    print(ingredient["name"])