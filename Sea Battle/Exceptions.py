class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску"


class BoardOccupiedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


"""
Если мы случайно сгенерили неправильный корабль
"""


class BoardWrongShipException(BoardException):
    pass
