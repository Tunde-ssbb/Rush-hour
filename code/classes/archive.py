class Archive:

    def __init__(self):
        self.nodes = set()

    def add_node(self, hash_board, score):
        Node(hash_board, score)