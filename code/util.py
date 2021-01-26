from code.classes.board import Board
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.ticker import MaxNLocator
import numpy as np
import csv


def make_animation(moves, size, csv, name):
    """
    Create an gif animation of a particular moveset for a specfic game under a given name. 
    Input: moves (list[list[car_id(str),step(int)]]), size (int), csv (start state of board), name (str)
    """

    # create board
    board = Board(size,csv)

    # define colors
    red = [255,0,0]
    blue = [0,0,255]
    yellow = [255, 255, 0]
    dark_yellow = [150, 150, 0]
    orange = [171, 106, 30]
    light_blue = [0,255,255]
    dark_blue = [40, 96, 99]
    purple = [255, 0, 255]
    grey = [120, 120, 120]

    # define mapping cars to colors
    colormaps = {
        "./data/gameboards/Rushhour6x6_1.csv" : { "X" : red, "A" : blue, "B" : yellow,
                "C" : orange, "D" : dark_blue, "E" : blue,
                "F" : dark_blue,"G" : light_blue,"H" : blue,
                "I" : light_blue,"J" :dark_blue,"K" : orange,"L" : dark_blue},
        
        "./data/gameboards/Rushhour6x6_2.csv" : { "X" : red, "A" : blue, "B" : orange,
                "C" : orange, "D" : dark_blue, "E" : dark_blue,
                "F" : blue,"G" : light_blue,"H" : yellow,
                "I" : dark_blue,"J" : orange,"K" : light_blue,"L" : orange},

        "./data/gameboards/Rushhour6x6_3.csv" : { "X" : red, "A" : light_blue, "B" : purple,
                "C" : yellow, "D" : orange, "E" : light_blue,
                "F" : orange,"G" : orange,"H" : dark_blue},

        "./data/gameboards/Rushhour9x9_4.csv" : { "X" : red, "A" : yellow, "B" : dark_blue,
                "C" : purple, "D" : grey, "E" : blue,
                "F" : purple, "G" : dark_yellow, "H" : yellow,
                "I" : light_blue, "J" : dark_blue, "K" : purple, "L" : orange,
                "M" : dark_blue, "N" : yellow, "O" : blue, "P" : dark_yellow,
                "Q" : blue, "R" : grey, "S" : orange, "T" : light_blue,
                "U" : dark_blue},

        "./data/gameboards/Rushhour9x9_5.csv" : { "X" : red, "A" : yellow, "B" : dark_blue,
                "C" : blue, "D" : dark_blue, "E" : purple,
                "F" : orange, "G" : blue, "H" : light_blue,
                "I" : orange, "J" : dark_yellow, "K" : blue, "L" : orange,
                "M" : dark_blue, "N" : purple, "O" : blue, "P" : yellow,
                "Q" : blue, "R" : grey, "S" : light_blue, "T" : dark_blue,
                "U" : light_blue, "V" : orange, "W" : light_blue},

        "./data/gameboards/Rushhour9x9_6.csv" : { "X" : red, "A" : blue, "B" : light_blue,
            "C" : dark_yellow, "D" : dark_blue, "E" : orange,
            "F" : blue, "G" : light_blue, "H" : dark_blue,
            "I" : dark_blue, "J" : orange, "K" : light_blue, "L" : grey,
            "M" : blue, "N" : yellow, "O" : light_blue, "P" : orange,
            "Q" : orange, "R" : dark_blue, "S" : yellow, "T" : blue,
            "U" : dark_blue, "V" : purple, "W" : purple, "Y" : dark_yellow, "Z" : grey},

        "./data/gameboards/Rushhour12x12_7.csv" : { "X" : red, "A" : purple, "B" : light_blue,
            "C" : dark_blue, "D" : blue, "E" : yellow,
            "F" : orange, "G" : light_blue, "H" : dark_blue,
            "I" : orange, "J" : dark_blue, "K" : orange, "L" : light_blue,
            "M" : grey, "N" : dark_blue, "O" : dark_yellow, "P" : purple,
            "Q" : purple, "R" : dark_yellow, "S" : grey, "T" : orange,
            "U" : light_blue, "V" : yellow, "W" : light_blue, "Y" : dark_blue, "a" : blue,
            "b" : light_blue, "c" : blue, "d" : orange, "e" : purple,
            "f" : yellow, "g" : dark_yellow, "h" : dark_blue, "i" : yellow,
            "j" : dark_blue, "k" : dark_blue, "l" : dark_blue, "m" : dark_yellow,
            "n" : grey, "o" : blue, "p" : light_blue, "q" : purple, 
            "r" : light_blue, "s" : dark_blue}
        }
        
    colormap = colormaps[csv]

    animationframes = []

    # create animation
    fig = plt.figure("animation", dpi=100, figsize=(5.0,5.0))

    # create first frame
    animationframes.append((plt.imshow(make_animation_frame(board.board, size, colormap)),))

    # move board, and make new frame for each move
    for move in moves:
        board.move(move[0],move[1])
        animationframes.append((plt.imshow(make_animation_frame(board.board, size, colormap)),))

    # finish animation
    plt.axis("off")
    im_animation = animation.ArtistAnimation(fig, animationframes, interval=500, repeat_delay=1000, blit=True)
    im_animation.save((name + ".gif"), writer="Pillow") 
    #plt.show()
        

def make_animation_frame(board, size, colormap):
    """
    create an animation frame to be used in animation
    """
    image = np.zeros((size,size,3))
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            if value != "#":
                image[i][j] = colormap[value]

    return image.astype(np.uint8)


def save_log(moves, name):

    # create output csv file
    with open('data/logs/'+name+'.csv', 'w') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',')

        # write headers and moves in output file
        csv_writer.writerow(['car', 'move'])
        csv_writer.writerows(moves)


def get_cars(data):
    with open(data, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        
        cars = []
        for row in csv_reader:
            cars.append(row['car'])

    return cars

def load_winning_moveset(size, data):
    board_number = data[-5]

    data = f"./data/logs/solution_board{board_number}.csv"
    moves = []
    with open(data, 'r') as csv_file:
        move_reader = csv.DictReader(csv_file, delimiter=',')

        for row in move_reader:
            moves.append([row['car'], int(row['move'])])
    return moves

def bar_plot_of_solutions(solutions, board_number, number_of_attempts):
    results = []
    for solution in solutions:
        results.append(len(solution))
    
    lengths = []
    for result in results:
        if result not in lengths:
            lengths.append(result)

    lengths.sort()
    heights = [0]* len(lengths)
    for i in range(len(lengths)):
        for result in results:
            if result == lengths[i]:
                heights[i] += 1
    
    ax = plt.figure(1).gca()

    ax.bar(lengths,heights)
    ax.set_xlabel(f"number_of_moves")
    ax.text(0.45, 0.93, f"shortest solution = {lengths[0]} with {round((heights[0]/sum(heights))* 100, 2)} %", verticalalignment='center', transform=ax.transAxes, bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 5})
    ax.set_title(f" {number_of_attempts} solutions of board {board_number}")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig(f'{number_of_attempts}solutions_of_board{board_number}-2.png')