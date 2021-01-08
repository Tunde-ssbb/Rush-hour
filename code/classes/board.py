import csv
import numpy as np
from code.classes.car import Car


class Board():

    def __init__(self, size, csv):
        self.size = size
        self.cars = {}
        self.moves = []
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

        # isolate path of move
        if step < 0:
            path = board[place + step : place]
        else:
            path = board[place + car.length : (place + car.length + step)%board.size]

        # check if path is free
        if path.size:
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

    def save_log(self):
        # create output csv file
        with open('data/logs/output.csv', 'w') as output_file:
            csv_writer = csv.writer(output_file, delimiter=',')

            # write headers and moves in output file
            csv_writer.writerow(['car', 'move'])
            csv_writer.writerows(self.moves)

    # util function used in move
    def range_for_move_order(self, step, length):
        if step < 0:
            range_of_i = range(length)
        else:
            range_of_i = range(length - 1, -1, -1)
        return range_of_i