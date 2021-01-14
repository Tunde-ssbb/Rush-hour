import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from code.classes.car import Car
#from code.classes.archive import Archive


class Board():

    def __init__(self, size, csv):
        self.size = size
        self.cars = {}
        self.moves = []
        self.shortest_solution_movesets = []
        self.archive = set()
        self.load_cars_from_csv(csv)
        self.board = np.full((size, size), "#")
        self.load_board()

    def load_board(self):
        """
        Fill the game board with the appropriate car letters in the right place
        according to the cars dictionary of the board.
        """

        # retrieve all car objects and loop
        for car in self.cars.values():
            for i in range(car.length):

                # place letter id in spaces occupied by the car
                if car.orientation == "H":
                    self.board[car.y][car.x + i] = car.letter_id
                else:
                    self.board[car.y + i][car.x] = car.letter_id
    
    def load_board_from_hash(self, hash):
        """
        Fill the game board with the appropriate car letters in the right place
        according to a given board hash. input: hash (str)
        """
        cars_done = set()
        
        # set location of the cars on the board
        for i in range(self.size):
            row = hash[:self.size]
            for j in range(self.size):
                self.board[i][j]= row[j]

                # set x and y position of car
                if row[j] != "#" and row[j] not in cars_done:
                    car = self.cars[row[j]]
                    car.x = j
                    car.y = i
                    cars_done.add(row[j])

            hash = hash[self.size:]
        
    def load_cars_from_csv(self, source_file):
        """
        Create car objects from csv file and place them in cars ditionary.
        """
        
        # read into sourcefile
        with open(source_file, 'r') as csv_file:
            car_reader = csv.DictReader(csv_file, delimiter=',')

            # create object for each car in file and store in dictionary
            for row in car_reader:
                car_object = Car(row['car'], row['orientation'], int(row['length']), int(row['row']), int(row['col']))
                self.cars.update({row['car']: car_object})

    def draw_board(self):
        """
        Create a text-based representation of the board in the terminal
        """
    
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j] + "  ", end="")
            print("")
        print("---" * self.size)
        
    def validate_move(self, car, step):
        """
        Validate a specific move. Input: car (str:letter_id), step(int). Output: boolean.
        """
        
        # find possible moves
        moves = self.find_moves()

        # return if given move is in possible moves
        return ((car in moves) and (step in range(moves[car][0], moves[car][1] + 1)))


    def move(self, car, step):
        """
        Move car on board. Input: car(str:letter_id), step(int). 
        """
        car_object = self.cars[car]
        
        x = car_object.x
        y = car_object.y

        # change the position in the car object
        car_object.move(step)
        
        # change the position on the board
        if car_object.orientation == "H":
            # set the order of moving
            range_of_i = self.range_for_move_order(step, car_object.length)
            for i in range_of_i:
                # swap character
                self.board[y, x + i],self.board[y, x + step + i] = self.board[y, x + step + i], self.board[y, x + i]
                
        else:            
            # set the order of moving
            range_of_i = self.range_for_move_order(step, car_object.length)

            for i in range_of_i:
                # swap character
                self.board[y + i, x],self.board[y + step + i, x] = self.board[y + step + i, x], self.board[y + i, x]

    def won(self):
        """
        Check if the game was won (car X is free to leave). Output: boolean
        """
        car = self.cars['X']
        return (car.x == self.size - car.length)
    

    def log_move(self, car_id, step):
        """
        Log a move in the game. Input: car_id (str), step(int)
        """
        # add current move to list of moves
        self.moves.append([car_id, step])
    
    def log_shortest_solution_movesets(self, moveset):
        """
        Save the current moveset as the shortest solution. Input: moveset (list[list[car(str),step(int)]])
        """
        self.shortest_solution_movesets = moveset

    def step_back(self):
        """
        Remove last move from saved moveset. Does not adjust the board.
        """
        self.moves.pop()

    def save_log(self):
        """
        Save the current saved moveset in a csv file. Output: csv file
        """
        # create output csv file
        with open('data/logs/output.csv', 'w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')

            # write headers and moves in output file
            csv_writer.writerow(['car', 'move'])
            csv_writer.writerows(self.moves)

    def archive_board(self):
        """
        Add the current state of the board the the game archive (in form of a hash)
        """

        # fetch string representation of board
        hash_board = self.give_hash()
        self.archive.add(hash_board)


    def give_hash(self):
        """
        Creates a string representation of the boardstate (unique to each board setup)
        Output: hash(str)
        """

        # create string representation of board
        hash_board = ""
        for row in self.board:
            for place in row:
                hash_board = hash_board + str(place)
        return hash_board

    # util function used in move
    def range_for_move_order(self, step, length):
        """
        Help function used in move function. Input: step(int), length(int). Output: range_of_i(range object)
        """
        if step < 0:
            range_of_i = range(length)
        else:
            range_of_i = range(length - 1, -1, -1)
        return range_of_i

    def find_moves(self):
        """
        Function find all possible moves in current board state. 
        Output: possible_moves (dict{car_id(str):moving range(list[start(int),stop(int)])})
        """

        possible_moves = {} 

        for car_id in self.cars:
            car = self.cars[car_id]

            # isolate board row/column containing car
            if car.orientation == "H":
                board = self.board[car.y,:]
                place = car.x
            else:
                board = self.board[:,car.x]
                place = car.y
            
            # isolate squares ahead, and behind the car
            backward = board[:place]
            forward = board[place+car.length:]

            # count available squares
            moves_forward = 0
            moves_backward = 0
            for i in forward:
                if i=="#":
                    moves_forward += 1
                else:
                    break
            for i in np.flip(backward):
                if i=="#":
                    moves_backward += 1
                else:
                    break

            # save moves in car object
            car.moves = (-moves_backward, moves_forward)

            # add to possible moves dictionary if moves are possible
            if moves_forward != 0 or moves_backward != 0:
                possible_moves.update({car.letter_id: [-moves_backward, moves_forward]})

        return possible_moves

            
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
            "U" : dark_blue, "V" : purple, "W" : purple, "Y" : dark_yellow, "Z" : grey}
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


