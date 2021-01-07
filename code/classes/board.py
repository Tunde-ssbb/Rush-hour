from car import Car
import csv

class Board():
    pass

    def __init__(self):
        self.cars = {}

    def load_board(self):
        pass

    def load_cars(self, source_file):
        
        # read into sourcefile
        with open(source_file, 'r') as csv_file:
            car_reader = csv.DictReader(csv_file, delimiter=',')

            # create object for each car in file and store in dictionary
            for row in car_reader:
                car_object = Car(row['car'], row['orientation'], int(row['length']), int(row['row']), int(row['col']))
                self.cars.update({row['car']: car_object})

    def draw_board(self):
        pass

    def validate_move(self, car, step):
        pass

    def move(self, car, step):
        pass

    def won(self):
        pass