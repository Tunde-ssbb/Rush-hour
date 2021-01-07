class Car():

    def __init__(self, letter_id, orientation, length, x, y):
        self.letter_id = letter_id
        self.orientation = orientation
        self.length = length
        # misschien x en y veranderen in een gecombineerde variable, dus:
        # self.location = [x - 1, y - 1]
        self.x = x - 1
        self.y = y - 1
    
    def move(self):
        pass