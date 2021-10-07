from Scheme import Dot, Board
from Ship import Ship
from Player import User, Computer
from Exceptions import BoardWrongShipException

from random import randint


class Game():
    def __init__(self, size=6):
        self.size = size
        board_user = self.random_board()
        board_comp = self.random_board()
        board_comp.hidden = True

        self.computer = Computer(board_comp, board_user)
        self.user = User(board_user, board_comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for length in lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(length=length,
                            bow=Dot(randint(0, self.size), randint(0, self.size)),
                            orientation=randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветствуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def process(self):
        num = 0
        while True:
            print("-" * 27)
            print("Доска пользователя:")
            print(self.user.board)
            print("-" * 27)
            print("Доска компьютера:")
            print(self.computer.board)
            if num % 2 == 0:
                print("-" * 27)
                print("Ходит пользователь!")
                repeat = self.user.play()
            else:
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.computer.play()
            if repeat:
                num -= 1

            if self.computer.board.killed == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.board.killed == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.process()


game = Game()
game.start()
