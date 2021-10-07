from Exceptions import BoardException
from Scheme import Dot

import random
from random import randint


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    """
    метод не вызывается напрямую из основного класса, а используется только в классах-потомках
    """
    def ask(self):
        raise NotImplementedError()

    def play(self):
        while True:
            try:
                cell = self.ask()
                repeat = self.enemy.shoot(cell)
                return repeat
            except BoardException as exc:
                print(exc)


class User(Player):
    def ask(self):
        while True:
            cell = input("Ваш ход: ").split()
            if len(cell) != 2:
                print("Введите 2 координаты клетки! ")
                continue

            x, y = cell
            if not x.isdigit() or not y.isdigit():
                print("Координаты должны быть числами! ")
                continue

            return Dot(int(x) - 1, int(y) - 1)


class Computer(Player):
    def ask(self):
        """
        Если пользователь успел потопить хотя бы один корабль компьютера,
        Компьютеру даётся преимущество:
        Он может рандомно выбрать, будет ли он сразу бить по клеткам с кораблями пользователя
        Или же атакует рандомную незанятую клетку на доске
        """
        if self.enemy.killed >= 1:
            advantage = randint(0, 1)
            if advantage:
                ship = random.choice(self.enemy.ships)
                dot = random.choice(ship.dots)
            else:
                dot = Dot(randint(0, 5), randint(0, 5))
        else:
            dot = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot
