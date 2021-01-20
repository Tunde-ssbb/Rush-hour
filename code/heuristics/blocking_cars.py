from code.classes.board import Board
import collections


def blocking_cars_heuristic(game, depth = 1):
    """
    Heuristic that calculates the how much the red car is blocked. Cars that obstruct the path 
    of the red car are weighted by their distance to form a total "blocked score".
    If depth is set to 2, the blocked score of the cars that are blocking the red car will also be added. 
    (higher depths just add layers to this blocked score)
    """
    possible_moves = game.find_moves()
    # find initial score
    score = blocking_cars_calculate_score(game, depth)
    unordered_moves = []
    for car in possible_moves:
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            # try all possible moves
            for step in possible_steps:
                # move car, calculate the change in score, and move back
                game.move(car,step)
                score_change = score - blocking_cars_calculate_score(game, depth)
                game.move(car,-step)
                unordered_moves.append((score_change, [car,step]))
    # order the moves to how much they affected the score
    ordered_moves = sorted(unordered_moves, reverse = True)
    ordered_moves = [move[1] for move in ordered_moves]
    return ordered_moves

def blocking_cars_calculate_score(game, depth = 1):
    """
    Function calculates the total blocked score of a game board as explained in blocking cars heuristic
    """
    cars, score = find_block(game, "X")
    i=0
    while i < depth:
        new_cars = []
        # find the blocked score for eaching blocking car (initially this is harcoded to be the red car)
        for car in cars:
            # find the blocked score of each car, and the blocking cars
            blocking_cars, new_score = find_block(game, car)
            new_cars.extend(blocking_cars)
            # add to total score
            score += new_score*(i+1)/5
        cars = new_cars
        i += 1
    return score

def find_block(game, car_id):
    """
    Function finds the block score of a car, as well as the id's of the cars that are blocking it
    """
    car = game.cars[car_id]
    blocked_score = 0 
    blocking_cars = []

    # isolate board row/columns
    if car.orientation == "H":
        path = game.board[car.y,:]
        place = car.x
    else:
        path = game.board[:,car.x]
        place = car.y
    # the red car can only be bloocked in forward direction
    if car_id == "X":
        path = path[place + car.length:]
    # for each blocked space in the row/column, something is added to the score
    for space,i in zip(path,range(len(path))):
        if space != "#" and space != car_id:
            blocking_cars.append(space)
            if car_id == "X":
                # the distance to the car in question affects the score
                blocked_score += 10/(i+1)
            elif i < place:
                blocked_score += 10/(place - i + 1)
            else:
                blocked_score += 10/(i-(place + car.length)+1)

    return blocking_cars, blocked_score
