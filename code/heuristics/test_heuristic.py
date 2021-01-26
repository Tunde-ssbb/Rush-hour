from code.classes.board import Board
import csv
from code.heuristics.blocking_cars import blocking_cars_calculate_score
from code.heuristics.winning_comparison import winning_comparison
from code.heuristics.a_star import a_star_heuristic

def test_heuristic(game, heuristic, size, data, best=True):
    solution = load_winning_moveset(size, data)
    scores = []
    if heuristic == "blocking_cars":
        
        if best:
            scores.append(round(blocking_cars_calculate_score(game, depth=2),5))
            for move in solution:
                game.move(move[0], move[1])
                scores.append(round(blocking_cars_calculate_score(game, depth=2),5))
        else:
            scores.append([round(blocking_cars_calculate_score(game, depth=2),5)])
            
            for move in solution:
                hash = game.give_hash()
                next_scores = []
                possible_moves = game.find_moves()

                cars = list(possible_moves.keys())
                for car in cars:
                    possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
                    if 0 in possible_steps:
                        possible_steps.remove(0)

                    for step in possible_steps:
                        game.load_board_from_hash(hash)
                        game.move(car, step)
                        next_scores.append(round(blocking_cars_calculate_score(game, depth=2),5))

                game.load_board_from_hash(hash)
                game.move(move[0], move[1])
                scores.append(next_scores)


    elif heuristic == "winning_comparison":
        winning_hash = get_winning_hash(solution, size, data)

        if best:
            print(solution)
            scores.append(round(winning_comparison(game ,winning_hash),5))
            for move in solution:
                print(move)
                game.move(move[0], move[1])
                scores.append(round(winning_comparison(game ,winning_hash),5))
        else:
            scores.append([round(winning_comparison(game ,winning_hash),5)])
            
            for move in solution:
                hash = game.give_hash()
                next_scores = []
                possible_moves = game.find_moves()

                cars = list(possible_moves.keys())
                for car in cars:
                    possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
                    if 0 in possible_steps:
                        possible_steps.remove(0)

                    for step in possible_steps:
                        game.load_board_from_hash(hash)
                        game.move(car, step)
                        next_scores.append(round(winning_comparison(game ,winning_hash),5))

                game.load_board_from_hash(hash)
                game.move(move[0], move[1])
                scores.append(next_scores)

    elif heuristic == "a_star":
        if best:
            scores.append(round(a_star_heuristic(game), 5))
            for move in solution:
                game.move(move[0], move[1])
                scores.append(round(a_star_heuristic(game), 5))
        else:
            scores.append([round(a_star_heuristic(game), 5)])
            
            for move in solution:
                hash = game.give_hash()
                next_scores = []
                possible_moves = game.find_moves()

                cars = list(possible_moves.keys())
                for car in cars:
                    possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
                    if 0 in possible_steps:
                        possible_steps.remove(0)

                    for step in possible_steps:
                        game.load_board_from_hash(hash)
                        game.move(car, step)
                        next_scores.append(round(a_star_heuristic(game), 5))

                game.load_board_from_hash(hash)
                game.move(move[0], move[1])
                scores.append(next_scores)


    return scores

def get_winning_hash(solution, size, data):
    game = Board(size, data)
    for move in solution:
        game.move(move[0],move[1])

    return game.give_hash()
