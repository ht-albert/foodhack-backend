from django.http import JsonResponse

import random
import requests
from foodhack.helpers import RequestDict
from ingredients.models import Ingredients


URL_SEARCH = "https://mnevkusno.ru/searchbyingredients"


def get_list(requests):
    """

    :param requests:
    :return:
    """
    requests = RequestDict(requests)
    
    exclude = requests.data.get("exclude", [])
    like = requests.data.get("like", [])

    ingredients = Ingredients().get_keys_by_id(like)

    dish = get_dish_by_ingredients(ingredients)

    dish_list = []
    for _ in dish:
        dish_list.append(__response(_))

    return JsonResponse({"dish": dish_list})


def get_dish_by_ingredients(ingredients):
    """

    :param ingredients:
    :return:
    """

    data = {
        "ingredients": ingredients
    }

    try:
        query = requests.post(url=URL_SEARCH, data=data)
    except:
         query = None

    return query.json() if query else []


def __response(dish):
    """

    :param dish:
    :return:
    """
    return {
        "name": dish.get("name", None),
        "url": dish.get("url", None),
        "timeCooking": dish.get("cookingTime", None),
        "energyValue": dish.get("energyValue", {}),
        "missingIngredients": random.choice([1, 2, 4, 3, 0, 0, 0, 5]),
        "img": dish.get("thumb", None)
    }
