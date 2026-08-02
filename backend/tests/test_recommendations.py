from pathlib import Path
import sys

# ==========================================================
# IMPORTS
# ==========================================================

backend = Path(__file__).parent.parent
sys.path.append(str(backend))

from services.recipe_service import RecipeService

service = RecipeService()

# ==========================================================
# TEST CASES
# ==========================================================

TEST_CASES = {

    "Student": [
        "egg",
        "bread",
        "butter",
        "milk",
        "cheddar_cheese"
    ],

    "Breakfast": [
        "egg",
        "bread",
        "butter",
        "bacon",
        "milk",
        "cheddar_cheese"
    ],

    "Italian Pasta": [
        "penne_pasta",
        "heavy_cream",
        "parmesan",
        "garlic",
        "butter"
    ],

    "Chicken": [
        "chicken_breast",
        "rice",
        "garlic",
        "soy_sauce",
        "onion"
    ],

    "Asian": [
        "rice",
        "soy_sauce",
        "sesame_oil",
        "garlic",
        "ginger",
        "egg"
    ],

    "Vegetarian": [
        "tomato",
        "mozzarella",
        "basil",
        "olive_oil"
    ],

    "Salad": [
        "lettuce",
        "tomato",
        "cucumber",
        "olive_oil",
        "feta_cheese"
    ],

    "Mexican": [
        "tortilla",
        "ground_beef",
        "cheddar_cheese",
        "tomato",
        "lettuce"
    ],

    "Pizza": [
        "pizza_dough",
        "mozzarella",
        "tomato_sauce",
        "pepperoni"
    ],

    "Random Pantry": [
        "egg",
        "rice",
        "tomato",
        "garlic",
        "onion",
        "olive_oil",
        "cheddar_cheese"
    ]
}

# ==========================================================
# RUN ALL TESTS
# ==========================================================

for test_name, inventory in TEST_CASES.items():

    print()
    print("=" * 90)
    print(f"TEST CASE: {test_name}")
    print("=" * 90)

    print()
    print("Inventory:")

    for ingredient in inventory:
        print(f"  • {ingredient}")

    print()

    results = service.recommend(inventory)

    print("-" * 90)
    print("TOP 5 RECOMMENDATIONS")
    print("-" * 90)

    for index, recipe in enumerate(results[:5], start=1):

        print()

        print(
            f"{index}. {recipe['name']}"
        )

        print(f"Score: {recipe['score']}%")

        print(
            f"Can cook: {'YES' if recipe['can_cook'] else 'NO'}"
        )

        print(
            f"Missing ingredients: {recipe['missing_count']}"
        )

        print(
            f"Required score: {recipe['required_match_score']}%"
        )

        print(
            f"Optional score: {recipe['optional_match_score']}%"
        )

        print()

        print("Match breakdown:")

        for match_type, count in recipe["match_breakdown"].items():

            print(f"  {match_type}: {count}")

        print()

        print("Matched ingredients:")

        if recipe["matched_ingredients"]:

            for ingredient in recipe["matched_ingredients"]:

                print(
                    f"  ✔ {ingredient['recipe_slug']} "
                    f"({ingredient['status']})"
                )

        else:

            print("  None")

        print()

        print("Missing ingredients:")

        if recipe["missing_ingredients"]:

            for ingredient in recipe["missing_ingredients"]:

                print(
                    f"  ✖ {ingredient['recipe_slug']}"
                )

        else:

            print("  None")

        print()

    print("=" * 90)