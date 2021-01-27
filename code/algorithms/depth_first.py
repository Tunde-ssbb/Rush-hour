from code.classes.board import Board
import random
import copy

def depth_first_smart_archive_algorithm(game, max_moves, archive, filter_cars = None, branch_and_bound = False, randomize = False):
    """
    depth first algorithm that finds the shortest solution with equal or less than the max_moves.
    an archive (given in )is used to reduce the running time of the algorithm
    """

    # check if the game is won in the current state
    if game.won():
        moves = game.moves[:]

        # save solution if it is shorter than shortest one found
        if len(moves) < len(game.shortest_solution_movesets) or game.shortest_solution_movesets == []:
            game.log_shortest_solution_movesets(moves)

    # dynamically cut off depth search at the shortest solution length if branch and bound is set to true
    if branch_and_bound and len(game.shortest_solution_movesets) > 0:
        if len(game.shortest_solution_movesets[-1]) < max_moves:
            max_moves = len(game.shortest_solution_movesets[-1])

    # only proceed on branch if current state is not yet in archive, or if current state was reached in less moves than identical state in archive
    elif len(game.moves) < max_moves and (game.give_hash() not in archive or (archive.get(game.give_hash(), max_moves +1) > len(game.moves))):    
       
        # save the current board to be able to go back
        current_board_state = game.give_hash()
        # add new state to archive, or update existing state
        archive.update({current_board_state:len(game.moves)})
        # find the possible moves of the game
        possible_moves = game.find_moves(filter_cars = filter_cars)
        cars = list(possible_moves.keys())

        # randomize order if requested
        if randomize:
            cars = random.sample(cars, len(cars))

        # loop over all possible moves
        for car in cars:
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            # start with the largest moves
            possible_steps = sorted(possible_steps, key=abs, reverse=True)
    
            for step in possible_steps:
                # make a move with the car
                game.move(car, step)
                game.moves.append([car,step])
                # run algorithm on current branch
                depth_first_smart_archive_algorithm(game, max_moves, archive, filter_cars = filter_cars, branch_and_bound = branch_and_bound, randomize = randomize)
                # done with the branch and move back and load the board
                game.step_back()
                game.load_board_from_hash(current_board_state)


def depth_first_smart_archive_main(number_of_attempts, max_moves, data, fixed_solutions, filter_movesets = None, branch_and_bound = False, randomize = False):
    """
    function used to call the depth first algorithm.
    with fixed_solutions on False the algoritm is run number_of_attempts times.
    with fixed_solutions on True the algoritm is run until it finds number_of_attempts solutions.
    A list of solution movesets can be given as filter. (The algorithm will not look at any cars 
    that do not move in these solutions)
    if branch_and bound_ is set to True, a dynamic bound is applied when searching state-space (starting at max_moves)
    if randomize is set to true, state sapce is searched in random order, rather than alphabetically by car_id
    """
    # create a compacter filter list with all car_id's
    if filter_movesets:
        filter_cars = create_filter(filter_movesets)
    else:
        filter_cars = filter_movesets

    if not fixed_solutions: 
        solutions = []
        # run the algorithm a fixed amount of times
        for n in range(number_of_attempts):
            game = Board(data)
            archive = {}
            # run the algorithm
            depth_first_smart_archive_algorithm(game, max_moves, archive, filter_cars = filter_cars, branch_and_bound = branch_and_bound, randomize = randomize)
            # the shortest solution (if any exists) is added to solution list
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)
    else:
        solutions = []
        # run the algorithm until enough solutions are found
        while len(solutions)  < number_of_attempts :
            game = Board(data)
            archive = {}
            # run the algorithm
            depth_first_smart_archive_algorithm(game, max_moves, archive = archive, filter_cars = filter_cars, branch_and_bound = branch_and_bound, randomize = randomize)
            # add shortest found solution to solution set
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)

    return solutions

def create_filter(filter_movesets):
    """
    Function used to go from list of solution movesets to usable filter for depth first 
    Input: list of soliution movesets (moveset is a list of moves)
    Output: list of unique car_id's that move in any of the solutions
    """
    filter_cars = []

    # extract moving cars from movesets
    for moveset in filter_movesets:
        filter_cars.extend([move[0] for move in moveset])
    filter_cars = list(set(filter_cars))

    print(f"filtering: {filter_cars}")

    return filter_cars