from django.http import JsonResponse

import requests
from foodhack.helpers import RequestDict
from ingredients.models import Ingredients


URL_SEARCH = "https://mnevkusno.ru/searchbyingredients"


def get_list(requests):
    """
    Получает список блюд
    :param requests:
    :return:
    """
    requests = RequestDict(requests)
    
    exclude = requests.data.get("exclude", [])
    like = requests.data.get("like", [])
    dish_list = []

    if not like:
        return JsonResponse({"dishes": dish_list})

    good_ingredients = Ingredients().get_keys_by_id(like)
    bad_ingredients = Ingredients().get_keys_by_id(exclude)

    dish = get_dish_by_ingredients(good_ingredients)

    for _ in dish:
        if is_bad_ingredient_in_dish(_, bad_ingredients) or not _.get("thumb", None):
            continue

        dish_list.append(__response(_, len(set(ingredients_list(_)).difference(set(good_ingredients)))))

    # Возвращем блюда в порядке возрастания недостающих ингредиетов
    return JsonResponse({"dishes": sorted(dish_list, key=lambda missing: missing['missingIngredients'])})


def get_dish_by_ingredients(ingredients):
    """
    Выполняет запрос на получение списка блюд по переданным ингридиентам
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


def ingredients_list(dish):
    """
    Возвращает список ключей ингридиентов, которые входят в состав блюда
    :param dish:
    :return:
    """
    list_ = []
    for _ in dish.get("ingredients", []):
        list_.append(_.get("name", None))

    return list_


def is_bad_ingredient_in_dish(dish, bag_ingredients):
    """
    Проверяет входят ли ингредиенты блюда в список запрещенных
    :param dish:
    :param bag_ingredients:
    :return:
    """
    for _ in ingredients_list(dish):
        if _ in bag_ingredients:
            return True

    return False


def __response(dish, missing):
    """
    Формат возвращаемых данных
    :param dish:
    :return:
    """

    return {
        "name": dish.get("name", None),
        "url": dish.get("url", None),
        "timeCooking": dish.get("cookingTime", None),   # время приготовления
        "energyValue": dish.get("energyValue", {}),   # информация о коллорийности
        "missingIngredients": missing,  # количество нехватающих ингридиентов
        "img": dish.get("thumb", None),
        "steps": dish.get("cookingSteps", {}),
        "ingredients": Ingredients().get_ingredients_by_keys(ingredients_list(dish))
    }
