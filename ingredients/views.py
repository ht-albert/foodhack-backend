from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from ingredients.models import Ingredients
from foodhack.helpers import RequestDict


@csrf_protect
def get_random_item(requests):
    """
    Получить рандомные ингридиенты
    :param requests:
    :return:
    """
    requests = RequestDict(requests)

    excludes = requests.data.get("exclude", [])
    limit = requests.data.get("limit", 10)

    list_ = Ingredients().random_ingredients_list(excludes, limit)

    return JsonResponse({"ingredients": list_})


