class Node:
    
    def __init__(self, hash_board, score):
        self.hash_board = hash_board
        self.score = score
        self.previous = set()
        self.next = set()
