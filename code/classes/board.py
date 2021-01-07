import numpy as np

class Board():
    pass

    def __init__(self, size, csv):
        self.size = size
        self.cars = {}
        #load_cars(csv)
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
        pass

    def draw_board(self):
        pass

    def validate_move(self, car, step):
        pass

    def move(self, car, step):
        pass

    def won(self):
        pass