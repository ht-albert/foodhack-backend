from django.db import models


class Ingredients(models.Model):

    class Meta:
        db_table = "ingredients"

    key = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    img = models.CharField(max_length=1000)

    def __response(self):
        """
        Формат в котором будет отправлены данные
        :return:
        """
        return {
            "id": self.id,
            "key": self.key,
            "name": self.name,
            "img": self.img,
        }

    @staticmethod
    def random_ingredients_list(filter_list, limit=10):
        """
        Возвращает случайный список ингридиентов исключая переданные ингридиенты
        :param filter_list:
        :param limit:
        :return:
        """

        ingredients = Ingredients.objects.exclude(id__in=filter_list).order_by("?")[:limit]

        list_ingredients = []
        for _ in ingredients:
            list_ingredients.append(_.__response())

        return list_ingredients

    @staticmethod
    def get_keys_by_id(ids):
        """
        Вернет список ингридиентов по id
        :param ids:
        :return:
        """
        ingredients = Ingredients.objects.filter(id__in=ids).values_list("key")

        list_ingredients = []
        for _ in ingredients:
            list_ingredients.append(_[0])

        return list_ingredients

    @staticmethod
    def get_ingredients_by_keys(keys):
        """
        Вернет список ингридиентов по ключам
        :param keys:
        :return:
        """

        ingredients = Ingredients.objects.filter(key__in=keys)

        list_ = []
        for _ in ingredients:
            list_.append(_.__response())

        return list_
