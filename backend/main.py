from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

from services.ingredient_service import IngredientService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ingredient_service = IngredientService()


@app.get("/")
def root():
    return {
        "message": "What Should I Cook API is running!"
    }


@app.get("/ingredients")
def get_ingredients():
    return ingredient_service.get_all()


@app.get("/ingredients/search")
def search_ingredients(q: str = Query("")):

    return ingredient_service.search(q)

from services.recipe_service import RecipeService
recipe_service = RecipeService()

@app.get("/recipes")
def get_recipes():

    return recipe_service.get_all()

@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):

    return recipe_service.get_by_id(recipe_id)

from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    inventory: list[str]


@app.post("/recipes/recommend")
def recommend_recipes(request: RecommendationRequest):

    recommendations = recipe_service.recommend(
        request.inventory
    )

    return recommendations