import json
from pathlib import Path
from re import match


class RecipeService:

    MATCH_EXACT = "exact"
    MATCH_FAMILY = "family"
    MATCH_SUBSTITUTE = "substitute"
    MATCH_MISSING = "missing"

    EXACT_WEIGHT = 1.00
    FAMILY_WEIGHT = 0.95
    SUBSTITUTE_WEIGHT = 0.80
    MISSING_WEIGHT = 0.00

    EXACT_SCORE = 100
    FAMILY_SCORE = 95
    SUBSTITUTE_SCORE = 80
    MISSING_SCORE = 0

    def __init__(self):

        database = Path(__file__).parent.parent / "database"
        recipes_file = database / "recipes.json"

        with open(recipes_file, "r", encoding="utf-8") as file:
            self.recipes = json.load(file)

        database = Path(__file__).parent.parent / "database"

        recipes_file = database / "recipes.json"
        ingredients_file = database / "ingredients.json"

        with open(recipes_file, "r", encoding="utf-8") as file:
            self.recipes = json.load(file)

        with open(ingredients_file, "r", encoding="utf-8") as file:
            self.ingredients = json.load(file)

        self.ingredients_by_slug = {
            ingredient["slug"]: ingredient
            for ingredient in self.ingredients
        }
        ingredients_file = database / "ingredients.json"

        with open(ingredients_file, "r", encoding="utf-8") as file:
            self.ingredients = json.load(file)

        self.ingredients_by_slug = {
            ingredient["slug"]: ingredient
            for ingredient in self.ingredients
        }

    def get_all(self):
        return self.recipes

    def get_by_id(self, recipe_id):

        for recipe in self.recipes:

            if recipe["id"] == recipe_id:
                return recipe

        return None

    def get_by_slug(self, slug):

        for recipe in self.recipes:

            if recipe["slug"] == slug:
                return recipe

        return None

    def match_ingredient(self, recipe_slug, inventory):

        recipe_ingredient = self.ingredients_by_slug.get(recipe_slug)

        if recipe_ingredient is None:

            return {
                "status": self.MATCH_MISSING,

                "recipe_slug": recipe_slug,
                "matched_slug": None,

                "recipe_ingredient": None,
                "inventory_ingredient": None,

                "weight": self.MISSING_WEIGHT,
                "match_score": self.MISSING_SCORE,

                "explanation": "Ingredient not found in database"
            }

        # Exact match
        if recipe_slug in inventory:

            return {
                "status": self.MATCH_EXACT,

                "recipe_slug": recipe_slug,
                "matched_slug": recipe_slug,

                "recipe_ingredient": recipe_ingredient,
                "inventory_ingredient": recipe_ingredient,

                "weight": self.EXACT_WEIGHT,
                "match_score": self.EXACT_SCORE,

                "explanation": "Exact ingredient match"
            }

        recipe_family = recipe_ingredient.get("family")
        recipe_substitutes = recipe_ingredient.get("substitutes", [])

        for inventory_slug in inventory:

            inventory_ingredient = self.ingredients_by_slug.get(inventory_slug)

            if inventory_ingredient is None:
                continue

            # Same family
            if (
                recipe_family
                and recipe_family == inventory_ingredient.get("family")
            ):

                return {
                    "status": self.MATCH_FAMILY,

                    "recipe_slug": recipe_slug,
                    "matched_slug": inventory_slug,

                    "recipe_ingredient": recipe_ingredient,
                    "inventory_ingredient": inventory_ingredient,

                    "weight": self.FAMILY_WEIGHT,
                    "match_score": self.FAMILY_SCORE,

                    "explanation": "Same ingredient family"
                }

            # Substitute
            if inventory_slug in recipe_substitutes:

                return {
                    "status": self.MATCH_SUBSTITUTE,

                    "recipe_slug": recipe_slug,
                    "matched_slug": inventory_slug,

                    "recipe_ingredient": recipe_ingredient,
                    "inventory_ingredient": inventory_ingredient,

                    "weight": self.SUBSTITUTE_WEIGHT,
                    "match_score": self.SUBSTITUTE_SCORE,

                    "explanation": "Ingredient substitution"
                }

        return {
            "status": self.MATCH_MISSING,

            "recipe_slug": recipe_slug,
            "matched_slug": None,

            "recipe_ingredient": recipe_ingredient,
            "inventory_ingredient": None,

            "weight": self.MISSING_WEIGHT,
            "match_score": self.MISSING_SCORE,

            "explanation": "Ingredient missing"
        }

    def recommend(self, inventory):

        results = []

        inventory = set(inventory)

        for recipe in self.recipes:

            required_total = 0
            required_points = 0.0

            optional_total = 0
            optional_points = 0.0

            matched = []
            missing = []
            ingredient_matches = []

            match_breakdown = {
                self.MATCH_EXACT: 0,
                self.MATCH_FAMILY: 0,
                self.MATCH_SUBSTITUTE: 0,
                self.MATCH_MISSING: 0
            }

            for ingredient in recipe["ingredients"]:

                slug = ingredient["slug"]

                importance = ingredient["importance"]

                match = self.match_ingredient(
                    slug,
                    inventory
                )

                ingredient_matches.append(match)

                match_breakdown[match["status"]] += 1

                if ingredient["required"]:

                    required_total += importance

                    if match["status"] != self.MATCH_MISSING:

                        required_points += (
                            importance * match["weight"]
                        )

                        matched.append(match)

                    else:

                        missing.append(match)

                else:

                    optional_total += importance

                    if match["status"] != self.MATCH_MISSING:

                        optional_points += (
                            importance * match["weight"]
                        )

                        matched.append(match)
                
            required_score = (
                required_points / required_total
                if required_total > 0
                else 1
            )

            optional_score = (
                optional_points / optional_total
                if optional_total > 0
                else 1
            )

            score = (
                required_score * 0.8 +
                optional_score * 0.2
            ) * 100

            score = min(score, 100)

            results.append({

                "id": recipe["id"],

                "slug": recipe["slug"],

                "name": recipe["name"],

                "difficulty": recipe["difficulty"],

                "time": recipe["time"],

                "score": round(score),

                "can_cook": len(missing) == 0,

                "required_total": required_total,

                "optional_total": optional_total,

                "required_match_score": round(required_score * 100),

                "optional_match_score": round(optional_score * 100),

                "matched_count": len(matched),

                "ingredient_count": required_total + optional_total,

                "missing_count": len(missing),

                "match_breakdown": match_breakdown,

                "matched_ingredients": matched,

                "missing_ingredients": missing,

                "ingredient_matches": ingredient_matches

            })

        results.sort(
            key=lambda recipe: (
                recipe["can_cook"],
                recipe["score"]
            ),
            reverse=True
        )

        return results