from django.http import JsonResponse
from ingredients.models import Ingredients
from foodhack.helpers import RequestDict


def get_random_items(requests):
    """
    Получить рандомные ингридиенты
    :param requests:
    :return:
    """
    requests = RequestDict(requests)

    excludes = requests.data.get("exclude", [])
    limit = requests.data.get("limit", 10)

    list_ = Ingredients().random_ingredients_list(excludes, int(limit))

    return JsonResponse({"ingredients": list_})


