from code.classes.board import Board
from code.util import save_log, make_animation
import random
import copy

def improve_solutions(solutions, size, data, animation, log):
    """
    algorithm that takes solutions and removes and reorders the moves so that it gets smaller.
    with the animation and log parameter it is possible to make those of every solution
    """

    short_solutions = []
    solution_number = 1
    for solution in solutions:
        short_solution = solution
        old_length = len(short_solution)
        new_length = old_length - 1

        # cut the solution up in chunks of size 10 and remove the useless moves it until there is no more improvement
        while old_length > new_length:
            old_length = len(short_solution)
            saperated_moveset, hashes, last_moves = cut_moveset_and_get_board_hashes(short_solution, 10, size, data)
            short_solution = improve_cut_solution(saperated_moveset, hashes, size, data) + last_moves
            new_length = len(short_solution)
            #print(len(short_solution))

        # remove the useless moves but now of the whole solution
        old_length = len(short_solution)
        new_length = old_length - 1
        while old_length > new_length:
            old_length = len(short_solution)
            short_solution = remove_useless_moves(short_solution, size, data)
            new_length = len(short_solution)
        
        # try to restructure moves of a car that makes moves in the same direction twice (inaccuracy)
        old_length = len(short_solution)
        new_length = old_length - 1
        while old_length > new_length:
            old_length = len(short_solution)
            canidates = check_for_possible_inaccuracy(short_solution, size, data)
            short_solution = solve_inaccuracy(short_solution, canidates, size, data)
            new_length = len(short_solution)
            #print(len(short_solution))
            
        
        print(f"solution_number {solution_number} final length : {len(short_solution)}")
        short_solutions.append(short_solution)
        
        if animation:
            make_animation(short_solution, size, data, str(solution_number))
        if log:
            save_log(short_solution, str(solution_number))
        solution_number += 1
    return short_solutions

def remove_useless_moves(moveset, size, data, start_hash=None, end_hash=None):
    """
    function combines moves of the same car and checks if the solution is still valid
    hashes are used for a part of a solution
    """
    # set 2 moves to 0
    moveset = combine(moveset, size, data, method="remove", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # add the steps of the first to the second
    moveset = combine(moveset, size, data, method="left", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # add the steps of the second to the first
    moveset = combine(moveset, size, data, method="right", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # set one move to 0
    moveset = combine(moveset, size, data, method="single", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
   
    return moveset

def remove0moves(moveset):
    """
    remove moves that take a step of 0 
    """
    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i]
    return moveset

def combine(moveset, size, data, method, start_hash=None, end_hash=None):
    """
    function combines moves of the same car and checks if the solution is still valid
    """
    for i in range(len(moveset)):
        car = moveset[i][0]
        if method == "single":
            test_moveset = copy.deepcopy(moveset)
            test_moveset[i][1] = 0
            if start_hash == None:  
                if check_solution(test_moveset, size, data):
                    moveset = test_moveset[:]
            else:
                if check_solution_to_hash(test_moveset, size, data, start_hash, end_hash):
                    moveset = test_moveset[:]
        else:
            for j in range(i+1,len(moveset)):
                if car == moveset[j][0]:
                    test_moveset = copy.deepcopy(moveset)
                    if method == "right":
                        test_moveset[i][1] = moveset[i][1] + moveset[j][1]
                        test_moveset[j][1] = 0
                    elif method == "left":
                        test_moveset[i][1] = 0
                        test_moveset[j][1] = moveset[i][1] + moveset[j][1]
                    elif method == "remove":
                        test_moveset[i][1] = 0
                        test_moveset[j][1] = 0

                    # test if the moveset still is a solution, if it is apply the changes
                    if start_hash == None:
                        if check_solution(test_moveset, size, data):
                            moveset = test_moveset[:]
                    else:
                        if check_solution_to_hash(test_moveset, size, data, start_hash, end_hash):
                            moveset = test_moveset[:]
    return moveset

def check_solution(moveset, size, data):
    """
    tests if the given moveset is a solution
    """
    game = Board(size,data)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])
    return game.won()

def check_solution_to_hash(moveset, size, data, start_hash, end_hash):
    """
    tests if the given moveset reaches the next board state
    """
    game = Board(size,data, hash=start_hash)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])

    result = game.give_hash()

    return result == end_hash

def check_for_possible_inaccuracy(moveset, size, data):
    """
    returns a list of the cars and their move numbers where they go in the same direction twice in a row
    """
    game = Board(size,data)
    cars = game.cars
    last_direction = {}
    canidates = []
    
    # direction is 1 or -1
    move_number = 0
    for car in cars:
        last_direction[car] = [0,move_number]

    for move in moveset:
        direction = int(move[1] / abs(move[1]))
        
        if direction == last_direction[move[0]][0]:
            canidates.append([move[0], last_direction[move[0]][1],move_number])
            last_direction[move[0]][0] = direction
            last_direction[move[0]][1] = move_number
        else:
            last_direction[move[0]][0] = direction
            last_direction[move[0]][1] = move_number
        move_number += 1
    return canidates

def solve_inaccuracy(moveset, canidates, size, data):
    """
    restructure moves of a car that makes moves in the same direction twice (inaccuracy)
    """
    for canidate in canidates:
        index_first = canidate[1]
        index_second = canidate[2]
        # ignore the last move, unlikely it is an inaccuracy and saves alot of time.
        if len(moveset) - index_second > 1:
            chunk_size = 1

            # move the two moves closer to each other
            # if the solution is invalid start moving in chunks
            while chunk_size < canidate[2] - canidate[1]:
                while True:
                    test_moveset = copy.deepcopy(moveset)

                    front = test_moveset[0:index_first]
                    moved_forward = test_moveset[index_first + chunk_size : index_first + chunk_size + 1]
                    chunk = test_moveset[index_first:index_first + chunk_size ]
                    in_place = test_moveset[index_first + chunk_size + 1: index_second]
                    end = test_moveset[index_second:]
                    
                    test_moveset = front + moved_forward + chunk + in_place + end

                    if check_solution(test_moveset, size, data):
                        index_first += 1
                        moveset = test_moveset
                    else:
                        break

                chunk_size += 1          

        moveset = remove_useless_moves(moveset, size, data)

    return moveset

def cut_moveset_and_get_board_hashes(moveset, chunck_size , size, data):
    """
    cut the moveset in smaller parts and hash the board states
    """
    hashes = []
    cut_moveset = []
    moves = []
    game = Board(size,data)
    hashes.append(game.give_hash())
    move_number = 0

    for move in moveset:
        game.move(move[0], move[1])
        moves.append(move)
        move_number += 1
        if move_number % chunck_size == 0:
            hashes.append(game.give_hash())
            cut_moveset.append(moves)
            moves = []

    last_moves = moves

    return cut_moveset, hashes, last_moves

def improve_cut_solution(separated_moveset, hashes, size, data):
    """
    removes the useless moves of the cut solution
    """
    for i in range(len(separated_moveset)):
        start_hash = hashes[i]
        end_hash = hashes[i+1]
        separated_moveset[i] = remove_useless_moves(separated_moveset[i], size, data, start_hash=start_hash, end_hash=end_hash)
    
    moveset = []
    for chunk in separated_moveset:
        moveset = moveset + chunk

    return moveset
