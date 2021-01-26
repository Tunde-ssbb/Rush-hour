def a_star_heuristic(game):
    """
    Heuristic that generates a score that represents the minimal number of moves to reach a solution.
    The score consists of the number of moves previously made 
    and the minimal remaining moves to win the game.
    """
    
    score = 0
    # add 1 to score for move with red car
    if not game.won():
        score += 1
    
    # select red car and path
    red_car = game.cars['X']
    path = game.board[red_car.y, red_car.x + red_car.length:]
    
    for place in path:
        # add 1 to score for every car in red cars path
        if place != '#':
            score += 1
            
            # add 1 for blockage of target cars 
            target_car = game.cars[place]
            if game.board[red_car.y - 1, target_car.x] != '#' or game.board[red_car.y + target_car.length, target_car.x] != '#':
                score += 1
    
    # add number of previous moves to score to get A* score
    a_star = len(game.moves) + score
    return a_star
            