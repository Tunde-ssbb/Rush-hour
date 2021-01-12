from code.classes.board import Board

def depth_first_algorithm(board_number):
    board_sizes = { "1": 6, "2": 6, "3": 6,
                     "4": 9, "5": 9, "6": 9,
                     "7": 12}

    data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
    board = Board(board_sizes[board_number],data)

    working_solution_movesets = []

    archive = set()
