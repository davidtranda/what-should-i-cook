import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "assign_families.py"

spec = importlib.util.spec_from_file_location("assign_families", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_family_mapping_for_tomatoes_and_cheeses():
    ingredients = json.loads((ROOT / "database" / "ingredients.json").read_text(encoding="utf-8"))
    by_slug = {ingredient["slug"]: ingredient for ingredient in ingredients}

    tomato_like = ["tomato", "cherry_tomatoes", "canned_tomatoes", "sun_dried_tomatoes"]
    cheese_like = ["cheese", "cheddar_cheese", "mozzarella", "parmesan", "cream_cheese", "feta_cheese", "gouda_cheese"]

    for slug in tomato_like:
        assert by_slug[slug]["family"] == "tomato", f"{slug} should map to tomato family"

    for slug in cheese_like:
        assert by_slug[slug]["family"] == "cheese", f"{slug} should map to cheese family"
