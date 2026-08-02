import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "database"
INGREDIENTS_FILE = DATABASE / "ingredients.json"
ASSIGN_SCRIPT = ROOT / "scripts" / "assign_families.py"
PREPARE_SCRIPT = ROOT / "scripts" / "prepare_ingredients.py"

FAMILIES = {
    "onion": [
        "onion",
        "red_onion",
        "white_onion",
        "shallot",
        "shallots",
        "spring_onion",
        "green_onion",
        "scallion",
        "spring_onions",
    ],
    "garlic": ["garlic"],
    "egg": ["egg", "eggs"],
    "butter": ["butter", "salted_butter", "unsalted_butter"],
    "milk": ["milk", "whole_milk", "semi_skimmed_milk", "skimmed_milk"],
    "cheese": [
        "cheese",
        "cheddar_cheese",
        "mozzarella",
        "parmesan",
        "cubed_feta_cheese",
        "feta_cheese",
        "gouda_cheese",
        "cream_cheese",
        "bryndza_cheese",
        "cottage_cheese",
        "goats_cheese",
        "emmentaler_cheese",
        "farmers_cheese",
        "liquid_cheese",
        "monterey_jack_cheese",
        "panquehue_cheese",
        "shredded_mexican_cheese",
        "stilton_cheese",
        "swiss_cheese",
        "cheese_curds",
    ],
    "bread": ["bread", "burger_buns", "baguette", "toast_bread", "toast", "bread_rolls"],
    "pasta": [
        "spaghetti",
        "penne_pasta",
        "fusilli",
        "macaroni",
        "farfalle",
        "linguine_pasta",
        "tagliatelle",
        "bowtie_pasta",
    ],
    "rice": ["rice", "basmati_rice", "brown_rice", "arabic_rice"],
    "chicken": ["chicken", "chicken_breast", "chicken_legs"],
    "beef": ["beef", "ground_beef", "beef_steak"],
    "fish": ["salmon", "tuna", "cod", "anchovy_fillet", "anchovy"],
    "lettuce": ["lettuce", "romaine_lettuce", "iceberg_lettuce", "baby_lettuce_leaves"],
    "tomato": [
        "tomato",
        "tomato_sauce",
        "tomato_puree",
        "tomato_ketchup",
        "cherry_tomatoes",
        "baby_plum_tomatoes",
        "beef_tomatoes",
        "canned_tomatoes",
        "chopped_tomatoes",
        "diced_tomatoes",
        "grape_tomatoes",
        "plum_tomatoes",
        "sun_dried_tomatoes",
        "tinned_tomatos",
        "vine_tomatoes",
    ],
    "pepper": [
        "bell_pepper",
        "red_bell_pepper",
        "green_bell_pepper",
        "yellow_bell_pepper",
        "banana_pepper",
        "pepper",
        "black_pepper",
    ],
    "potato": ["potato", "potatoes", "baby_new_potatoes", "new_potatoes"],
    "mushroom": ["mushroom", "button_mushroom", "chestnut_mushroom", "shiitake_mushroom"],
    "carrot": ["carrot", "carrots"],
    "cucumber": ["cucumber", "cucumbers"],
    "spinach": ["spinach"],
}

KEYWORDS = {
    "tomato": ["tomato", "tomatoes", "tomatos"],
    "cheese": ["cheese", "cheddar", "mozzarella", "parmesan", "feta", "gouda", "bryndza", "emmentaler", "stilton", "swiss", "cottage"],
    "onion": ["onion", "shallot", "shallots", "scallion", "spring onion", "green onion"],
    "garlic": ["garlic"],
    "egg": ["egg"],
    "butter": ["butter"],
    "milk": ["milk"],
    "bread": ["bread", "bun", "buns", "baguette", "toast"],
    "pasta": ["pasta", "spaghetti", "penne", "fusilli", "macaroni", "farfalle", "linguine", "tagliatelle"],
    "rice": ["rice"],
    "chicken": ["chicken"],
    "beef": ["beef"],
    "fish": ["fish", "salmon", "tuna", "cod", "anchovy", "sardine"],
    "lettuce": ["lettuce", "romaine", "iceberg"],
    "pepper": ["pepper"],
    "potato": ["potato", "potatoes"],
    "mushroom": ["mushroom"],
    "carrot": ["carrot", "carrots"],
    "cucumber": ["cucumber"],
    "spinach": ["spinach"],
}


