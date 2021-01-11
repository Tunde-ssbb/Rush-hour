class Archive:

    def __init__(self):
        self.nodes = set()

    def add_node(self, hash_board, score):
        node = Node(hash_board, score)
        self.nodes.add(node)