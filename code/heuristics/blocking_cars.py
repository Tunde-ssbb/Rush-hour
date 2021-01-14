from code.classes.board import Board
import collections


def blocking_cars_heuristic(game):
    possible_moves = game.find_moves()
    score = calculate_score(game)
    unordered_moves = []
    for car in possible_moves:
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)

            for step in possible_steps:
                game.move(car,step)
                score_change = score - calculate_score(game)
                game.move(car,-step)
                unordered_moves.append((score_change, [car,step]))
    ordered_moves = sorted(unordered_moves, reverse = True)
    ordered_moves = [move[1] for move in ordered_moves]
    return ordered_moves




def calculate_score(game):
    cars, score = find_block(game, "X")
    for car in cars:
        new_cars, new_score = find_block(game, car)
        score += new_score
    return score

def find_block(game, car_id):
    car = game.cars[car_id]
    blocked_score = 0 
    blocking_cars = []
    if car.orientation == "H":
        path = game.board[car.y,:]
        place = car.x
    else:
        path = game.board[:,car.x]
        place = car.y
    if car_id == "X":
        path = path[place + car.length:]
    for space,i in zip(path,range(len(path))):
        if space != "#" and space != car_id:
            blocking_cars.append(space)
            if car_id == "X":
                blocked_score += 10/(i+1)
            elif i < place:
                blocked_score += 10/(place - i + 1)
            else:
                blocked_score += 10/(i-(place + car.length)+1)

    return blocking_cars, blocked_score
