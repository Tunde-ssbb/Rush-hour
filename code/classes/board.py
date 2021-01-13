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
        self.load_cars(csv)
        self.board = np.full((size, size), "#")
        self.load_board()

    def load_board(self):
        # fill the board
        for car in self.cars.values():
            for i in range(car.length):
                if car.orientation == "H":
                    self.board[car.y][car.x + i] = car.letter_id
                else:
                    self.board[car.y + i][car.x] = car.letter_id

    def load_board_from_hash(self, hash):
        cars_done = set()
        # set cars on the board
        for i in range(self.size):
            row = hash[:self.size]
            for j in range(self.size):
                self.board[i][j]= row[j]
                # set car x and y
                if row[j] != "#" and row[j] not in cars_done:
                    car = self.cars[row[j]]
                    car.x = j
                    car.y = i
                    cars_done.add(row[j])

            hash = hash[self.size:]
        
    def load_cars(self, source_file):
        
        # read into sourcefile
        with open(source_file, 'r') as csv_file:
            car_reader = csv.DictReader(csv_file, delimiter=',')

            # create object for each car in file and store in dictionary
            for row in car_reader:
                car_object = Car(row['car'], row['orientation'], int(row['length']), int(row['row']), int(row['col']))
                self.cars.update({row['car']: car_object})

    def draw_board(self):
    
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j] + "  ", end="")
            print("")
        print("---" * self.size)
        


    def validate_move(self, car, step):
        car = self.cars[car]

        # isolate board row/column
        if car.orientation == "H":
            board = self.board[car.y,:]
            place = car.x
        else:
            board = self.board[:,car.x]
            place = car.y
            step = -step

        # isolate path of move
        if step < 0:
            path = board[place + step : place]
        else:
            path = board[place + car.length : (place + car.length + step)]

        # check if path is free
        if path.size == abs(step):
            return np.all(path == "#") 
        return False


    def move(self, car, step):
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
            # definition of direction
            step = -step
            
            # set the order of moving
            range_of_i = self.range_for_move_order(step, car_object.length)

            for i in range_of_i:
                # swap character
                self.board[y + i, x],self.board[y + step + i, x] = self.board[y + step + i, x], self.board[y + i, x]

    def won(self):
        car = self.cars['X']
        return (car.x == self.size - car.length)
    

    def log_move(self, car_id, step):
        # add current move to list of moves
        self.moves.append([car_id, step])
    
    def log_shortest_solution_movesets(self, moveset):
        self.shortest_solution_movesets = moveset

    def step_back(self):
        self.moves.pop()

    def save_log(self):
        # create output csv file
        with open('data/logs/output.csv', 'w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')

            # write headers and moves in output file
            csv_writer.writerow(['car', 'move'])
            csv_writer.writerows(self.moves)


    def archive_board(self):
        # create string representation of board
        hash_board = ""
        for row in self.board:
            for place in row:
                hash_board = hash_board + str(place)

        self.archive.add(hash_board)

    def give_hash(self):
        hash_board = ""
        for row in self.board:
            for place in row:
                hash_board = hash_board + str(place)
        return hash_board

    # util function used in move
    def range_for_move_order(self, step, length):
        if step < 0:
            range_of_i = range(length)
        else:
            range_of_i = range(length - 1, -1, -1)
        return range_of_i

    def find_moves(self):
        possible_moves = {} 
        for car_id in self.cars:
            car = self.cars[car_id]

            # isolate board row
            if car.orientation == "H":
                board = self.board[car.y,:]
                place = car.x
            else:
                board = self.board[:,car.x]
                place = car.y

            backward = board[:place]
            forward = board[place+car.length:]
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
 
            if car.orientation == "V":
                temp = moves_backward
                moves_backward = moves_forward
                moves_forward = temp
            car.moves = (-moves_backward, moves_forward)

            if moves_forward != 0 or moves_backward != 0:
                possible_moves.update({car.letter_id: [-moves_backward, moves_forward]})

        return possible_moves

            
def make_animation(moves, size, csv, name):
    board = Board(size,csv)

    red = [255,0,0]
    blue = [0,0,255]
    yellow = [255, 255, 0]
    dark_yellow = [150, 150, 0]
    orange = [171, 106, 30]
    light_blue = [0,255,255]
    dark_blue = [40, 96, 99]
    purple = [255, 0, 255]
    grey = [120, 120, 120]

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

    fig = plt.figure("animation", dpi=100, figsize=(5.0,5.0))
    animationframes.append((plt.imshow(make_animation_frame(board.board, size, colormap)),))

    for move in moves:
        board.move(move[0],move[1])
        animationframes.append((plt.imshow(make_animation_frame(board.board, size, colormap)),))

    plt.axis("off")
    im_animation = animation.ArtistAnimation(fig, animationframes, interval=500, repeat_delay=1000, blit=True)
    im_animation.save((name + ".gif"), writer="Pillow") 
    #plt.show()
        

def make_animation_frame(board, size, colormap):
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


