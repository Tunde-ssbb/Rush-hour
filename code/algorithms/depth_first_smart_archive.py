from code.classes.board import Board
import random
import copy
import time

def depth_first_algorithm(game, max_moves, archive = None):
    """
    depth first algorithm that finds the shortest solution with equal or less than the max_moves.
    an archive is used to reduce the running time of the algorithm
    """
    #archive = {}
    # check if the branch reached a winning solution
    if game.won():
        moves = game.moves[:]
        #print(f"solution found: {len(moves)}")
        if len(moves) < len(game.shortest_solution_movesets) or game.shortest_solution_movesets == []:
            game.log_shortest_solution_movesets(moves)

    # dynamically cut off depth search at the shortest solution length
    # if len(game.shortest_solution_movesets) > 0:
    #     if len(game.shortest_solution_movesets[-1]) < max_moves:
    #                 max_moves = len(game.shortest_solution_movesets[-1])

    # if the new branch is in the archive ignore the branch
    elif len(game.moves) < max_moves and (game.give_hash() not in archive or (archive.get(game.give_hash(), max_moves +1) > len(game.moves)))  :
        # save the current board to be able to go back
        current_board_state = game.give_hash()

        archive.update({current_board_state:len(game.moves)})
        #print(f"{len(archive)} boards in archive")
        #time.sleep(1)
 
        possible_moves = game.find_moves()
        # randomize the order of moves
        cars = list(possible_moves.keys())
        cars = random.sample(cars, len(cars))
        for car in cars:
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)

            # start with the largest moves
            possible_steps = sorted(possible_steps, key=abs, reverse=True)

            # make a move with the car
            for step in possible_steps:
                game.move(car, step)
                game.moves.append([car,step])
                # go to the branch of the move
                depth_first_algorithm(game, max_moves, archive = archive)

                # done with the branch and move back and load the board
                game.step_back()
                game.load_board_from_hash(current_board_state)


def depth_first_main(number_of_attempts, max_moves, size, data, fixed_solutions):
    """
    function used to call the depth first algorithm.
    with fixed_solutions on False the algoritm is run number_of_attempts times.
    with fixed_solutions on True the algoritm is run until it finds number_of_attempts solutions.
    """

    if not fixed_solutions: 
        solutions = []
        for n in range(number_of_attempts):
            game = Board(size,data)
            archive = {}
            depth_first_algorithm(game, max_moves, archive = archive)
            # print(len(game.shortest_solution_movesets))
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)
    else:
        solutions = []
        while len(solutions)  < number_of_attempts :
            game = Board(size,data)
            archive = {}
            depth_first_algorithm(game, max_moves, archive = archive)
            # print(f"solutions found: {len(game.shortest_solution_movesets)}")
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)

    return solutions