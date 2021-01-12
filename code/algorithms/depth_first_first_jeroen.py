from code.classes.board import Board

def depth_first_algorithm(game, working_solution_movesets):
    for car in game.find_moves():
        possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
        if 0 in possible_steps:
            possible_steps.remove(0)

        for step in possible_steps:
            game.move()



board_number = "test"
board_sizes = { "1": 6, "2": 6, "3": 6,
                 "4": 9, "5": 9, "6": 9,
                 "7": 12, "test" : 4}

data = f"./data/gameboards/Rushhour{board_sizes[board_number]}x{board_sizes[board_number]}_{board_number}.csv"
game = Board(board_sizes[board_number],data)

all_solutions = depth_first_algorithm(game, [])


