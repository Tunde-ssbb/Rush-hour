from code.classes.board import Board
from code.util import save_log, make_animation
import random
import copy

def improve_solutions(solutions, data, animation, log):
    """
    algorithm that takes solutions and removes and reorders the moves so that it gets smaller.
    with the animation and log parameter it is possible to make those of every solution.

    The current algotithm is optimized for large solutions of bigger boards, this can be changed with the parameters:
    minimum_improvement: lower will be faster on smaller boards
    chunk_size (useless_moves): a size of 10 is fine for all boards but can be set.
    chunk_size (in remove_cut_inaccuracy line 28): for the small boards can be skipped by using a large number  
    """

    short_solutions = []
    solution_number = 1
    
    for solution in solutions:
        short_solution = solution
        print(f"Initial length of solution {solution_number}: {len(short_solution)}")

        print("________Removing_cut_useless_moves_____________")
        
        # cut the solution up in chunks and remove the useless moves until the improvement is the minimum_improvement or less
        short_solution = remove_cut_useless_moves(short_solution, data, minimum_improvement=50, chunk_size=10)

        print("________Removing_cut_inaccuracy________________")
        # cut the solution up in chunks and remove the inaccuracy until there is no more improvement
        short_solution = remove_cut_inaccuracy(short_solution, data, chunk_size=30)

        print("________Removing_cut_useless_moves_increasing__")
        # cut the solution up in chunks and remove the useless moves, multiplying the chunk size by 2 every loop iteration
        short_solution = remove_cut_useless_moves_increasing(short_solution, data, chunk_size=10)
        print("________Removing_useless_moves_________________")
        # remove the useless moves but now of the whole solution
        short_solution = remove_useless_moves_all(short_solution, data)
        
        print("________Removing_inaccuracy____________________")
        # try to restructure moves of a car that makes moves in the same direction twice (inaccuracy)
        short_solution = removing_inaccuracy_all(short_solution, data)
        
        print(f"solution_number {solution_number} final length : {len(short_solution)}\n")
        short_solutions.append(short_solution)
        
        if animation:
            make_animation(short_solution, data, str(solution_number))
        if log:
            save_log(short_solution, str(solution_number))
        solution_number += 1
    return short_solutions

def remove_useless_moves(moveset, data, start_hash=None, end_hash=None):
    """
    function combines moves of the same car and checks if the solution is still valid
    hashes are used for a part of a solution
    """
    # set 2 moves to 0
    moveset = combine(moveset, data, method="remove", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # add the steps of the first to the second
    moveset = combine(moveset, data, method="left", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # add the steps of the second to the first
    moveset = combine(moveset, data, method="right", start_hash=start_hash, end_hash=end_hash)
    moveset = remove0moves(moveset)
    # set one move to 0
    moveset = combine(moveset, data, method="single", start_hash=start_hash, end_hash=end_hash)
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

def combine(moveset, data, method, start_hash=None, end_hash=None):
    """
    function combines moves of the same car and checks if the solution is still valid
    """
    for i in range(len(moveset)):
        car = moveset[i][0]
        if method == "single":
            test_moveset = copy.deepcopy(moveset)
            test_moveset[i][1] = 0
            if start_hash == None:  
                if check_solution(test_moveset, data):
                    moveset = test_moveset[:]
            else:
                if check_solution_to_hash(test_moveset, data, start_hash, end_hash):
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
                        if check_solution(test_moveset, data):
                            moveset = test_moveset[:]
                    else:
                        if check_solution_to_hash(test_moveset, data, start_hash, end_hash):
                            moveset = test_moveset[:]
    return moveset

def check_solution(moveset, data):
    """
    tests if the given moveset is a solution
    """
    game = Board(data)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])
    return game.won()

def check_solution_to_hash(moveset, data, start_hash, end_hash):
    """
    tests if the given moveset reaches the next board state
    """
    game = Board(data, hash=start_hash)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])

    result = game.give_hash()

    return result == end_hash

def check_for_possible_inaccuracy(moveset, data):
    """
    returns a list of the cars and their move numbers where they go in the same direction twice in a row
    """
    game = Board(data)
    cars = game.cars
    last_direction = {}
    canidates = []
    
    move_number = 0
    for car in cars:
        last_direction[car] = [0, move_number]

    for move in moveset:
        # direction is 1 or -1
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

