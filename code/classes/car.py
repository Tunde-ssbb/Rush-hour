class Car():

    def __init__(self, letter_id, orientation, length, x, y):
        self.letter_id = letter_id
        self.orientation = orientation
        self.length = length
        self.x = x - 1
        self.y = y - 1
    
    def move(self,step):
        if self.orientation == "H":
            self.x = self.x + step
        else:
            self.y = self.y - step