def resolve_family(ingredient):
    slug = ingredient.get("slug", "")
    name = ingredient.get("name", "")
    aliases = ingredient.get("aliases", [])
    haystack = " ".join([slug, name, *aliases]).lower()

    for family, members in FAMILIES.items():
        if slug in members:
            return family

    for family, keywords in KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            return family

    return ingredient.get("family") or slug


with INGREDIENTS_FILE.open("r", encoding="utf-8") as handle:
    ingredients = json.load(handle)

updated = 0
for ingredient in ingredients:
    old_family = ingredient.get("family")
    new_family = resolve_family(ingredient)
    ingredient["family"] = new_family
    if old_family != new_family:
        updated += 1

family_groups = defaultdict(list)
category_groups = defaultdict(list)
for ingredient in ingredients:
    family = ingredient.get("family") or ingredient.get("slug")
    family_groups[family].append(ingredient["slug"])
    category_groups[ingredient.get("category", "other")].append(ingredient["slug"])

for ingredient in ingredients:
    family = ingredient.get("family") or ingredient.get("slug")
    category = ingredient.get("category", "other")
    substitutes = [slug for slug in family_groups.get(family, []) if slug != ingredient["slug"]]
    if not substitutes:
        substitutes = [slug for slug in category_groups.get(category, []) if slug != ingredient["slug"]][:5]
    ingredient["substitutes"] = substitutes

with INGREDIENTS_FILE.open("w", encoding="utf-8") as handle:
    json.dump(ingredients, handle, indent=4, ensure_ascii=False)