def solve_inaccuracy(moveset, canidates, data, start_hash=None, end_hash=None):
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
                    if start_hash == None:
                        if check_solution(test_moveset, data):
                            index_first += 1
                            moveset = test_moveset
                        else:
                            break
                    else:
                        if check_solution_to_hash(test_moveset, data, start_hash, end_hash):
                            index_first += 1
                            moveset = test_moveset
                        else:
                            break

                chunk_size += 1          

        if start_hash == None:
            moveset = remove_useless_moves(moveset, data)        
        else:
            moveset = remove_useless_moves(moveset, data, start_hash, end_hash)           
        

    return moveset

def cut_moveset_and_get_board_hashes(moveset, chunck_size, data):
    """
    cut the moveset in smaller parts and hash the board states
    """
    hashes = []
    cut_moveset = []
    moves = []
    game = Board(data)
    # hash begin position board
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

def improve_cut_solution(separated_moveset, hashes, data):
    """
    removes the useless moves of the cut solution
    """
    for i in range(len(separated_moveset)):
        start_hash = hashes[i]
        end_hash = hashes[i+1]
        separated_moveset[i] = remove_useless_moves(separated_moveset[i], data, start_hash=start_hash, end_hash=end_hash)
    
    moveset = []
    for chunk in separated_moveset:
        moveset = moveset + chunk

    return moveset

def solve_cut_inaccuracy(separated_moveset, canidates, hashes, data):
    """
    removes inaccuracy in a cut solution
    """
    for i in range(len(separated_moveset)):
        separated_moveset[i] = solve_inaccuracy(separated_moveset[i], canidates[i], data, start_hash=hashes[i], end_hash=hashes[i+1])
        
    moveset = []
    for chunk in separated_moveset:
        moveset = moveset + chunk

    return moveset

def remove_cut_useless_moves(short_solution, data, minimum_improvement=0, chunk_size=10):
    """
    remove useless moves from a subset of the solution until the improvement is
    equal or less than the minimum_improvement
    """
    old_length = len(short_solution)
    new_length = 0
    while old_length - new_length > minimum_improvement:
        old_length = len(short_solution)
        separated_moveset, hashes, last_moves = cut_moveset_and_get_board_hashes(short_solution, chunk_size, data)
        short_solution = improve_cut_solution(separated_moveset, hashes, data) + last_moves
        new_length = len(short_solution)
        print(len(short_solution))
    
    return short_solution

def remove_cut_inaccuracy(short_solution, data, chunk_size=30):
    """
    remove inaccuracies from a subset of the solution until there is no improvement
    """
    old_length = len(short_solution)
    new_length = 0
    while old_length > new_length:
        old_length = len(short_solution)
        separated_moveset, hashes, last_moves = cut_moveset_and_get_board_hashes(short_solution, chunk_size, data)

        canidates = []
        for moveset in separated_moveset:
            canidates.append(check_for_possible_inaccuracy(moveset, data))
        
        short_solution = solve_cut_inaccuracy(separated_moveset, canidates, hashes, data) + last_moves
        new_length = len(short_solution)
    return short_solution

def remove_cut_useless_moves_increasing(short_solution, data, chunk_size=10):
    """
    remove inaccuracies from a subset of the solution while increasing the chunk_size.
    stops when the chunk_size is more than half of the solution size
    """
    while chunk_size < len(short_solution) / 2:
        separated_moveset, hashes, last_moves = cut_moveset_and_get_board_hashes(short_solution, chunk_size, data)
        short_solution = improve_cut_solution(separated_moveset, hashes, data) + last_moves
        chunk_size = chunk_size * 2
    return short_solution

def remove_useless_moves_all(short_solution, data):
    """
    remove useless moves from the solution until there is no improvement
    """
    old_length = len(short_solution)
    new_length = 0
    while old_length > new_length:
        old_length = len(short_solution)
        short_solution = remove_useless_moves(short_solution, data)
        new_length = len(short_solution)
    return short_solution

def removing_inaccuracy_all(short_solution, data):
    """
    remove inaccuracies from the solution until there is no improvement
    """
    old_length = len(short_solution)
    new_length = 0
    while old_length > new_length:
        old_length = len(short_solution)
        canidates = check_for_possible_inaccuracy(short_solution, data)
        short_solution = solve_inaccuracy(short_solution, canidates, data)
        new_length = len(short_solution)
    return short_solution
