from dataclasses import dataclass
from .constants import Spice, RawMaterial
from pathlib import Path
import json
from unidecode import unidecode


@dataclass
class RecipeItem:
    item: Spice | RawMaterial | None
    quantity: float
    text: str


@dataclass
class Recipe:
    name: str
    items: dict | list[RecipeItem]
    procedure: dict | list[str]
    note: str | None = None
    portions: int | None = None
    is_čuču: bool = False


def _parse_item(item: str) -> RecipeItem:
    return RecipeItem(None, 0, item)


def _load_items_rec(items: list[str] | dict) -> list[RecipeItem] | dict:
    if type(items) is list:
        return list(map(lambda x: _parse_item(x), items))

    out = {}
    for k, v in items.items():
        out[k] = _load_items_rec(v)
    return out


def _load_recipe(file: Path) -> Recipe:
    recipe_json = json.load(open(file, mode='r', encoding='utf-8'))

    items = _load_items_rec(recipe_json['items'])

    return Recipe(recipe_json['name'], items, recipe_json['procedure'], note=recipe_json.get('note'),
                  is_čuču=recipe_json.get('is_čuču', False), portions=recipe_json.get('portions'))


def load_all() -> dict[str, list[Recipe]]:
    out = {}
    for meal in ['Polévky', 'Hlavní Jídla', 'Lehčí jídla na svačinu', 'Pomazánky', 'Saláty', 'Přílohy', 'Dezerty']:
        out[meal] = []
        directory = Path(__file__).parent.parent/'recepty' / \
            unidecode(meal).replace(' ', '_').lower()
        for recipe in directory.iterdir():
            if not recipe.name.endswith('.json'):
                continue

            out[meal].append(_load_recipe(recipe))

    return out
