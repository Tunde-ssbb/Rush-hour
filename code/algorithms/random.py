from code.classes.board import Board
import copy
import random


def random_main(data, number_of_attempts, max_moves):
    """
    Function used to call random_moves algorithm number of attempts times.
    Keeps running until length of solution is smaller than max moves.
    Input: number_of_attempts (int), max_moves (int). Output: list of solution movesets.
    """
    solutions = []
    for i in range(number_of_attempts):
        print(f"finding random solution {len(solutions) + 1}")
        
        # reset length to initial value
        length_solution = float('inf')

        # repeat random algorithm until smaller solution than max moves is found
        while length_solution > max_moves:
            game = Board(data)
            new_solution = random_algorithm(game, max_moves)
            length_solution = len(new_solution)

        # if solution found copy moves and add to solutions list
        print(f"length random solution: {length_solution}")
        best_solution = copy.deepcopy(new_solution)
        solutions.append(best_solution)

    return solutions


def random_algorithm(game, max_moves):
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

        # stop algorithm if longer than shortest solution found
        if len(game.moves) > max_moves:
            break

    return game.moves