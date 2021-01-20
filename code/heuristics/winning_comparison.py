from code.classes.board import Board
import copy

def winning_comparison(game, winning_hash):
    """
    Function that calls on heuristic function and generates a score for the current board.
    Input: game (Board object), winning_hash (string). Output: score (int)
    """
    # copy game and load the hash positions into the game
    winning_game = copy.deepcopy(game)
    winning_game.load_board_from_hash(winning_hash)

    # calculate score
    score = comparison_score(game, winning_game)

    return score


def comparison_score(game, winning_game):
    """
    Compares positions of cars in current game with the positions in winning game.
    Generates a score for the current board.
    Input: game (Board object), winning_game (Board object). Output: score (int)
    """
    # initiate score on 0
    score = 0

    for car in game.cars.values():
        
        # select the correct car from the winning game
        winning_car = winning_game.cars[car.letter_id]
        
        # compare the x or y values of the cars and add the difference to the score
        if car.orientation == 'H':
            score = score + abs(car.x - winning_car.x)
        else:
            score = score + abs(car.y - winning_car.y)
    
    return score
   