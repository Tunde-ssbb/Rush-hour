from code.classes.board import Board
import queue
import copy

def breadth_first_algorithm(game, depth = None):
    solution_lengths = []
    state_queue = queue.Queue()
    state_queue.put([game.give_hash(),[]])

    while not state_queue.empty() :
        state = state_queue.get()

        #print("examining game state:" ,state)
        game_hash,moves = state[0],state[1]
        game.load_board_from_hash(game_hash)
        game.archive_board()
 
        if game.won():
            # print("Solution was found! Moves:", moves)
            solution_lengths.append(len(moves))
            if len(moves) < len(game.shortest_solution_movesets) or game.shortest_solution_movesets == []:
                game.log_shortest_solution_movesets(moves)
            if depth == None:
                break

        elif depth == None or (depth != None and len(moves) < depth):
            possible_moves = game.find_moves()

            for car in possible_moves:
                possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
                if 0 in possible_steps:
                    possible_steps.remove(0)
                #print(f"possible_steps for {car}: {possible_steps}")

                for step in possible_steps:
                    #print("moving",car,step)
                    game.move(car,step)
                    moves.append([car, step])
                    
                    if game.give_hash() not in game.archive:
                        #print("Adding to queue", game.give_hash(), moves)
                        state_queue.put([game.give_hash(), copy.deepcopy(moves)])
                    else:
                        #print("State", game.give_hash(), "already exists in archive")
                        pass

                    #print("queue:", list(state_queue.queue))
                    moves.pop()
                    game.load_board_from_hash(game_hash)
    print("shortest solution found:", game.shortest_solution_movesets)
    return game.shortest_solution_movesets, solution_lengths




