from Exceptions import BoardException
from Scheme import Dot

import random
from random import randint

near = [
    (-1, 0),
    (0, -1), (0, 0), (0, 1),
    (1, 0)
]


class Player:
    def __init__(self, board, enemy):
        """
        board - доска игрока
        enemy - доска противника
        repeat - получил ли компьютер доп. ход (т.е. выбил ли он часть корабля противника в предыдущем ходе)
        """
        self.board = board
        self.enemy = enemy
        self.repeat = False

    def ask(self):
        """
        метод не вызывается напрямую из основного класса, а используется только в классах-потомках
        """
        raise NotImplementedError()

    def play(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
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
        dot = self.choose_dot()
        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot

    def choose_dot(self):
        """
        Выбираем, в какую клетку будет бить компьютер.

        Если пользователь не успел потопить корабль компьютера, выбираем случайную клетку из незанятых.
        Если компьютер случайно выбил клетку корабля, в следующий ход он будет выбирать клетку,
        анализируя окружение поражённой клетки, чтобы с большей вероятностью потопить корабль.

        Если пользователь потопил больше 1 корабля компьютера, компьютер может получить преимущество
        (преимущество выбираем из ряда 0, 1, 1, чтобы компьютер чаще оказывался в выигрышной позиции):

        Сначала компьютер получает большое преимущество, чтобы он мог начать обыгрывать пользователя -
        Он выбирает корабль из списка пользовательских кораблей и топит его,
         пока не потопит в общей сложности 3 корабля.
        Далее преимущество уменьшается - компьютер так же выбирает корабль пользователя и пробивает одну точку в нём,
        затем бьёт наугад по окружающим незанятым клеткам.
        Он может как потопить весь корабль, так и промахнуться.
        """
        if self.board.killed > 1:
            advantage = random.choice([0, 1, 1])
            if advantage and self.enemy.killed <= 3:
                return self.sink()
            elif advantage and 4 < self.enemy.killed <= 5:
                return self.advantage()

        if self.repeat:
            return self.advantage()

        attempts = 0
        while attempts <= 100:
            dot = Dot(randint(0, 5), randint(0, 5))
            if dot not in self.enemy.occupied:
                return dot
            attempts += 1
        dot = Dot(randint(0, 5), randint(0, 5))
        return dot

    def sink(self):
        """
        Если доп. ход,
         найдём клетку, которую мы выбили в предыдущем ходе.
         По клетке найдём корабль и выбьем в нём другую клетку.

        Если не доп.ход,
         выбираем рандомный корабль противника длиной 1 или 2 и бьём по нему.
        """
        if self.repeat:
            shot_dot = self.enemy.occupied[-1]
            for ship in self.enemy.ships:
                if shot_dot in ship.dots:
                    for dot in ship.dots:
                        if dot.x != shot_dot.x or dot.y != shot_dot.y:
                            return dot

        while True:
            ship = random.choice(self.enemy.ships)
            if ship.length < 3:
                return random.choice(ship.dots)
            continue

    def advantage(self):
        """
        Если доп. ход,
         найдём клетку, которую мы выбили в предыдущем ходе.
         Найдём в её окружении клетки, куда мы ещё не били/которые не заняты, и будем бить по ним,
         чтобы с большей вероятностью потопить весь корабль.

        Если не доп.ход,
         выбираем рандомный корабль противника и бьём по нему
        """
        if self.repeat:
            shot_dot = self.enemy.occupied[-1]
            targets = []
            for dot_x, dot_y in near:
                cur_dot = Dot(shot_dot.x + dot_x, shot_dot.y + dot_y)
                if not (self.enemy.dot_out(cur_dot)) and cur_dot not in self.enemy.occupied:
                    targets.append(cur_dot)
            dot = random.choice(targets)
            return dot

        ship = random.choice(self.enemy.ships)
        return random.choice(ship.dots)

    def play(self, repeat=False):
        self.repeat = repeat
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as exc:
                print(exc)
