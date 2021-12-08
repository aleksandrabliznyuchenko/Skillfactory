from Scheme import Dot, Board
from Ship import Ship
from Player import User, Computer
from Exceptions import BoardWrongShipException

from random import randint

results = {1: 0,
           2: 0}


class Game():
    def __init__(self, size=6):
        self.size = size
        self.lengths = [3, 2, 2, 1, 1, 1, 1]

        board_user = self.random_board()
        board_comp = self.random_board()
        board_comp.hidden = True

        self.computer = Computer(board_comp, board_user)
        self.user = User(board_user, board_comp)
        self.boards = [board_user, board_comp]

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for length in self.lengths:
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
        repeat = False
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
                repeat = self.computer.play(repeat=repeat)
            if repeat:
                num -= 1

            if self.computer.board.killed == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                results[1] += 1
                break

            if self.user.board.killed == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                results[2] += 1
                break
            num += 1

    def new_game(self):
        new_game = input("Желаете сыграть ещё раз? (да/нет): ")
        if (new_game.lower() == "да"):
            board_user_new = self.random_board()
            board_comp_new = self.random_board()
            board_comp_new.hidden = True

            self.computer = Computer(board_comp_new, board_user_new)
            self.user = User(board_user_new, board_comp_new)
            self.boards = [board_user_new, board_comp_new]
            self.start()
        else:
            final_result = "-" * 27
            final_result += "\nРезультаты игры:\nИгрок: %i \nКомпьютер: %i" % (results[1], results[2])
            print(final_result)

    def start(self):
        self.greet()
        self.process()
        self.new_game()


game = Game()
game.start()