ASSIGN_SCRIPT.write_text("""from pathlib import Path
import json

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BACKEND_DIR / \"database\"
INGREDIENTS_FILE = DATABASE_DIR / \"ingredients.json\"

FAMILIES = {
    \"onion\": [
        \"onion\",
        \"red_onion\",
        \"white_onion\",
        \"shallot\",
        \"shallots\",
        \"spring_onion\",
        \"green_onion\",
        \"scallion\",
        \"spring_onions\",
    ],
    \"garlic\": [\"garlic\"],
    \"egg\": [\"egg\", \"eggs\"],
    \"butter\": [\"butter\", \"salted_butter\", \"unsalted_butter\"],
    \"milk\": [\"milk\", \"whole_milk\", \"semi_skimmed_milk\", \"skimmed_milk\"],
    \"cheese\": [
        \"cheese\",
        \"cheddar_cheese\",
        \"mozzarella\",
        \"parmesan\",
        \"cubed_feta_cheese\",
        \"feta_cheese\",
        \"gouda_cheese\",
        \"cream_cheese\",
        \"bryndza_cheese\",
        \"cottage_cheese\",
        \"goats_cheese\",
        \"emmentaler_cheese\",
        \"farmers_cheese\",
        \"liquid_cheese\",
        \"monterey_jack_cheese\",
        \"panquehue_cheese\",
        \"shredded_mexican_cheese\",
        \"stilton_cheese\",
        \"swiss_cheese\",
        \"cheese_curds\",
    ],
    \"bread\": [\"bread\", \"burger_buns\", \"baguette\", \"toast_bread\", \"toast\", \"bread_rolls\"],
    \"pasta\": [
        \"spaghetti\",
        \"penne_pasta\",
        \"fusilli\",
        \"macaroni\",
        \"farfalle\",
        \"linguine_pasta\",
        \"tagliatelle\",
        \"bowtie_pasta\",
    ],
    \"rice\": [\"rice\", \"basmati_rice\", \"brown_rice\", \"arabic_rice\"],
    \"chicken\": [\"chicken\", \"chicken_breast\", \"chicken_legs\"],
    \"beef\": [\"beef\", \"ground_beef\", \"beef_steak\"],
    \"fish\": [\"salmon\", \"tuna\", \"cod\", \"anchovy_fillet\", \"anchovy\"],
    \"lettuce\": [\"lettuce\", \"romaine_lettuce\", \"iceberg_lettuce\", \"baby_lettuce_leaves\"],
    \"tomato\": [
        \"tomato\",
        \"tomato_sauce\",
        \"tomato_puree\",
        \"tomato_ketchup\",
        \"cherry_tomatoes\",
        \"baby_plum_tomatoes\",
        \"beef_tomatoes\",
        \"canned_tomatoes\",
        \"chopped_tomatoes\",
        \"diced_tomatoes\",
        \"grape_tomatoes\",
        \"plum_tomatoes\",
        \"sun_dried_tomatoes\",
        \"tinned_tomatos\",
        \"vine_tomatoes\",
    ],
    \"pepper\": [
        \"bell_pepper\",
        \"red_bell_pepper\",
        \"green_bell_pepper\",
        \"yellow_bell_pepper\",
        \"banana_pepper\",
        \"pepper\",
        \"black_pepper\",
    ],
    \"potato\": [\"potato\", \"potatoes\", \"baby_new_potatoes\", \"new_potatoes\"],
    \"mushroom\": [\"mushroom\", \"button_mushroom\", \"chestnut_mushroom\", \"shiitake_mushroom\"],
    \"carrot\": [\"carrot\", \"carrots\"],
    \"cucumber\": [\"cucumber\", \"cucumbers\"],
    \"spinach\": [\"spinach\"],
}

FAMILY_KEYWORDS = {
    \"tomato\": [\"tomato\", \"tomatoes\", \"tomatos\"],
    \"cheese\": [\"cheese\", \"cheddar\", \"mozzarella\", \"parmesan\", \"feta\", \"gouda\", \"bryndza\", \"emmentaler\", \"stilton\", \"swiss\", \"cottage\"],
    \"onion\": [\"onion\", \"shallot\", \"shallots\", \"scallion\", \"spring onion\", \"green onion\"],
    \"garlic\": [\"garlic\"],
    \"egg\": [\"egg\"],
    \"butter\": [\"butter\"],
    \"milk\": [\"milk\"],
    \"bread\": [\"bread\", \"bun\", \"buns\", \"baguette\", \"toast\"],
    \"pasta\": [\"pasta\", \"spaghetti\", \"penne\", \"fusilli\", \"macaroni\", \"farfalle\", \"linguine\", \"tagliatelle\"],
    \"rice\": [\"rice\"],
    \"chicken\": [\"chicken\"],
    \"beef\": [\"beef\"],
    \"fish\": [\"fish\", \"salmon\", \"tuna\", \"cod\", \"anchovy\", \"sardine\"],
    \"lettuce\": [\"lettuce\", \"romaine\", \"iceberg\"],
    \"pepper\": [\"pepper\"],
    \"potato\": [\"potato\", \"potatoes\"],
    \"mushroom\": [\"mushroom\"],
    \"carrot\": [\"carrot\", \"carrots\"],
    \"cucumber\": [\"cucumber\"],
    \"spinach\": [\"spinach\"],
}


def resolve_family(ingredient):
    slug = ingredient.get(\"slug\", \"\")
    name = ingredient.get(\"name\", \"\")
    aliases = ingredient.get(\"aliases\", [])
    haystack = \" \".join([slug, name, *aliases]).lower()

    for family, members in FAMILIES.items():
        if slug in members:
            return family

    for family, keywords in FAMILY_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            return family

    return ingredient.get(\"family\") or slug


with open(INGREDIENTS_FILE, \"r\", encoding=\"utf-8\") as file:
    ingredients = json.load(file)

updated = 0

for ingredient in ingredients:
    previous_family = ingredient.get(\"family\")
    new_family = resolve_family(ingredient)
    ingredient[\"family\"] = new_family

    if previous_family != new_family:
        updated += 1

with open(INGREDIENTS_FILE, \"w\", encoding=\"utf-8\") as file:
    json.dump(ingredients, file, indent=4, ensure_ascii=False)

print(f\"\\nUpdated {updated} ingredients.\")
""")

