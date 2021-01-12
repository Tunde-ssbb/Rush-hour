from code.classes.board import Board

def depth_first_algorithm(game):
    if game.won():
        game.working_solution_movesets.append(game.moves)

    if game.give_hash() not in game.archive:
        game.draw_board()
        current_board_state = game.give_hash() 
        game.archive_board()
        print(game.archive)
        possible_moves = game.find_moves()
        for car in possible_moves.keys():
            possible_steps = list(range(possible_moves[car][0], possible_moves[car][1]+1))
            if 0 in possible_steps:
                possible_steps.remove(0)
            print(f"possible_steps for {car}: {possible_steps}")

            for step in possible_steps:
                print(f"{car} does {step}")
                game.move(car, step)
                game.moves.append([car,step])
                print(F"moves taken : {game.moves}")
                depth_first_algorithm(game)
                game.step_back()
                game.load_board_from_hash(current_board_state)
    else:
        print("repeated state")



