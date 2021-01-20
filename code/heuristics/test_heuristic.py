from code.classes.board import Board
import csv
from code.heuristics.blocking_cars import blocking_cars_calculate_score
from code.heuristics.winning_comparison import winning_comparison
def test_heuristic(game, heuristic, size, data):
    solution = load_winning_moveset(size, data)
    scores = []
    if heuristic == "blocking_cars":
        
        scores.append(round(blocking_cars_calculate_score(game),5))

        for move in solution:
            game.move(move[0], move[1])
            scores.append(round(blocking_cars_calculate_score(game, depth=2),5))
    elif heuristic == "winning_comparison":
        winning_hash = get_winning_hash(solution, size, data)

        scores.append(round(winning_comparison( game ,winning_hash),5))
        for move in solution:
            game.move(move[0], move[1])
            scores.append(round(winning_comparison( game ,winning_hash),5))

    print(scores)

def load_winning_moveset(size, data):
    board_number = data[-5]

    data = f"./data/logs/solution_board{board_number}.csv"
    moves = []
    with open(data, 'r') as csv_file:
        move_reader = csv.DictReader(csv_file, delimiter=',')

        for row in move_reader:
            moves.append([row['car'], int(row['move'])])
    return moves

def get_winning_hash(solution, size, data):
    game = Board(size, data)
    for move in solution:
        game.move(move[0],move[1])

    return game.give_hash()