PREPARE_SCRIPT.write_text("""import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

database = Path(__file__).parent.parent / \"database\"
ingredients_file = database / \"ingredients.json\"


def slugify(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize(\"NFKD\", text)
    text = text.encode(\"ascii\", \"ignore\").decode(\"ascii\")
    text = re.sub(r\"[^a-z0-9]+\", \"_\", text)
    text = re.sub(r\"_+\", \"_\", text)
    return text.strip(\"_\")


def resolve_family(ingredient):
    slug = ingredient.get(\"slug\", \"\")
    name = ingredient.get(\"name\", \"\")
    aliases = ingredient.get(\"aliases\", [])
    haystack = \" \".join([slug, name, *aliases]).lower()

    if \"tomato\" in haystack or \"tomatoes\" in haystack or \"tomatos\" in haystack:
        return \"tomato\"
    if \"cheese\" in haystack or \"cheddar\" in haystack or \"mozzarella\" in haystack or \"parmesan\" in haystack or \"feta\" in haystack or \"gouda\" in haystack or \"bryndza\" in haystack or \"emmentaler\" in haystack or \"stilton\" in haystack or \"swiss\" in haystack or \"cottage\" in haystack:
        return \"cheese\"
    if \"onion\" in haystack or \"shallot\" in haystack or \"scallion\" in haystack:
        return \"onion\"
    if \"garlic\" in haystack:
        return \"garlic\"
    if \"egg\" in haystack:
        return \"egg\"
    if \"butter\" in haystack:
        return \"butter\"
    if \"milk\" in haystack:
        return \"milk\"
    if \"bread\" in haystack or \"bun\" in haystack or \"baguette\" in haystack or \"toast\" in haystack:
        return \"bread\"
    if \"pasta\" in haystack or \"spaghetti\" in haystack or \"penne\" in haystack or \"fusilli\" in haystack or \"macaroni\" in haystack or \"farfalle\" in haystack or \"linguine\" in haystack or \"tagliatelle\" in haystack:
        return \"pasta\"
    if \"rice\" in haystack:
        return \"rice\"
    if \"chicken\" in haystack:
        return \"chicken\"
    if \"beef\" in haystack:
        return \"beef\"
    if \"fish\" in haystack or \"salmon\" in haystack or \"tuna\" in haystack or \"cod\" in haystack or \"anchovy\" in haystack or \"sardine\" in haystack:
        return \"fish\"
    if \"lettuce\" in haystack or \"romaine\" in haystack or \"iceberg\" in haystack:
        return \"lettuce\"
    if \"pepper\" in haystack:
        return \"pepper\"
    if \"potato\" in haystack:
        return \"potato\"
    if \"mushroom\" in haystack:
        return \"mushroom\"
    if \"carrot\" in haystack:
        return \"carrot\"
    if \"cucumber\" in haystack:
        return \"cucumber\"
    if \"spinach\" in haystack:
        return \"spinach\"

    return ingredient.get(\"family\") or ingredient.get(\"slug\")


with open(ingredients_file, \"r\", encoding=\"utf-8\") as file:
    ingredients = json.load(file)


family_groups = defaultdict(list)
category_groups = defaultdict(list)
for ingredient in ingredients:
    family = ingredient.get(\"family\") or ingredient.get(\"slug\")
    family_groups[family].append(ingredient[\"slug\"])
    category_groups[ingredient.get(\"category\", \"other\")].append(ingredient[\"slug\"])


for ingredient in ingredients:
    ingredient[\"slug\"] = slugify(ingredient[\"name\"])

    if not ingredient.get(\"aliases\"):
        ingredient[\"aliases\"] = [ingredient[\"name\"].lower()]

    ingredient[\"family\"] = resolve_family(ingredient)

    family = ingredient.get(\"family\") or ingredient.get(\"slug\")
    category = ingredient.get(\"category\", \"other\")
    substitutes = [
        slug
        for slug in family_groups.get(family, [])
        if slug != ingredient[\"slug\"]
    ]

    if not substitutes:
        substitutes = [
            slug
            for slug in category_groups.get(category, [])
            if slug != ingredient[\"slug\"]
        ][:5]

    ingredient[\"substitutes\"] = substitutes

with open(ingredients_file, \"w\", encoding=\"utf-8\") as file:
    json.dump(ingredients, file, indent=4, ensure_ascii=False)

print(f\"Prepared {len(ingredients)} ingredients.\")
""")

print(f"Updated {updated} ingredient families and substitutes.")
