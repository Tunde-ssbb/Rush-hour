from code.classes.board import Board
import copy
import random


def random_main(size, data, number_of_attempts, max_moves):
    """
    Function used to call random_moves algorithm number of attempts times.
    Keeps running until length of solution is smaller than max moves.
    Input: number_of_attempts (int), max_moves (int). Output: list of solution movesets.
    """
    solutions = []
    for i in range(number_of_attempts):
        print(f"finding random solution {len(solutions) + 1}")
        
        # reset length and best solution to initial values
        length_best_solution = float('inf')
        best_solution = []

        # repeat random algorithm until smaller solution than max moves is found
        while length_best_solution > max_moves:
            game = Board(size, data)
            new_solution = random_algorithm(game, length_best_solution)
            
            # replace length best solution if new solution is smaller
            if len(new_solution) < length_best_solution:
                length_best_solution = len(new_solution)

        # if solution found copy moves and add to solutions list
        print(length_best_solution)
        best_solution = copy.deepcopy(new_solution)
        solutions.append(best_solution)

    return solutions


def random_algorithm(game, length_best_solution):
    """
    Random algorithm that finds solutions by performing random moves. 
    Keeps running until game is won.
    Input: game (Board object). Output: list of moves.
    """

    # repeat until game is won
    while not game.won():
        
        # find possible moves and select random car to move
        possible_moves = game.find_moves()
        car = random.choice(list(possible_moves.keys()))

        # select range of car, excluding 0, and select random step out of range
        possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
        if 0 in possible_steps:
            possible_steps.remove(0)
        step = random.choice(possible_steps)

        # filter out moves that are the exact opposite of the last move
        if len(game.moves) == 0:
            game.move(car, step)
            game.log_move(car, step)
        elif game.moves[-1][0] == car and game.moves[-1][1] == -step:
            pass
        else:
            game.move(car, step)
            game.log_move(car, step)

        if len(game.moves) >= length_best_solution:
            break

    return game.moves