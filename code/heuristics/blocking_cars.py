from code.classes.board import Board

def blocking_cars(game):
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
    for space,i in zip(path,range(len(path))):
        if space != "#" and space != car_id:
            blocking_cars.append(space)
            if i < place:
                blocked_score += 10/(place - i + 1)
            else:
                blocked_score += 10/(i-(place + car.length)+1)

    return blocking_cars, blocked_score
