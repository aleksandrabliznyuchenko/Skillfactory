board = list(range(1, 10))
results = {1: 0,
           2: 0}


def show_board(board):
    print("-" * 9)
    for i in range(3):
        print("|", board[0 + i * 3], board[1 + i * 3], board[2 + i * 3])


def check_cell(cell):
    if 1 < cell > 9:
        print("Введите число от 1 до 9.")
        return False

    if board[cell - 1] in ["X", "0"]:
        print("Клетка уже занята.")
        return False

    return True


def put_item(player, item):
    cell = int(input("Игрок %i, в какую клетку поставить %s? " % (player, item)))
    if check_cell(cell):
        board[cell - 1] = item
        show_board(board)
    else:
        put_item(player, item)


def check_result(board):
    combos = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7)]

    for combo in combos:
        result = board[combo[0] - 1] == board[combo[1] - 1] == board[combo[2] - 1]
        if result:
            return True
    return False


def game():
    global board
    show_board(board)
    for i in range(9):
        player = 1 if i % 2 == 0 else 2
        item = "X" if player == 1 else "0"
        put_item(player, item)
        if i >= 4:
            if (check_result(board)):
                print("Победил игрок %i!" % player)
                results[player] += 1
                break
            elif i == 9 and not check_result(board):
                print("Ничья!")

    new_game = input("Желаете сыграть ещё раз? (да/нет): ")
    if (new_game.lower() == "да"):
        board = list(range(1, 10))
        game()
    else:
        final_result = "Результаты игры:\nИгрок 1: %i \nИгрок 2: %i" % (results[1], results[2])
        print(final_result)


game()
