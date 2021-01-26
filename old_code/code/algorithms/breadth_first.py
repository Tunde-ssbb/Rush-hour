from code.classes.board import Board
from code.heuristics.blocking_cars import blocking_cars_calculate_score
import queue
import copy
import time

def breadth_first_algorithm(game, depth = None, origin = "main"):
    """
    Implementation of breadth first algorithm. Function takes game (board object) as input.
    If an integer is given for depth, all solutions up to depth amount of moves are given. Otherwise the algorithm
    is run until a solution is found.
    """
    solution_lengths = []
    state_queue = queue.Queue()
    state_queue.put([game.give_hash(),[]])
    cur_depth = 0
    if origin == "population":
        scores_and_boards = []
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
            scores_and_boards.append(( blocking_cars_calculate_score(game, 3), game.give_hash()))

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
        return scores_and_boards, game.shortest_solution_movesets


def breadth_first_population(game, n_gens,  layers_per_gen, n_survivors):
    """
    Population based algorithm with breadth first. Each generation gets layers_per_gen moves. All the boards
    that are created after these moves are put through a heuristic. The best n_survivors survive. These will be used 
    in the next generation of breadth first moves. 
    """

    # initiate first survivor and archive survivors
    survivors = [game.give_hash()]
    best_score = blocking_cars_calculate_score(game, 3)
    gen = 0
    archive = set()
    while gen < n_gens:
        boards = []
        # examine each survivor
        for survivor in survivors:
            game.load_board_from_hash(survivor)
            # search board
            scores_and_boards, shortest_sol = breadth_first_algorithm(game, layers_per_gen, origin = "population")
            # print if a solution was found
            if len(shortest_sol):
                print(f"a solution of {len(shortest_sol)} moves was found: {shortest_sol}")
            # add to searched boards
            boards.extend(scores_and_boards)
        # sort boards to score and take best boards
        sorted_scores_and_boards = sorted(boards)
        sorted_scores_and_boards = [board for board in sorted_scores_and_boards if board[1] not in archive]

        if len(sorted_scores_and_boards):
            new_sorted_scores, new_sorted_boards = zip(*sorted_scores_and_boards)
            # if scores have improved, move on to next generation
            if new_sorted_scores[0] <= best_score:
                survivors, best_score, old_boards = new_sorted_boards[:n_survivors], new_sorted_scores[0], sorted_scores_and_boards[n_survivors:]
                print(f"searched gen {gen}")
                print(f"best score: {best_score}")
            # if not, rerun current generation with new boards from the previous generation
            else:
                print("generation did not improve, trying again")
                old_boards = [board for board in old_boards if board[1] not in archive]
                survivors = tuple([board[1] for board in old_boards[:n_survivors]])
                old_boards = old_boards[n_survivors:]
                gen -= 1
        # if there are no boards that have survived that are not alreeady in archive, new boards from previous generation are used
        else:
            old_boards = [board for board in old_boards if board[1] not in archive]
            survivors = tuple([board[1] for board in old_boards[:n_survivors]])
            old_boards = old_boards[n_survivors:]
            gen -= 1
        # add survivors to archive
        for survivor in survivors:
            archive.add(survivor)

        gen += 1


