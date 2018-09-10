import json


class RequestDict(object):
    """
    Сериалиазиция запроса
    """
    data = {}
    token = None

    def __init__(self, request):
        self.request = request
        self.type = request.method
        self.__init_data()

    def __init_data(self):
        """
        В зависимоти от запроса инициализирует данные
        """
        if self.type == "POST" or self.type == "DELETE":
            self.data = json.loads(self.request.body.decode("utf-8"))
            self.token = self.data.get("token", None)

        elif self.type == "GET":
            self.data = self.request.GET
            self.token = self.data.get("token", None)
