from code.classes.board import Board
import random
import copy

def improve_solutions(solutions, size, data, animation, log):
    if  len(solutions) > 0:
        short_solutions = []
        solution_number = 1
        for solution in solutions:
            short_solution = solution
            old_length = len(short_solution)
            new_length = old_length - 1
            while old_length > new_length:
                old_length = len(short_solution)
                short_solution = remove_useless_moves(short_solution, size, data)
                new_length = len(short_solution)
            
            #make_animation(short_solution, size, data, str(solution_number))
            #save_log(short_solution, str(solution_number))
            print(f"solution_number {solution_number} length : {len(short_solution)}")
            solution_number += 1
            short_solutions.append(short_solution)

def remove_useless_moves(moveset, size, data):
    
    moveset = combine(moveset, size, data, method="remove")
    moveset = remove0moves(moveset)
    moveset = combine(moveset, size, data, method="left")
    moveset = remove0moves(moveset)
    moveset = combine(moveset, size, data, method="right")
    moveset = remove0moves(moveset)
    moveset = combine(moveset, size, data, method="single")
    moveset = remove0moves(moveset)
   
    return moveset

def remove0moves(moveset):
    for i in range(len(moveset) - 1, -1, -1):
        if moveset[i][1] == 0:
            del moveset[i]
    return moveset

def combine(moveset, size, data, method):
    for i in range(len(moveset)):
        car = moveset[i][0]
        if method == "single":
            test_moveset = copy.deepcopy(moveset)
            test_moveset[i][1] = 0  
            if check_solution(test_moveset, size, data):
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
                        test_moveset[j][1] = moveset[i][1] + moveset[j][1]
    
                    if check_solution(test_moveset, size, data):
                        moveset = test_moveset[:]
    return moveset

# returns True if the given moeset solves the board
def check_solution(moveset, size, data):
    game = Board(size,data)
    for move in moveset:
        if not game.validate_move(move[0],move[1]):
            return False
        game.move(move[0],move[1])
    return game.won()