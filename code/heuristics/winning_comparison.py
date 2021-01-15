from code.classes.board import Board
import copy

def winning_comparison(game, winning_hash):
    winning_game = copy.deepcopy(game)
    winning_game.load_board_from_hash(winning_hash)

    score = comparison_score(game, winning_game)

    return score


def comparison_score(game, winning_game):
    score = 0

    for car in game.cars.values():
        winning_car = winning_game.cars[car.letter_id]
        if car.orientation == 'H':
            score = score + abs(car.x - winning_car.x)
        else:
            score = score + abs(car.y - winning_car.y)
    
    return score
   