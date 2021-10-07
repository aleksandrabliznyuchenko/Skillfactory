from Exceptions import BoardException, BoardOutException, BoardOccupiedException, BoardWrongShipException


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Board:
    """
    hidden - скрыто ли поле от пользователя (True/False)
    size - размер поля (стандартно 6х6)

    field - отметка поля
    ships - список кораблей на доске
    occupied - занятые кораблями клетки (либо клетки, куда стреляли, но промазали)
    killed - потопленные корабли
    """

    def __init__(self, hidden=False, size=6):
        self.hidden = hidden
        self.size = size

        self.field = [["O"] * size for _ in range(size)]
        self.ships = []
        self.occupied = []
        self.killed = 0

    def __str__(self):
        board = "-" * 27
        board += "\n  |"
        for _ in range(self.size):
            board += " %i |" % (_ + 1)
            # board += " %i |" % (_)
        for i, row in enumerate(self.field):
            board += f"\n{i + 1} | " + " | ".join(row) + " |"
            # board += f"\n{i} | " + " | ".join(row) + " |"

        if self.hidden:
            board = board.replace("#", "O")

        return board

    def contour(self, ship, mark=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dot in ship.dots:
            for dot_x, dot_y in near:
                cur_dot = Dot(dot.x + dot_x, dot.y + dot_y)
                # обводим контур корабля, если он не выходит за пределы доски и
                # не перекрывает занятые клетки
                if not (self.dot_out(cur_dot)) and cur_dot not in self.occupied:
                    self.occupied.append(cur_dot)
                    if mark:
                        self.field[cur_dot.x][cur_dot.y] = "."

    def check_ship(self, ship):
        for dot in ship.dots:
            if self.dot_out(dot):
                raise BoardOutException
            if dot in self.occupied:
                raise BoardOccupiedException
        return True

    def add_ship(self, ship):
        for dot in ship.dots:
            if self.dot_out(dot) or dot in self.occupied:
                raise BoardWrongShipException

        for dot in ship.dots:
            self.field[dot.x][dot.y] = "#"
            self.occupied.append(dot)

        self.ships.append(ship)
        self.contour(ship)

    """
    находится ли точка за пределами доски
    """

    def dot_out(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    """
    Стреляем по кораблю
    В случае промаха ход переходит к другому игроку
    Если корабль ранили, но не добили, даём игроку дополнительный ход
    Если корабль потопили, обводим его контур на доске, а ход переходит к другому игроку
    """

    def shoot(self, dot):
        if self.dot_out(dot):
            raise BoardOutException
        if dot in self.occupied:
            raise BoardOccupiedException

        self.occupied.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                self.field[dot.x][dot.y] = "X"
                ship.lives -= 1
                if ship.lives == 0:
                    self.killed += 1
                    self.contour(ship, mark=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.occupied = []
