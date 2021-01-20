from code.classes.board import Board
import matplotlib.pyplot as plt
from matplotlib import animation

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

        "./data/gameboards/Rushhour12x12_7.csv" : { "X" : red, "A" : blue, "B" : light_blue,
            "C" : dark_yellow, "D" : dark_blue, "E" : orange,
            "F" : blue, "G" : light_blue, "H" : dark_blue,
            "I" : dark_blue, "J" : orange, "K" : light_blue, "L" : grey,
            "M" : blue, "N" : yellow, "O" : light_blue, "P" : orange,
            "Q" : orange, "R" : dark_blue, "S" : yellow, "T" : blue,
            "U" : dark_blue, "V" : purple, "W" : purple, "Y" : dark_yellow, "AA" : grey,
            "AB" : blue, "AC" : light_blue, "AD" : dark_yellow, "AE" : dark_blue,
            "AF" : orange, "AG" : blue, "AH" : light_blue, "AI" : grey,
            "AJ" : dark_blue, "AK" : dark_yellow, "AL" : purple, "AM" : yellow,
            "AN" : orange, "AO" : purple, "AP" : dark_yellow, "AQ" : orange, 
            "AR" : light_blue, "AS" : orange}
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
    with open('data/logs/output'+name+'.csv', 'w') as output_file:
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
