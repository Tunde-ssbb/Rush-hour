from code.classes.board import Board
from code.heuristics.blocking_cars import calculate_score
import queue
import copy

def breadth_first_algorithm(game, depth = None, origin = "main"):
    """
    Implementation of breadth first algorithm. Function takes game (board object) as input.
    If an integer is given for depth, all solutions up to depth amount of moves are given. Otherwise the algoraithm
    is run until a solution is found.
    """
    solution_lengths = []
    state_queue = queue.Queue()
    state_queue.put([game.give_hash(),[]])
    cur_depth = 0
    if origin == "population":
        boards_and_scores = []
    # keep searching as long as there are states to be examined
    while not state_queue.empty() :
        # get next state
        state = state_queue.get()
        # set game to the state
        game_hash,moves = state[0],state[1]
        game.load_board_from_hash(game_hash)
        game.archive_board()

        if origin == "main" and len(moves) > cur_depth:
            print("checking solutions of depth", len(moves))
            cur_depth = len(moves)
        
        if origin == "population":
            boards_and_scores.append((game.give_hash(), blocking_cars_calculate_score(game, 3)))

        # check if game was won
        if game.won():
            # print("Solution was found! Moves:", moves)
            solution_lengths.append(len(moves))
            if len(moves) < len(game.shortest_solution_movesets) or game.shortest_solution_movesets == []:
                game.log_shortest_solution_movesets(moves)
            # if no depth was provided the algorithm stops
            if depth == None:
                break
        # if game was not won, and depth is not exceeded yet, continue search
        elif depth == None or (depth != None and len(moves) < depth):
            # retrieve and loop over all possible moves
            possible_moves = game.find_moves()
            for car in possible_moves:
                possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
                if 0 in possible_steps:
                    possible_steps.remove(0)
                #print(f"possible_steps for {car}: {possible_steps}")

                for step in possible_steps:
                    # make move and save
                    game.move(car,step)
                    moves.append([car, step])
                    # if it is a new boardstate it gets added to the queue
                    if game.give_hash() not in game.archive:
                        #print("Adding to queue", game.give_hash(), moves)
                        state_queue.put([game.give_hash(), copy.deepcopy(moves)])
                    # undo move
                    moves.pop()
                    game.load_board_from_hash(game_hash)
    # print shortest solution
    if len(game.shortest_solution_movesets) != 0:
        print("shortest solution found:", game.shortest_solution_movesets)
    else:
        pass
        #print("no solution found")

    if origin == "main":
        return game.shortest_solution_movesets
    elif origin == "population":
        return boards_and_scores, game.shortest_solution_movesets


def breadth_first_population(game, n_gens,  layers_per_gen, n_survivors):
    """
    Population based algorithm with breadth first. Each generation gets layers_per_gen moves. All the boards
    that are created after these moves are put through a heuristic. The best n_survivors survive. These will be used 
    in the next generation of breadth first moves. 
    """

    # initiate first survivor and archive survivors
    survivors = [(game.give_hash(), (blocking_cars_calculate_score(game, 3)))]
    gen = 0
    archive = set()
    while gen < n_gens:
        boards = []
        # examine each survivor
        for survivor in survivors:
            print(survivor[1])
            game.load_board_from_hash(survivor[0])
            # search board
            boards_and_scores, shortest_sol = breadth_first_algorithm(game, layers_per_gen, origin = "population")
            if len(shortest_sol):
                print(f"a solution of {len(shortest_sol)} moves was found: {shortest_sol}")
            # add to searched boards
            boards.extend(boards_and_scores)
        # sort boards to score and take best boards
        sorted_boards = sorted(boards)
        sorted_boards = [board for board in sorted_boards if board[0] not in archive]
        survivors = sorted_boards[:n_survivors]
        for survivor in survivors:
            archive.add(survivor[0])

        print(f"searched gen {gen}")
        gen += 1


