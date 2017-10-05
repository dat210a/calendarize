class Error(Exception):
    pass


class AccessPermissionError(Error):

    def __init__(self, expression, message):
        self.__expression = expression
        self.__message = message
