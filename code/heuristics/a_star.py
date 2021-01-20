def a_star_heuristic(game):
    red_car = game.cars['X']
    distance_to_exit = (game.size - 1) - red_car.x

    path = game.board[red_car.y, red_car.x + red_car.length:]
    for place in path:
        if place != '#':
            distance_to_exit += 1
            
            target_car = game.cars[place]
            if board[red_car.y - 1, target_car.x] != '#' or board[red_car.y + target_car.length, target_car.x] != '#':
                distance_to_exit += 1

    a_star = len(game.moves) + distance_to_exit
    return a_star
            