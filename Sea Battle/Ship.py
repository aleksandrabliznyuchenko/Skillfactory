from Scheme import Dot


class Ship:
    def __init__(self, length, bow, orientation):
        """
        length - длина корабля
        bow - точка, в которой размещен нос корабля
        orientation - ориентация корабля(0 = вертикальная, 1 = горизонтальная)
        lives - количество жизней у корабля( = длине корабля)
        """
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            # ориентация вертикальная
            if self.orientation == 0:
                cur_x += i
            # ориентация горизонтальная
            elif self.orientation == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots
