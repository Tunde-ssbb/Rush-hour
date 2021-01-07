from car import Car
import csv
import numpy as np

class Board():
    pass

    def __init__(self, size, csv):
        self.size = size
        self.cars = {}
        load_cars(csv)
        self.board = np.full((size, size), "#")
        load_board(self)

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
        return self.board

    def validate_move(self, car, step):
        pass

    def move(self, car, step):
        pass

    def won(self):
        pass

