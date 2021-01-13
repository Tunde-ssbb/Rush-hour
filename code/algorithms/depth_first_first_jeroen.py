from code.classes.board import Board
import random
import copy



def depth_first_algorithm(game, max_moves):
    # check if the branch reavhed an winning solution
    if game.won():
        moves = game.moves[:]
        #print(f"Winning moves : { game.moves }")
        if len(moves) < len(game.shortest_solution_movesets) or game.shortest_solution_movesets == []:
            game.log_shortest_solution_movesets(moves)


    elif game.give_hash() not in game.archive and len(game.moves) < max_moves :
        #game.draw_board()
        current_board_state = game.give_hash() 
        game.archive_board()
        #print(game.archive)
        possible_moves = game.find_moves()
        cars = list(possible_moves.keys())
        cars = random.sample(cars, len(cars))
        for car in cars:
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            #print(f"possible_steps for {car}: {possible_steps}")

            for step in possible_steps:
                #print(f"{car} does {step}")
                game.move(car, step)
                game.moves.append([car,step])
                #print(F"moves taken : {game.moves}")
                depth_first_algorithm(game, max_moves)
                game.step_back()
                game.load_board_from_hash(current_board_state)
    else:
        pass
        #print("repeated state")


def depth_first_main(number_of_attempts, max_moves, size, data, fixed_solutions):
    if not fixed_solutions: 
        solutions = []
        for n in range(number_of_attempts):
            game = Board(size,data)
            depth_first_algorithm(game, max_moves)
            print(len(game.shortest_solution_movesets))
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)
    else:
        solutions = []
        while len(solutions)  < number_of_attempts :
            game = Board(size,data)
            depth_first_algorithm(game, max_moves)
            print(len(game.shortest_solution_movesets))
            if len(game.shortest_solution_movesets) != 0:
                solutions.append(game.shortest_solution_movesets)

    return solutions


def remove_useless_moves(moveset, size, data):
   
    for i in range(len(moveset)):
        car = moveset[i][0]
        for j in range(i+1,len(moveset)):
            
           
            if car == moveset[j][0]:
                test_moveset = copy.deepcopy(moveset)
                test_moveset[i][1] = moveset[i][1] + moveset[j][1]
                test_moveset[j][1] = 0
                if check_solution(test_moveset, size, data):
                    moveset = test_moveset[:]

    
    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i]
    #print(moveset)      
    #print(len(moveset))

    for i in range(len(moveset)):
        car = moveset[i][0]
        for j in range(i+1,len(moveset)):
                    
            if car == moveset[j][0]:
                test_moveset = copy.deepcopy(moveset)
                test_moveset[i][1] = 0
                test_moveset[i][1] = 0
                if check_solution(test_moveset, size, data):
                    #print("-----remove-remove-----")
                    moveset = test_moveset[:]

    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i]
    #print(moveset)      
    #print(len(moveset))

    for i in range(len(moveset)):
        car = moveset[i][0]
        for j in range(i+1,len(moveset)):
                    
            if car == moveset[j][0]:
                test_moveset = copy.deepcopy(moveset)
                test_moveset[i][1] = 0
                test_moveset[j][1] = moveset[i][1] + moveset[j][1]
                if check_solution(test_moveset, size, data):
                    #print("-----merge-right-----")
                    moveset = test_moveset[:]

    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i]

    for i in range(len(moveset)):
        car = moveset[i][0]
        for j in range(i+1,len(moveset)):
            test_moveset = copy.deepcopy(moveset)
            test_moveset[i][1] = 0  
            if check_solution(test_moveset, size, data):
                #print("-----merge-right-----")
                moveset = test_moveset[:]

    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i] 
   
    return moveset


# returns True if the given moeset solves the board
def check_solution(moveset, size, data):
    game = Board(size,data)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])
    return game.won()